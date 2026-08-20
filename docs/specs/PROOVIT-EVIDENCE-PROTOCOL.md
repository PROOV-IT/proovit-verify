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

The certification manifest is `proovit.manifest.v3`. The archive inventory is `archive_manifest_v1`. Their exact fields and compatibility rules are described in the linked sub-specifications.

## 8. Signatures

The canonical manifest SHA-256 hexadecimal text is the Ed25519 signing input. The signature value and public keys are base64-encoded. Key selection uses `signing_key_id`.

## 9. Blockchain anchoring

The current contract events are `ProofStoredV3` and `FileAddedV3`. A global proof transaction and file transactions may be separate. Verification requires the relevant transaction hashes and an accessible JSON-RPC endpoint.

## 10. Portable archive

The ZIP is readable with its access code. The access code is not a signature and does not authenticate the issuer.

## 11. Independent verification

The verifier checks only data available in the archive and, for online checks, public RPC responses. It does not call a private ProovIT API.

## 12. Limitations

Older archives may omit global blockchain fields or individual file transaction hashes. A blockchain confirmation does not prove authorship, truth of the captured content, or legal admissibility.

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
- [Security and Trust Model](SECURITY-AND-TRUST-MODEL.md)
- [Versioning and Compatibility](VERSIONING-AND-COMPATIBILITY.md)

Le protocole décrit la relation vérifiable entre une archive ProovIT, ses fichiers, ses manifestes, sa signature et son ancrage blockchain.

1. `archive_manifest_v1` inventorie les entrées de l’archive et leurs SHA-256.
2. Le manifeste de certification est canonique et signé avec Ed25519.
3. Les preuves Web peuvent ajouter une timeline chaînée par hash et un `evidence_root_hash`.
4. L’ancrage `storeProofV3` publie notamment `proofId`, `dataHash`, `filesRoot` et `fileCount` dans l’événement `ProofStoredV3`.
5. `proovit-verify` recalcule les contrôles locaux puis interroge directement le RPC indiqué par l’archive ou fourni par l’utilisateur.

Le logiciel ne déduit pas la recevabilité juridique : il établit des faits techniques reproductibles à partir de l’archive et de données publiques.
