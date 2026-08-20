# Documentation Gap Analysis

| Document | Strength | Gap or ambiguity | Implementation reference |
| --- | --- | --- | --- |
| `PROOVIT-EVIDENCE-PROTOCOL.md` | Entry point and trust boundaries | Some acquisition claims are not independently observable | `proovit_verify.py`, `ProofManifestBuilder.php` |
| `ARCHIVE-MANIFEST-V1.md` | Explains ZIP inventory and SHA-256 checks | Optional/generated entries need fixture coverage | `PortableProofArchiveService.php`, `verify_archive()` |
| `MANIFEST-V3.md` | Describes current fields and signature | PHP number serialization and legacy compatibility require vectors | `canonicalizeV3Manifest()`, `normalizeForCanonicalHash()` |
| `WEB-EVIDENCE-V2.md` | Describes event-chain concept | Full Web producer provenance still needs field-by-field extraction | `verify_timeline()`, Web capture manifest builders |
| `MULTIMEDIA-EVIDENCE-V1.md` | Separates original, derived and encrypted forms | Media-specific producer rules need synthetic fixtures | `ProofManifestBuilder.php`, archive exporter |
| `BLOCKCHAIN-VERIFICATION.md` | Documents current events and RPC check | Contract address and global payload availability vary by archive generation | `BlockchainCodec.php`, `ProofContractClient.php` |
| `PUBLIC-KEYS.md` | Publishes key lookup concept | Validity intervals/fingerprints need an automated registry check | `BUILTIN_PUBLIC_KEYS` |
| `THIRD-PARTY-GUIDE.md` | Explains technical/legal boundaries | Output status vocabulary should be stabilized | `Report.print()` |

## Known discrepancies

Older documentation described blockchain payload decoding as future work. The verifier now decodes `ProofStoredV3` and `FileAddedV3`, but old archives can legitimately lack the fields needed for comparison. The current CLI still prints `INFO`/`WARN` labels rather than the future normalized `NOT_AVAILABLE` vocabulary.

## Deliberately not invented

No normative browser-isolation, DNS, TLS, redirect or media re-encoding rule is specified here unless it is directly represented in the current archive and verifier code. Those areas require a further backend inventory before publication as a stable protocol.
