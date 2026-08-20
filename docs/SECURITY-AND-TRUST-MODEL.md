# Security and Trust Model

## Independently verifiable

The verifier can independently recalculate archive file SHA-256 values, the V3 canonical manifest hash, the Ed25519 signature check, the implemented Web timeline hash chain, blockchain receipt status, `ProofStoredV3` and `FileAddedV3` fields, and the documented Merkle calculation when the required leaves are present.

## Still dependent on platform observation

The following are recorded observations or declarations: the browser runtime and isolation, the fact that the backend received a request, account identity, client-provided GPS, device identifiers, client timestamps and the truthfulness of the captured source.

## External attestations

The blockchain receipt is an external public-network observation. RPC availability and endpoint correctness remain operational assumptions. An RFC3161 token marked non-qualified is not represented as a qualified eIDAS timestamp.

## Non-claims

The format is not a proof of absolute truth, authorship, unspoofable GPS, or legal qualification. The verifier does not replace an expert examination of the circumstances of acquisition and preservation.

## Malicious input

Implementations should reject malformed JSON, invalid UTF-8, invalid signatures, path traversal, oversized decompression and unsafe HTML rendering. RPC responses and archive metadata must be treated as untrusted data.
