# Multimedia Evidence V1

## Scope

This specification covers image, video, audio, document and screen-capture files represented in a portable PROOV-IT archive. It describes the evidence representation and the controls exposed by the verifier; it does not define the truth of the recorded scene or the complete acquisition implementation.

## File model

Each original user file has a stable file identifier, a user-file SHA-256 digest and a plaintext byte size. A derived artifact, including a preview, thumbnail, normalized media file or PDF, is a separate archive entry with its own digest and role. A producer MAY record an original-to-derived relationship in the file metadata.

## Acquisition and preservation

The producer may record client-side and server-side digests, metadata extraction, device context, geolocation and capture timestamps. The portable archive preserves the representation selected for verification and inventories its bytes through `archive_manifest_v1`.

## Blockchain representation

`FileAddedV3` records `fileId`, `cid`, `size` and `metaHash`. Current protocol versions define `size` and `metaHash` in the user-file domain (`size_basis: plaintext_user_file`). The CID may point to an encrypted IPFS representation and is therefore a separate value.

## Media families

Images, video, audio, documents and screen recordings are handled as byte-addressed files. Format-specific metadata may be recorded as context or derived information. The verifier checks the archived bytes and declared digests; it does not re-interpret pixels, audio meaning, document authorship or scene content.

## Signatures, timestamps and context

An embedded signature file, RFC3161 token, geolocation value or device record is an associated artifact or context value. Its provenance and verification status are recorded separately from the file digest.

## Portable and independent verification

The archive inventory, certification manifest, signature and optional blockchain references are checked independently. See [Archive Manifest V1](ARCHIVE-MANIFEST-V1.md), [Manifest V3](MANIFEST-V3.md) and [Blockchain Verification](BLOCKCHAIN-VERIFICATION.md).
