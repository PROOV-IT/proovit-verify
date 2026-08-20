# Public signature key registry

The verifier uses raw Ed25519 public keys encoded as base64. The SHA-256 fingerprint below is calculated over the decoded 32-byte public key and is shown in lower-case hexadecimal.

| Key ID | Algorithm | Purpose | Environment | Public key (base64) | SHA-256 fingerprint | Valid from | Valid until | Status |
|---|---|---|---|---|---|---|---|---|
| `proovit-ed25519-staging-2026-01` | Ed25519 | Certification manifest signatures | Staging | `yHmzVtLg40wUkii0EuQYNdZpRbnp4giWb9nXl0sr9WI=` | `674dc043ba3c69174cceec2e41baa74cf211648b4b91ddd47e2e93949c43cd57` | 2026-01-01 | — | active |
| `proovit-ed25519-prod-2026-01` | Ed25519 | Certification manifest signatures | Production | `4gB8kv+H303RoTr3huskF+HTQh/0WptL+2DY3OPYQlc=` | `dea031726ea62077f2bbd41d9d645e3cc58420b15374d7a7b45a528637352e9e` | 2026-01-01 | — | active |

## Rotation policy

Key rotation publishes a new key ID and keeps retired keys in this registry so historical manifests remain verifiable. Private keys MUST never be committed. A key is revoked only when its private material or authorization is known to be compromised; revocation status does not rewrite historical signatures.

The verifier’s built-in registry and this document MUST be updated together and published in the same release.
