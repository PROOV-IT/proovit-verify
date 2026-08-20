# PROOV-IT Evidence Protocol

## 1. Scope

This document describes the evidence archive and the independent checks currently implemented by `proovit-verify`. It is a technical description of the current implementation, not a legal certification or a claim that every acquisition fact is independently observable.

## 2. Terminology

- **Original**: the user-file representation whose SHA-256 is recorded by the proof.
- **Derived artifact**: a file generated from an original, such as a preview, thumbnail or certificate.
- **Manifest**: a JSON description of proof, files, integrity and external references.
- **Canonical manifest**: the manifest after the self-referential fields are neutralized and object keys are recursively sorted.
- **Archive manifest**: `MANIFESTS/archive_manifest_v1.json`, the ZIP inventory used for file checks.
- **Timeline**: an ordered Web capture event chain, when present.
- **filesRoot**: the Keccak Merkle root submitted to `storeProofV3` for the eligible file hashes.
- **dataHash**: the `bytes32` data hash submitted to `storeProofV3`.
- **Blockchain anchor**: a confirmed transaction receipt and its decoded contract event.
- **Portable archive**: the password-protected ZIP delivered for independent verification.

## 3. Evidence families

The archive may represent a multimedia proof, a Web capture, or both. A missing Web timeline is therefore `NOT_APPLICABLE` for a non-Web proof, not evidence that the archive is corrupt.

## 4. Trust model

File hashes, manifest canonicalization, Ed25519 signatures, timeline chains and public blockchain receipts can be recomputed by a third party. Browser runtime behavior, account identity, client GPS and some device claims remain observations or declarations recorded by ProovIT and are not cryptographically proven by this tool.

## 5. Evidence lifecycle

The current flow is: acquisition or upload, server-side file handling, manifest generation, optional encryption/storage, blockchain anchoring, and portable archive export. Derived artifacts must be treated separately from the original representation.

## 6. Hashing model

File SHA-256 values are hexadecimal strings. Blockchain file `metaHash` is the original-file hash. For current protocol versions, file `size` is `plaintext_user_file`; the IPFS CID may identify an encrypted representation and is not expected to equal the original-file hash.

## 7. Manifests

The signed manifest is `proovit.manifest.v3`. The archive inventory is
`archive_manifest_v1`. Their exact fields and compatibility rules are described
in the linked sub-specifications.

## 8. Signatures

The canonical manifest SHA-256 hexadecimal text is the Ed25519 signing input. The signature value and public keys are base64-encoded. Key selection uses `signing_key_id`.

## 9. Blockchain anchoring

The current contract events are `ProofStoredV3` and `FileAddedV3`. A global proof transaction and file transactions may be separate. Verification requires the relevant transaction hashes and an accessible JSON-RPC endpoint.

## 10. Portable archive

The ZIP is readable with its access code. The access code is not a signature and does not authenticate the issuer.

## 11. Independent verification

The verifier checks only data available in the archive and, for online checks, public RPC responses. It does not call a private ProovIT API.

## 12. Protocol scope and compatibility

Older archives may use an earlier manifest shape or omit individual file transaction hashes. Such fields are reported according to the compatibility rules in `VERSIONING-AND-COMPATIBILITY.md`. A blockchain confirmation is an external technical attestation; it does not by itself establish authorship, the truth of captured content or legal admissibility.

## 13. Versioning and compatibility

Archive and manifest versions are independent. The verifier retains legacy canonical-hash compatibility for known historical manifests. New fields must be additive where possible.

## 14. Security considerations

Consumers should treat ZIP contents, JSON, HTML and RPC responses as untrusted input. Preserve the original archive, record its external SHA-256 and retain the verifier version used.

## 15. References to sub-specifications

- [Archive Manifest V1](ARCHIVE-MANIFEST-V1.md)
- [Manifest V3](MANIFEST-V3.md)
- [Web Evidence V2](WEB-EVIDENCE-V2.md)
- [Multimedia Evidence V1](MULTIMEDIA-EVIDENCE-V1.md)
- [Blockchain Verification](BLOCKCHAIN-VERIFICATION.md)
- [Security and Trust Model](../expert/MODELE-DE-CONFIANCE.md)
- [Versioning and Compatibility](VERSIONING-AND-COMPATIBILITY.md)
