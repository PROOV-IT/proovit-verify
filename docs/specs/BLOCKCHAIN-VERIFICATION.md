# ProovIT blockchain verification

This specification describes the current public blockchain checks performed by
`proovit-verify`. It documents verification of references already present in a
portable archive; it does not define a new contract or transaction format.

## What is anchored

The blockchain stores identifiers and cryptographic commitments, not
necessarily the original media. A `ProofStoredV3` event can expose the proof
identifier, `dataHash`, `filesRoot`, file count, public proof metadata and the
submitter. The archive may also reference separate `FileAddedV3` transactions.

The verifier retrieves each referenced receipt through the configured public
RPC, checks the expected network and contract when those references are
available, decodes the event, and compares the decoded values with the archive
snapshot and local file metadata.

## Event formats

The current event signatures are:

```text
ProofStoredV3(bytes32,address,uint64,uint64,uint32,bytes32,bytes32,string,string,string,int64,int64)
FileAddedV3(bytes32,uint256,string,string,uint64,bytes32)
```

For `ProofStoredV3`, the decoded data contains the timestamp, price, file
count, `dataHash`, `filesRoot`, and dynamic proof name, proof identifier and
signer fields, followed by latitude and longitude in E6 form. Topics identify
the proof event and submitter. For `FileAddedV3`, topics identify the proof and
file index; the data contains the file identifier, CID, clear-file size and
`metaHash`.

The verifier compares file identifiers, clear-file sizes and metadata hashes.
The CID identifies the stored representation and is not used as the clear-file
SHA-256 value.

## `filesRoot`

The backend computes `filesRoot` as a Keccak-256 binary Merkle tree over the
eligible file hash leaves converted to `bytes32`. Each pair is concatenated
and hashed; when a level has an odd number of nodes, its final node is
duplicated. An empty tree is represented by a zero `bytes32` value. Leaf order
and normalization must be preserved exactly as supplied by the archive.

The initial proof transaction may have a zero file count when file additions
are anchored in separate transactions. In that case the verifier reports the
number of successfully verified `FileAddedV3` transactions separately; it does
not silently reinterpret the initial event.

## Results and protocol scope

A receipt proves inclusion of a transaction in the queried chain. A successful
comparison proves consistency between the public event and the archive values
that were checked. It does not prove authorship, the truth of captured content,
or legal admissibility. Missing public references produce an unavailable or
non-applicable result rather than an invented comparison.

See [Manifest V3](MANIFEST-V3.md), [Web Evidence V2](WEB-EVIDENCE-V2.md), and
the [test vectors](TEST-VECTORS.md) for related deterministic calculations.
