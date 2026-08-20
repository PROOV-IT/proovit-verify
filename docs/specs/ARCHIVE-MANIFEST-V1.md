# Portable archive and `archive_manifest_v1`

## Scope

This specification defines the ZIP inventory used by `proovit-verify`. It is distinct from the signed certification manifest `proovit.manifest.v3`.

## Archive layout

```text
proof.zip
├── proovit.json
├── verification.html
├── MANIFESTS/
│   ├── archive_manifest_v1.json
│   └── certification_manifest_v3.json
├── FILES/                 # original and derived evidence files
├── METADATA/              # portable metadata and blockchain references
└── CERTIFICATES/          # optional PDF and timestamp artifacts
```

The producer may add documented entries. The verifier requires `proovit.json`, both manifest files and every path referenced by the archive inventory.

## Inventory fields

`archive_manifest_v1.json` contains a `files` array. Each entry uses `path` (string), `sha256` (lower-case hexadecimal SHA-256) and, when supplied, `size_bytes` (non-negative integer). Optional fields include `role`, `proof_file_id`, `source_retrieval` and `zip_encrypted`.

Paths are relative POSIX paths. They MUST NOT be absolute, contain `..` components or resolve outside the archive. Inventory paths are compared to ZIP entry names exactly.

## Verification

The verifier reads each inventory path, computes SHA-256 over the uncompressed bytes and compares the result and declared size. An encrypted ZIP requires the access code; the code is a decryption credential and is not an authenticity mechanism.

## Original and derived files

An original is the user-file representation whose digest is recorded by the proof. A derived file, such as a preview or certificate, MUST be identified by its role and MUST NOT replace the original digest.

## Compatibility

Additional fields are ignored by older readers. A reader MUST reject an absent required path or a digest/size mismatch. The certification manifest and its signature are verified independently.
