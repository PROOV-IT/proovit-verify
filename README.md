# ProovIT Verify

Current release: `v0.2.12`.

`proovit-verify` is an open-source verifier for ProovIT portable evidence archives. It performs the local checks without the ProovIT API and can query public blockchain data when the archive provides a public RPC reference.

## Quick start

```bash
proovit-verify preuve.zip --password 'CODE_D_ACCES'
proovit-verify preuve.zip --password 'CODE_D_ACCES' --json > rapport.json
```

The release page provides binaries for Linux x64, Windows x86/x64/ARM64 and macOS Intel/Apple Silicon. On Linux and macOS, extract the archive and run the executable from the extracted directory.

## Checks performed

The verifier checks archive readability, inventory entries, SHA-256 digests, the V3 canonical manifest, its Ed25519 signature, the Web timeline when present, and blockchain receipts and file transactions when their references and a public RPC are available. `INFO` and `WARN` results identify unavailable, non-applicable or contextual checks; they are not silently converted into a positive assertion.

## Public documentation

Start with the [documentation by audience](docs/README.md). The [French verification guide](docs/fr/GUIDE-VERIFICATION.md) is intended for third parties, legal professionals and experts. Developers can use the [protocol specification](docs/specs/PROOVIT-EVIDENCE-PROTOCOL.md), [test vectors](docs/test-vectors/) and related specifications in `docs/specs/`.

## Build from source

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt pyinstaller
.venv/bin/pyinstaller --clean --onefile --name proovit-verify proovit_verify.py
```

Build Windows executables on Windows and macOS executables on macOS or use the published GitHub Actions workflow. The source remains available for audit and independent reimplementation.

## Scope

The tool establishes reproducible technical relationships between the archive, its files, manifests, signature, timeline and public blockchain references. It does not determine legal admissibility, authorship, the truth of captured content or the weight of evidence in a case.
