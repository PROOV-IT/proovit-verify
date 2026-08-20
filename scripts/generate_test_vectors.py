#!/usr/bin/env python3
"""Regenerate deterministic public protocol vectors without importing the CLI."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

from Cryptodome.Hash import keccak
from Cryptodome.PublicKey import ECC
from Cryptodome.Signature import eddsa

ROOT = Path(__file__).resolve().parents[1] / "docs" / "test-vectors"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def merkle(leaves: list[str]) -> str:
    level = [bytes.fromhex(item.removeprefix("0x")) for item in leaves]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [keccak.new(digest_bits=256, data=level[i] + level[i + 1]).digest() for i in range(0, len(level), 2)]
    return "0x" + (level[0] if level else bytes(32)).hex()


def write_json(name: str, value: object) -> None:
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {"files": [{"path": "FILES/a.txt", "sha256": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb", "size_bytes": 1}], "schema": "proovit.manifest.v3"}
    write_json("manifest-v3-input.json", manifest)
    canonical_bytes = canonical(manifest)
    (ROOT / "manifest-v3-canonical.json").write_bytes(canonical_bytes + b"\n")
    (ROOT / "manifest-v3-sha256.txt").write_text(sha(canonical_bytes) + "\n", encoding="ascii")

    leaves = ["0x" + hashlib.sha256(value).hexdigest() for value in (b"alpha", b"beta", b"gamma")]
    write_json("files-root-input.json", {"leaves": leaves})
    (ROOT / "files-root-expected.txt").write_text(merkle(leaves) + "\n", encoding="ascii")

    event = {"event_id": "evt-1", "session_id": "sess-1", "acquisition_id": None, "sequence": 1, "event_type": "capture", "actor_type": "runner", "user_id": None, "server_received_at": "2026-01-01T00:00:00Z", "runner_occurred_at": None, "monotonic_time": None, "normalized_payload": {"ok": True}, "result": "accepted", "previous_event_hash": None}
    write_json("timeline-events.json", [event])
    event_hash = sha(canonical(event))
    write_json("timeline-expected-event-hashes.json", [event_hash])
    (ROOT / "timeline-expected-final-hash.txt").write_text(event_hash + "\n", encoding="ascii")

    (ROOT / "evidence-root-input.json").write_text(json.dumps({"protocol_version": "web-evidence-v2", "canonical_manifest_sha256": "a" * 64, "timeline_last_hash": event_hash, "artifact_hashes": []}, indent=2) + "\n", encoding="utf-8")
    root_input = json.loads((ROOT / "evidence-root-input.json").read_text(encoding="utf-8"))
    (ROOT / "evidence-root-expected.txt").write_text(sha(canonical(root_input)) + "\n", encoding="ascii")

    key = ECC.construct(curve="Ed25519", seed=b"\x01" * 32)
    message = b"proovit-test-message"
    signature = eddsa.new(key, "rfc8032").sign(message)
    (ROOT / "ed25519-message.txt").write_bytes(message + b"\n")
    (ROOT / "ed25519-public-key.txt").write_text(base64.b64encode(key.public_key().export_key(format="raw")).decode() + "\n", encoding="ascii")
    (ROOT / "ed25519-signature.txt").write_text(base64.b64encode(signature).decode() + "\n", encoding="ascii")
    write_json("ed25519-expected.json", {"valid": True, "algorithm": "Ed25519"})


if __name__ == "__main__":
    main()
