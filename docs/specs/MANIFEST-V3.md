# `proovit.manifest.v3`

**Protocol:** certification manifest V3. **Encoding:** JSON, UTF-8.

## Purpose and field groups

The manifest describes the proof, files, integrity values, signature, timestamp, acquisition context and public blockchain references. Producers MAY include additional fields; readers MUST preserve unknown fields while applying the published canonicalization rules.

Common fields are `schema` (`proovit.manifest.v3`), `protocol_version`, `proof`, `files`, `artifacts`, `integrity`, `signature`, `timestamping` and `blockchain`. `hashes.manifest_canonical_sha256` is the canonical manifest digest. File entries normally contain an identifier, role, archive path, `size_bytes` and `sha256`.

## Canonical JSON

The verifier serializes the manifest as follows:

1. Deep-copy the JSON object.
2. Set `hashes.manifest_canonical_sha256` to JSON `null`.
3. Set `integrity.manifest_signature_valid` to JSON `null`.
4. Set `embedded_metadata.fields.manifest_canonical_sha256` and `embedded_metadata.fields.manifest_signature` to JSON `null` when that object exists.
5. Remove the top-level `signature` member.
6. Recursively sort object keys lexicographically by Unicode code point. Preserve array order.
7. Serialize with no insignificant whitespace, using `,` and `:` separators, UTF-8 characters unescaped (`ensure_ascii=false`), JSON `true`, `false` and `null`, and finite JSON numbers.

The canonical byte sequence is the UTF-8 encoding of that serialization. The exact operation is covered by `docs/test-vectors/canonical-input.json` and `canonical-output.json`.

## Digest and signature

The SHA-256 digest is rendered as lower-case hexadecimal. The Ed25519 signature input is the ASCII/UTF-8 bytes of that hexadecimal string, not the raw 32-byte digest. `signature.signature_value` is base64. `signature.signing_key_id` selects a public key in [PUBLIC-KEYS.md](PUBLIC-KEYS.md).

## Blockchain fields

`blockchain` MAY contain `chain_id`, `contract_address`, `rpc_url`, `proof_chain_id`, `transaction_hash`, `data_hash`, `files_root`, `file_count` and `file_transactions`. A file transaction contains `file_id`, `transaction_hash`, `file_index`, `size`, `size_basis`, `cid` and `meta_hash` when available. Current file sizes use `size_basis: plaintext_user_file`; a CID may identify encrypted storage.

## Verification order

Read and authenticate the archive, verify inventory entries, canonicalize and hash the manifest, verify Ed25519, verify the timeline when present, then perform blockchain checks when references and a public RPC are available. Missing optional data is reported as unavailable or not applicable; it is not synthesized.

## Reference vectors

See [the test vectors](../test-vectors/) and [the protocol overview](PROOVIT-EVIDENCE-PROTOCOL.md).
