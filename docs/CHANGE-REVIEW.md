# Review semantic changes before approving a read plan

The registry already carries versions, but a version string alone does not prove that the definition stayed unchanged. [change_review.py](../change_review.py) compares two local registry snapshots and reports affected records without executing reads, changing the registry, or granting approval.

## Run

```sh
python3 change_review.py ontology.json ontology.json
# Compare a separately retained approved baseline with a proposed candidate:
python3 change_review.py /path/to/baseline.json /path/to/candidate.json
```

The first command is a clean positive control. The second requires your own files. Use a reviewed, immutable baseline from source control, not a baseline copied from the candidate. The tool cannot establish baseline authenticity.

## Policy

- Both inputs must pass the bounded [registry validator](../validation.py). Invalid source/action bindings are rejected as `invalid_registry`, not described as a compatible change.
- A changed registry needs a different registry version. A changed existing metric record needs a different metric version too. Even a label-only edit requires a version change under this deliberately strict snapshot policy.
- Version strings are opaque. A changed version is not proof of monotonic progression, semantic-version compatibility, or approval. Reused historical versions require a history store, which is not implemented.
- Added and removed records are explicit. Existing records report changed top-level fields. A label-only change is `descriptive`; a version-only change is `version_only`; all other existing-record changes are `contract_review_required`.
- “Contract review required” conservatively includes potential breaking changes such as changed meaning, validity, lifecycle, approval or bindings. It does **not** assert that every such change breaks consumers. Unknown extension fields also require review.
- Ordering of the concepts, metrics and relationships collections does not change their semantic comparison. Array ordering inside records remains significant. Missing extension fields and explicit null are distinct.
- All changes require human review. A passing comparison is not injected into the resolver and cannot authorize execution. This CLI is opt-in; CI runs its regression tests but does not select an approved baseline or enforce a PR-to-base diff gate.

## Results

| Status | Exit | Meaning |
| --- | --- | --- |
| `unchanged` | 0 | No record-level changes under this policy |
| `review_required` | 1 | Changes detected; necessary version changes present |
| `version_policy_violation` | 1 | Changed content retains a version that should change |
| `invalid_registry` | 1 | At least one snapshot fails registry/finite-JSON validation |
| `invalid_input` | 1 | File read or JSON parsing failed (including duplicate keys) |

Valid comparisons include SHA-256 fingerprints of sorted-key, compact, ASCII-escaped Python JSON encoded as UTF-8. This is explicitly **not RFC 8785/JCS**, a signature, or a byte-for-byte source-file hash. Top-level collection reordering changes the fingerprint while leaving the semantic comparison unchanged. Fingerprints support identifying compared inputs; they do not prove provenance or freshness.

## Evidence

[test_change_review.py](../test_change_review.py) exercises silent definition drift, insufficient registry-only version changes, lifecycle revocation, descriptive edits, additions/removals, collection ordering, unknown extensions, invalid bindings, malformed files, stable mapping serialization and CLI exit behavior. These are synthetic local controls, not vendor integration or independent validation.
