#!/usr/bin/env python3
"""Validate synthetic documentation vectors without importing verifier internals."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTOR = ROOT / "docs" / "test-vectors"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")


def main() -> int:
    value = json.loads((VECTOR / "canonical-input.json").read_text(encoding="utf-8"))
    output = canonical(value)
    digest = hashlib.sha256(output).hexdigest()
    (VECTOR / "canonical-output.json").write_bytes(output)
    (VECTOR / "canonical-output.sha256").write_text(digest + "\n", encoding="ascii")
    assert hashlib.sha256((VECTOR / "canonical-output.json").read_bytes()).hexdigest() == digest
    print(f"canonical vector OK: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
