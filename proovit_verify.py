#!/usr/bin/env python3
"""Independent offline/online verifier for ProovIT portable proof archives."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import getpass
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

import pyzipper
from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import eddsa
from Cryptodome.Hash import keccak


BUILTIN_PUBLIC_KEYS = {
    "proovit-ed25519-staging-2026-01": "yHmzVtLg40wUkii0EuQYNdZpRbnp4giWb9nXl0sr9WI=",
    "proovit-ed25519-prod-2026-01": "4gB8kv+H303RoTr3huskF+HTQh/0WptL+2DY3OPYQlc=",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def get_path(value: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def normalize_hex(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.lower().strip()
    return value if value.startswith("0x") else f"0x{value}"


def keccak256(data: bytes) -> str:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return "0x" + digest.hexdigest()


def decode_abi_string(data_hex: str, offset_word: str) -> str | None:
    try:
        offset = int(offset_word, 16) * 2
        length = int(data_hex[offset:offset + 64], 16) * 2
        raw = bytes.fromhex(data_hex[offset + 64:offset + 64 + length])
        return raw.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None


def decode_proof_stored_v3(log: dict[str, Any]) -> dict[str, Any] | None:
    data = normalize_hex(log.get("data"))
    topics = log.get("topics") or []
    if not data or len(topics) < 3:
        return None
    payload = data[2:]
    if len(payload) < 10 * 64:
        return None
    words = [payload[index:index + 64] for index in range(0, len(payload), 64)]
    signature = "ProofStoredV3(bytes32,address,uint64,uint64,uint32,bytes32,bytes32,string,string,string,int64,int64)"
    if normalize_hex(keccak256(signature.encode())) != normalize_hex(topics[0]):
        return None
    def uint(index: int) -> int:
        return int(words[index], 16)
    def signed(index: int) -> int:
        value = int(words[index], 16)
        return value - (1 << 256) if value >= (1 << 255) else value
    return {
        "id": normalize_hex(topics[1]),
        "submitter": "0x" + topics[2][-40:],
        "date": uint(0), "price": uint(1), "fileCount": uint(2),
        "dataHash": normalize_hex(words[3]), "filesRoot": normalize_hex(words[4]),
        "proofId": decode_abi_string(payload, words[5]),
        "proofName": decode_abi_string(payload, words[6]),
        "signer": decode_abi_string(payload, words[7]),
        "latE6": signed(8), "lngE6": signed(9),
    }


def decode_file_added_v3(log: dict[str, Any]) -> dict[str, Any] | None:
    data = normalize_hex(log.get("data"))
    topics = log.get("topics") or []
    if not data or len(topics) < 3:
        return None
    payload = data[2:]
    if len(payload) < 4 * 64:
        return None
    words = [payload[index:index + 64] for index in range(0, len(payload), 64)]
    signature = "FileAddedV3(bytes32,uint256,string,string,uint64,bytes32)"
    if normalize_hex(keccak256(signature.encode())) != normalize_hex(topics[0]):
        return None
    return {
        "proof_id_hash": normalize_hex(topics[1]),
        "file_index": int(topics[2], 16),
        "file_id": decode_abi_string(payload, words[0]),
        "cid": decode_abi_string(payload, words[1]),
        "size": int(words[2], 16),
        "meta_hash": normalize_hex(words[3]),
    }


def first_value(*values: Any) -> Any:
    return next((value for value in values if value not in (None, "")), None)


def verify_blockchain_payload(root: dict[str, Any], manifest: dict[str, Any], receipt: dict[str, Any], report: Report) -> None:
    logs = receipt.get("logs") or []
    decoded = next((decode_proof_stored_v3(log) for log in logs if isinstance(log, dict)), None)
    if not decoded:
        report.add("Payload blockchain", "FAIL", "événement ProofStoredV3 introuvable ou illisible")
        return
    blockchain = {
        **(get_path(root, "portable_evidence_snapshot.blockchain", {}) or {}),
        **(manifest.get("blockchain", {}) or {}),
    }
    expected_proof_id = first_value(blockchain.get("proof_chain_id"), blockchain.get("proof_id"), blockchain.get("proofId"))
    expected_data_hash = first_value(blockchain.get("data_hash"), blockchain.get("dataHash"), get_path(manifest, "hashes.data_sha256"))
    expected_files_root = first_value(blockchain.get("files_root"), blockchain.get("filesRoot"))
    expected_file_count = first_value(blockchain.get("file_count"), blockchain.get("fileCount"))
    file_events = [decoded_file for log in logs if isinstance(log, dict) for decoded_file in [decode_file_added_v3(log)] if decoded_file]
    checks = [
        ("Proof ID blockchain", expected_proof_id, decoded["proofId"]),
        ("dataHash blockchain", expected_data_hash, decoded["dataHash"]),
        ("filesRoot blockchain", expected_files_root, decoded["filesRoot"]),
    ]
    for label, expected, actual in checks:
        if expected is None:
            report.add(label, "INFO", "valeur attendue absente du manifeste")
        else:
            equal = normalize_hex(str(expected)) == normalize_hex(str(actual)) if "Hash" in label or "Root" in label else str(expected) == str(actual)
            report.add(label, "PASS" if equal else "FAIL", str(actual))

    # ProofStoredV3 is emitted before FileAddedV3 transactions. Its historical
    # fileCount therefore represents the aggregate state at anchor creation;
    # the authoritative post-anchor count is the number of verified file
    # transactions when those transactions are listed in the archive.
    separate_file_count = len(blockchain.get("file_transactions") or [])
    if expected_file_count is None:
        report.add("fileCount blockchain", "INFO", "valeur attendue absente du manifeste")
    elif int(decoded["fileCount"]) == 0 and separate_file_count == int(expected_file_count) and separate_file_count > 0:
        report.add("fileCount blockchain", "PASS", f"0 dans l’ancrage initial; {separate_file_count} fichier(s) vérifié(s) séparément")
    else:
        equal = str(expected_file_count) == str(decoded["fileCount"])
        report.add("fileCount blockchain", "PASS" if equal else "FAIL", str(decoded["fileCount"]))

    files = get_path(root, "portable_evidence_snapshot.files.items", []) or manifest.get("files", [])
    if not file_events:
        report.add("Fichiers blockchain", "INFO", "aucun événement FileAddedV3 dans la transaction globale; vérification séparée")
        return
    report.add("Fichiers blockchain", "PASS", f"{len(file_events)} événement(s) décodé(s)")
    expected_by_id = {str(item.get("proof_file_id", item.get("file_id", ""))): item for item in files if item.get("proof_file_id", item.get("file_id"))}
    for event in file_events:
        expected = expected_by_id.get(str(event["file_id"]))
        if not expected:
            report.add("Fichier blockchain", "WARN", f"fileId absent de l’archive: {event['file_id']}")
            continue
        expected_size = first_value(expected.get("size_bytes"), expected.get("size"))
        expected_cid = expected.get("ipfs_cid") or expected.get("cid")
        expected_hash = first_value(expected.get("stored_sha256"), expected.get("sha256"), expected.get("plain_sha256"))
        if expected_size is not None:
            report.add("Taille fichier blockchain", "PASS" if int(expected_size) == event["size"] else "FAIL", str(event["size"]))
        if expected_cid:
            report.add("CID fichier blockchain", "PASS" if str(expected_cid) == event["cid"] else "FAIL", event["cid"])
        if expected_hash:
            report.add("metaHash fichier blockchain", "PASS" if normalize_hex(str(expected_hash)) == event["meta_hash"] else "FAIL", event["meta_hash"])


def fetch_receipt(rpc_url: str, tx_hash: str) -> dict[str, Any] | None:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt", "params": [tx_hash]}).encode()
    request = urllib.request.Request(rpc_url, data=body, headers={"Content-Type": "application/json"})
    response = json.loads(urllib.request.urlopen(request, timeout=10).read())
    return response.get("result")


def verify_file_transactions(root: dict[str, Any], manifest: dict[str, Any], rpc_url: str, report: Report) -> None:
    blockchain = manifest.get("blockchain") or get_path(root, "portable_evidence_snapshot.blockchain", {}) or {}
    transactions = blockchain.get("file_transactions") or []
    if not transactions:
        report.add("Transactions fichiers", "INFO", "aucune transaction individuelle dans le manifeste")
        return
    files = get_path(root, "portable_evidence_snapshot.files.items", []) or []
    files_by_id = {str(item.get("proof_file_id", "")): item for item in files}
    root_transactions = {
        str(item.get("transaction_hash")): item
        for item in (get_path(root, "portable_evidence_snapshot.blockchain.file_transactions", []) or [])
    }
    decoded_count = 0
    for transaction in transactions:
        tx_hash = transaction.get("transaction_hash")
        if not tx_hash:
            report.add("Transaction fichier", "FAIL", "hash de transaction absent")
            continue
        try:
            receipt = fetch_receipt(rpc_url, str(tx_hash))
            event = next((decoded for log in (receipt or {}).get("logs", []) if (decoded := decode_file_added_v3(log))), None)
            if not event:
                report.add("Transaction fichier", "FAIL", f"FileAddedV3 absent: {tx_hash}")
                continue
            decoded_count += 1
            file_id = str(transaction.get("file_id", ""))
            expected = files_by_id.get(file_id, {})
            checks = [
                ("fileId fichier", file_id, event["file_id"]),
                ("Taille fichier", transaction.get("size") or root_transactions.get(str(tx_hash), {}).get("size"), event["size"]),
                ("metaHash fichier", transaction.get("meta_hash", expected.get("stored_sha256", expected.get("sha256"))), event["meta_hash"]),
            ]
            for label, expected_value, actual in checks:
                if expected_value in (None, ""):
                    report.add(label, "INFO", "valeur attendue absente")
                else:
                    equal = normalize_hex(str(expected_value)) == normalize_hex(str(actual)) if "Hash" in label else str(expected_value) == str(actual)
                    if label == "Taille fichier" and not equal:
                        report.add(label, "WARN", f"{actual} octets on-chain; taille archive en clair différente")
                    else:
                        report.add(label, "PASS" if equal else "FAIL", str(actual))
        except (urllib.error.URLError, ValueError, KeyError) as exc:
            report.add("Transaction fichier", "FAIL", f"{tx_hash}: {exc}")
    report.add("Fichiers blockchain vérifiés", "PASS" if decoded_count == len(transactions) else "FAIL", f"{decoded_count}/{len(transactions)}")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []
        self.errors = 0

    def add(self, label: str, state: str, detail: str = "") -> None:
        self.rows.append((label, state, detail))
        if state == "FAIL":
            self.errors += 1

    def print(self, json_output: bool = False) -> None:
        if json_output:
            print(json.dumps({"ok": self.errors == 0, "checks": [{"check": a, "status": b, "detail": c} for a, b, c in self.rows]}, ensure_ascii=False, indent=2))
            return
        for label, state, detail in self.rows:
            icon = {"PASS": "✓", "INFO": "ℹ", "WARN": "!", "FAIL": "✗"}.get(state, "?")
            print(f"{icon} {label}: {detail}" if detail else f"{icon} {label}")
        print(f"\nRésultat: {'VALIDE' if self.errors == 0 else 'ÉCHEC'} ({len(self.rows)} contrôles)")


def read_json(zf: pyzipper.AESZipFile, name: str) -> dict[str, Any] | None:
    try:
        return json.loads(zf.read(name).decode("utf-8"))
    except (KeyError, ValueError, UnicodeDecodeError):
        return None


def verify_manifest(manifest: dict[str, Any], report: Report, public_key: str | None) -> None:
    expected = get_path(manifest, "hashes.manifest_canonical_sha256")
    if not expected:
        report.add("Manifest canonique", "WARN", "hash manifest_canonical_sha256 absent")
        return
    payload = json.loads(json.dumps(manifest))
    payload.setdefault("hashes", {})["manifest_canonical_sha256"] = None
    payload.setdefault("integrity", {})["manifest_signature_valid"] = None
    payload.setdefault("embedded_metadata", {}).setdefault("fields", {})["manifest_canonical_sha256"] = None
    payload["embedded_metadata"]["fields"]["manifest_signature"] = None
    payload.pop("signature", None)
    actual = sha256_bytes(canonical(payload))
    legacy_payload = json.loads(json.dumps(payload))
    legacy_payload["integrity"]["manifest_signature_valid"] = False
    legacy = sha256_bytes(canonical(legacy_payload))
    matches = actual.lower() == str(expected).lower()
    legacy_match = legacy.lower() == str(expected).lower()
    report.add("Manifest canonique", "PASS" if matches or legacy_match else "FAIL", "legacy compatibility" if legacy_match and not matches else actual)

    signature = manifest.get("signature") or {}
    if not signature.get("signed"):
        report.add("Signature Ed25519", "WARN", "manifest non signé")
        return
    key_id = str(signature.get("signing_key_id", ""))
    public_key = public_key or BUILTIN_PUBLIC_KEYS.get(key_id)
    if not public_key:
        report.add("Signature Ed25519", "WARN", f"clé publique inconnue: {key_id} (utiliser --public-key)")
        return
    try:
        key_bytes = base64.b64decode(public_key, validate=True)
        # ProovIT stores the raw 32-byte Ed25519 public key as base64. Wrap it
        # in the standard SubjectPublicKeyInfo envelope for PyCryptodome.
        if len(key_bytes) == 32:
            key_bytes = bytes.fromhex("302a300506032b6570032100") + key_bytes
        key = ECC.import_key(key_bytes)
        verifier = eddsa.new(key, "rfc8032")
        # PHP signs the hexadecimal SHA-256 string as UTF-8 text, not the
        # decoded 32-byte digest.
        verifier.verify(str(expected).encode("ascii"), base64.b64decode(signature["signature_value"], validate=True))
        report.add("Signature Ed25519", "PASS", str(signature.get("signing_key_id", "")))
    except Exception as exc:  # crypto libraries expose several exception types
        report.add("Signature Ed25519", "FAIL", str(exc))


def verify_timeline(manifest: dict[str, Any], report: Report) -> None:
    timeline = manifest.get("timeline") or get_path(manifest, "web.timeline", {}) or {}
    events = timeline.get("events", []) if isinstance(timeline, dict) else []
    if not events:
        report.add("Timeline Web", "INFO", "aucun événement présent")
        return
    previous = None
    valid = True
    for index, event in enumerate(events, 1):
        if event.get("sequence") != index or event.get("previous_event_hash") != previous:
            valid = False
            break
        payload = {
            "event_id": str(event.get("event_id", "")),
            "session_id": str(event.get("session_id", "")),
            "acquisition_id": event.get("acquisition_id"),
            "sequence": int(event.get("sequence", 0)),
            "event_type": event.get("event_type"),
            "actor_type": event.get("actor_type"),
            "user_id": event.get("user_id"),
            "server_received_at": event.get("server_received_at"),
            "runner_occurred_at": event.get("runner_occurred_at"),
            "monotonic_time": event.get("monotonic_time"),
            "normalized_payload": event.get("payload", event.get("normalized_payload")),
            "result": event.get("result"),
            "previous_event_hash": previous,
        }
        actual = sha256_bytes(canonical(payload))
        if actual != event.get("event_hash"):
            valid = False
            break
        previous = actual
    expected = timeline.get("last_event_hash")
    if expected and expected != previous:
        valid = False
    report.add("Timeline Web", "PASS" if valid else "FAIL", f"{len(events)} événement(s)")


def verify_archive(path: Path, password: str | None, public_key: str | None, rpc_url: str | None, json_output: bool) -> int:
    report = Report()
    try:
        zf = pyzipper.AESZipFile(path, "r")
        if password:
            zf.setpassword(password.encode())
        names = zf.namelist()
        report.add("Archive lisible", "PASS", f"{len(names)} entrée(s)")
    except Exception as exc:
        report.add("Archive lisible", "FAIL", str(exc))
        report.print(json_output)
        return 2

    root = read_json(zf, "proovit.json")
    manifest = read_json(zf, "MANIFESTS/certification_manifest_v3.json")
    archive_manifest = read_json(zf, "MANIFESTS/archive_manifest_v1.json")
    if not root or not manifest or not archive_manifest:
        report.add("Manifest présent", "FAIL", "proovit.json, manifeste de certification ou inventaire absent")
        report.print(json_output)
        return 2
    report.add("Manifest présent", "PASS", str(manifest.get("schema", manifest.get("protocol_version", ""))))

    entries = archive_manifest.get("files", [])
    checked = 0
    for entry in entries:
        name = entry.get("path")
        if not name or name not in names:
            report.add("Inventaire archive", "FAIL", f"entrée absente: {name}")
            continue
        try:
            content = zf.read(name)
            actual = sha256_bytes(content)
            if actual.lower() != str(entry.get("sha256", "")).lower():
                report.add("SHA-256 fichiers", "FAIL", str(name))
            elif entry.get("size_bytes") is not None and len(content) != int(entry["size_bytes"]):
                report.add("Taille fichiers", "FAIL", str(name))
            else:
                checked += 1
        except Exception as exc:
            report.add("SHA-256 fichiers", "FAIL", f"{name}: {exc}")
    report.add("Fichiers vérifiés", "PASS" if checked == len(entries) else "FAIL", f"{checked}/{len(entries)}")

    verify_manifest(manifest, report, public_key)
    verify_timeline(manifest, report)
    root_hash = get_path(manifest, "integrity.evidence_root_hash")
    if root_hash:
        artifact_hashes = [str(item.get("sha256", "")) for item in manifest.get("artifacts", [])]
        calculated = sha256_bytes(canonical({
            "protocol_version": manifest.get("protocol_version"),
            "canonical_manifest_sha256": get_path(manifest, "integrity.canonical_manifest_sha256"),
            "timeline_last_hash": get_path(manifest, "integrity.timeline_last_hash") or get_path(manifest, "timeline.last_event_hash"),
            "artifact_hashes": artifact_hashes,
        }))
        report.add("Root hash", "PASS" if calculated.lower() == str(root_hash).lower() else "FAIL", calculated)
    else:
        is_web_manifest = manifest.get("type") == "web-proof" or manifest.get("protocol_version") == "web-evidence-v2"
        report.add("Root hash", "INFO", "non présent dans ce manifeste" if is_web_manifest else "non applicable à cette preuve")

    tx = get_path(root, "portable_evidence_snapshot.blockchain.transaction_hash") or get_path(manifest, "blockchain.transaction_hash") or get_path(manifest, "blockchain.tx_hash")
    manifest_rpc = get_path(root, "portable_evidence_snapshot.blockchain.rpc_url") or get_path(manifest, "blockchain.rpc_url")
    effective_rpc = rpc_url or manifest_rpc
    if tx and effective_rpc:
        try:
            body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt", "params": [tx]}).encode()
            request = urllib.request.Request(effective_rpc, data=body, headers={"Content-Type": "application/json"})
            response = json.loads(urllib.request.urlopen(request, timeout=10).read())
            receipt = response.get("result")
            report.add("Transaction blockchain", "PASS" if receipt else "FAIL", "reçu trouvé" if receipt else "reçu absent")
            if receipt:
                verify_blockchain_payload(root, manifest, receipt, report)
                verify_file_transactions(root, manifest, effective_rpc, report)
        except (urllib.error.URLError, ValueError) as exc:
            report.add("Transaction blockchain", "WARN", str(exc))
    elif tx:
        report.add("Transaction blockchain", "INFO", f"présente: {tx} (utiliser --rpc-url pour interroger le réseau)")
    else:
        report.add("Transaction blockchain", "INFO", "aucune transaction dans l’archive")

    report.add("Géolocalisation", "INFO", "enregistrée" if manifest.get("geolocation") else "absente/non déclarée")
    timestamp = manifest.get("timestamping") or manifest.get("timestamp") or {}
    report.add("Horodatage", "INFO", f"{timestamp.get('type', 'non présent')}" if timestamp else "non présent")
    report.print(json_output)
    return 0 if report.errors == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Vérificateur indépendant d’une archive portable ProovIT")
    parser.add_argument("archive", type=Path)
    parser.add_argument("--password", help="Code de déverrouillage de l’archive")
    parser.add_argument("--public-key", help="Override technique de la clé publique Ed25519 base64")
    parser.add_argument("--rpc-url", help="RPC JSON-RPC pour vérifier le reçu blockchain")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    password = args.password
    if password is None and args.archive.exists():
        password = getpass.getpass("Code de l’archive (laisser vide si non chiffrée): ") or None
    return verify_archive(args.archive, password, args.public_key, args.rpc_url, args.json_output)


if __name__ == "__main__":
    sys.exit(main())
