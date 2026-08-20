# Web Evidence V2

## 1. Scope

This document covers the Web timeline checks currently implemented by the independent verifier. It is not a complete browser-forensics specification.

## 2. Provenance levels

Fields in a Web archive should be interpreted as `DECLARED_BY_USER`, `OBSERVED_BY_BROWSER`, `OBSERVED_BY_RUNNER`, `OBSERVED_BY_BACKEND`, `DERIVED_BY_PROOVIT`, or `EXTERNAL_ATTESTATION` when the producer records that provenance. A recorded provenance label describes origin; it does not automatically make the value tamper-proof.

## 3. Session and navigation

The archive may contain requested and final URLs, browser/runtime information, network context, resource references and screenshots. The verifier does not independently replay the source Web page or prove that a remote page was truthful at the time of capture.

A Web evidence archive may contain an event timeline: session opening, navigation, capture, state freeze and finalization. Each event contains a sequence number, a type, normalized content and the hash of the preceding event.

The verifier checks sequence continuity, verifies that the first event has no predecessor, recomputes each canonical event hash and compares the final hash with the announced value.

An archive without a Web timeline is not classified as corrupt by that fact alone: it may represent multimedia evidence or another evidence family. The result reports that the Web control is not applicable.

## 4. Exact timeline hash input

The current verifier builds the canonical event payload with these keys: `event_id`, `session_id`, `acquisition_id`, `sequence`, `event_type`, `actor_type`, `user_id`, `server_received_at`, `runner_occurred_at`, `monotonic_time`, `normalized_payload` (from `payload` or `normalized_payload`), `result`, and `previous_event_hash`. It serializes that object using the verifier’s canonical JSON routine and hashes the UTF-8 bytes with SHA-256.

The first event must have sequence `1` and no previous hash. Each following event must reference the preceding computed hash. `last_event_hash`, when present, must equal the final computed hash.

## 5. Evidence root

For manifests that contain `integrity.evidence_root_hash`, the current verifier hashes the canonical object containing `protocol_version`, `canonical_manifest_sha256`, `timeline_last_hash` and `artifact_hashes`. This check is only available when those source fields are present. It is not inferred for a non-Web proof.

## 6. Known limits

The current verifier does not independently validate all browser isolation, DNS, TLS, redirect, HTML, DOM or screenshot acquisition claims. Those claims remain dependent on the producer’s recorded observations and the platform implementation.
