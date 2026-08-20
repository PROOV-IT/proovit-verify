# Synthetic test vectors

These vectors are synthetic and contain no user evidence. They cover canonical
JSON, Manifest V3 hashing, Ed25519 signing, Web timeline hashes, the evidence
root, and the blockchain file root.

`scripts/generate_test_vectors.py` is the generator of record. Run it from the
repository root, then run `scripts/validate_docs.py`; expected output files
are generated artifacts and should not be edited by hand. A compatible
implementation can reproduce the same outputs from the algorithms in the
specifications without using ProovIT infrastructure.

The vector files are listed in [`docs/test-vectors/README.md`](../test-vectors/README.md).
