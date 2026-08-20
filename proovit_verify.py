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
    payload.setdefault("embedded_metadata", {}).setdefault("fields", {})["manifest_canonical_sha256"] = None
    payload["embedded_metadata"]["fields"]["manifest_signature"] = None
    payload.pop("signature", None)
    actual = sha256_bytes(canonical(payload))
    report.add("Manifest canonique", "PASS" if actual.lower() == str(expected).lower() else "FAIL", actual)

    signature = manifest.get("signature") or {}
    if not signature.get("signed"):
        report.add("Signature Ed25519", "WARN", "manifest non signé")
        return
    if not public_key:
        report.add("Signature Ed25519", "WARN", "clé publique absente (utiliser --public-key)")
        return
    try:
        key_bytes = base64.b64decode(public_key, validate=True)
        key = ECC.import_key(key_bytes)
        verifier = eddsa.new(key, "rfc8032")
        verifier.verify(bytes.fromhex(str(expected)), base64.b64decode(signature["signature_value"], validate=True))
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
        report.add("Root hash", "INFO", "non présent dans ce manifeste")

    tx = get_path(root, "portable_evidence_snapshot.blockchain.transaction_hash") or get_path(manifest, "blockchain.transaction_hash") or get_path(manifest, "blockchain.tx_hash")
    if tx and rpc_url:
        try:
            body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt", "params": [tx]}).encode()
            request = urllib.request.Request(rpc_url, data=body, headers={"Content-Type": "application/json"})
            response = json.loads(urllib.request.urlopen(request, timeout=10).read())
            receipt = response.get("result")
            report.add("Transaction blockchain", "PASS" if receipt else "FAIL", "reçu trouvé" if receipt else "reçu absent")
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
    parser.add_argument("--public-key", help="Clé publique Ed25519 base64 du manifeste")
    parser.add_argument("--rpc-url", help="RPC JSON-RPC pour vérifier le reçu blockchain")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    password = args.password
    if password is None and args.archive.exists():
        password = getpass.getpass("Code de l’archive (laisser vide si non chiffrée): ") or None
    return verify_archive(args.archive, password, args.public_key, args.rpc_url, args.json_output)


if __name__ == "__main__":
    sys.exit(main())
