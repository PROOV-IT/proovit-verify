# Web Evidence V2

## 1. Scope and terminology

This document specifies the Web Evidence V2 fields and integrity checks that
are represented in a ProovIT portable archive and consumed by the independent
verifier. It is not a browser-forensics standard and does not independently
replay a remote page.

In this document, **recorded** means present in the archive, **observed** means
attributed by the producer to a browser, runner or backend, **derived** means
calculated during processing, and **verified** means that the independent
verifier successfully performed the applicable comparison.

The protocol identifier is `web-evidence-v2`. A Web timeline is optional for
the archive family; its absence is not an integrity failure for multimedia or
other non-Web evidence.

## 2. Acquisition session and navigation

The producer may record a session identifier, acquisition identifier, requested
URL, final URL, redirects, browser/runtime context, network observations and
an initial session event. These values describe the acquisition context; their
presence does not prove that a third party would observe the same remote page.

The current verifier checks the fields and hashes supplied in the archive. It
does not create a browser context, validate isolation, replay navigation, or
re-resolve the remote URL. URL scheme validation, SSRF protection, redirect
policy, network restrictions and navigation completion are acquisition-side
controls and are not asserted by this offline verifier unless their resulting
records are covered by a published integrity structure.

## 3. Observations and artifacts

A Web archive can contain HTML, a DOM snapshot, viewport or full-page
screenshots, downloaded files, resources, HTTP metadata, response headers, DNS
or TLS observations, timestamps and runtime information. The archive and its
manifest establish which artifacts were actually supplied. File hashes and
inventory entries can be recalculated locally; an observation such as a DNS
answer, TLS property or HTTP header is not independently re-observed by the
verifier.

Downloads are represented as file entries when included by the producer. Their
identity, clear-file size, content hash and relationship to the session are
checked only when the corresponding manifest and/or blockchain metadata is
present. A CID identifies a stored representation and is not a clear-file
SHA-256 value.

### Normative field reference

| Field or artifact | Source | Required | Format | Integrity mechanism | Verification method |
|---|---|---:|---|---|---|
| `requested_url` | acquisition context | conditional | URL string | manifest/signature when included | compare recorded value |
| `final_url` | browser/runner record | conditional | URL string | manifest/timeline when included | compare recorded value |
| redirects | runner record | optional | ordered URL records | artifact/manifest hashes | inspect and hash |
| HTML / DOM | browser/runner | conditional | archive files | SHA-256 and inventory | recompute file hash |
| viewport / full-page screenshot | browser/runner | optional | archive image files | SHA-256 and inventory | recompute file hash |
| HTTP status / headers | runner record | optional | structured metadata | manifest/timeline when included | compare recorded value |
| DNS / TLS | runner record | optional | structured metadata | manifest/timeline when included | compare recorded value |
| resources | runner record | optional | ordered references/files | hashes when included | inspect references and hashes |
| downloads | runner record | optional | file entries | SHA-256, manifest, optional blockchain | recompute and compare |
| timeline | runner/backend | optional for archive family | ordered event array | chained SHA-256 | validate sequence and hashes |
| runtime | runner record | optional | structured metadata | manifest when included | inspect recorded values |
| acquisition timestamps | runner/backend | conditional | recorded timestamp strings | manifest/timeline/signature | inspect exact mechanism |
| `evidence_root_hash` | derived | optional | lowercase SHA-256 hex | manifest/signature | recompute exact root |

“Conditional” means required only when the producer includes that Web feature;
it does not imply that the verifier can reconstruct an omitted observation.

## 4. Timeline integrity

Each event is an object containing `event_id`, `session_id`, `acquisition_id`,
`sequence`, `event_type`, `actor_type`, `user_id`, `server_received_at`,
`runner_occurred_at`, `monotonic_time`, `normalized_payload` (read from
`payload` or `normalized_payload`), `result`, and
`previous_event_hash`. Object keys are canonicalized using the Manifest V3
JSON rules: UTF-8, sorted object keys, preserved array order, no insignificant
whitespace, and JSON escaping as specified by the canonicalization routine.

The event hash is SHA-256 of the UTF-8 canonical JSON bytes of that object,
rendered as lowercase hexadecimal. The first event has sequence `1` and no
predecessor. Every later event must reference the hash of the immediately
preceding computed event. If `last_event_hash` is present, it must equal the
final computed hash. The verifier rejects gaps, reordering, broken predecessor
hashes or a mismatching final value.

## 5. Freeze and finalization

The archive may record events such as capture, freeze and finalization. In the
portable evidence model, these are recorded state transitions; the verifier
checks their ordering and hashes when a timeline is present. This verifier does
not claim that freeze stopped network access, that the browser became
forensically isolated, or that no producer-side process ran afterwards.

Finalization relates the runner output to backend processing: the backend
persists the manifest and artifact references, builds the portable archive,
and may publish blockchain references. The verifier checks the resulting
archive, manifest, signature, timeline and public receipts; it does not inspect
the private runner-to-backend transport.

## 6. Manifest and evidence root

The Web data is carried by the portable archive manifest and its file entries.
Manifest V3 canonicalization, hashing and Ed25519 verification are specified in
[`MANIFEST-V3.md`](MANIFEST-V3.md). The Web protocol version and artifact
references are inputs to that manifest; they are not a second unsigned source
of truth.

When `integrity.evidence_root_hash` is present, the verifier canonicalizes this
object, preserving the listed artifact order:

```json
{
  "protocol_version": "...",
  "canonical_manifest_sha256": "...",
  "timeline_last_hash": "...",
  "artifact_hashes": []
}
```

It hashes the UTF-8 canonical JSON bytes with SHA-256 and compares the
lowercase hexadecimal result with `evidence_root_hash`. Missing source fields
are reported as unavailable; no root is fabricated.

## 7. Verification procedure

Offline checks include archive readability, inventory, artifact SHA-256 values,
manifest canonicalization, manifest signature, timeline continuity and the
evidence root when their inputs are present. Network-dependent checks include
retrieving a referenced blockchain receipt through the supplied RPC and
comparing decoded public commitments. The verifier does not contact the Web
origin, execute archived HTML, or treat an unavailable RPC as a successful
comparison.

## 8. Security considerations and protocol scope

Archives, JSON, HTML, screenshots and RPC responses are untrusted input. A
safe implementation must reject malformed JSON and invalid signatures, avoid
path traversal and excessive decompression, avoid executing archived HTML as
trusted code, and apply suitable request and resource limits. Acquisition
systems must separately handle hostile pages, redirects, SSRF, oversized
resources and secret-bearing fields.

This specification protects reproducible relationships among recorded Web
artifacts, their manifest, timeline and optional public anchors. It does not
establish the truth of a page, authorship, browser isolation, a qualified
timestamp, or legal admissibility.
