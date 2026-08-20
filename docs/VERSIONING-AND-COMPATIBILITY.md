# Versioning and Compatibility

The archive format, certification manifest, Web evidence protocol and blockchain event/API versions are separate versioned surfaces.

- `archive_manifest_v1` identifies the ZIP inventory format.
- `proovit.manifest.v3` identifies the certification manifest format.
- `proovit.portable_evidence_snapshot.v2` identifies the portable snapshot.
- `ProofStoredV3` and `FileAddedV3` identify the current contract events.
- `signing_key_id` identifies the signing-key generation.

The verifier supports known historical manifest canonicalization through an explicit legacy compatibility path. It must never silently reinterpret an unknown schema as current. Missing fields are reported as unavailable or not applicable.

Key rotation must add a new public key identifier while retaining retired public keys so historical signatures remain verifiable. Private signing material must never be committed to this repository.
