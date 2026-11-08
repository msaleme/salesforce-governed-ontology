# Validation and evidence boundaries

## Reproducible local checks

```sh
python3 -m unittest discover -v
python3 scripts/verify.py
git diff --check
```

The verification script exits nonzero on a failed unit control, invalid registry, unexpected tour outcome, drifted ontology diagram, changed example output, or broken repository-relative Markdown file link. CI runs the same script on Python 3.10 and 3.12. CI results must be read from the actual workflow run; this document is not a predeclared passing result.

## Existing behavioral controls

The 15 test methods in [test_demo.py](../test_demo.py) cover:

1. Unique concept IDs and relationship target/source references.
2. Ambiguous revenue clarification.
3. Distinct metric definitions and read operations.
4. Missing fixture scope, including an ambiguous request.
5. Unknown concepts.
6. Expired definition.
7. Draft and revoked definitions.
8. Missing approval reference.
9. Write and unknown operation rejection.
10. Explained synthetic bridge.
11. Difference without inferred cause.
12. Currency, period, operator, and contract mismatches.
13. Invalid bridge amount.
14. Noninteger amount rejection.
15. Missing source reference.

These are local behavior tests, not adversarial proof of a vendor authorization boundary. Multiple scenarios within a method do not count as separately reported test methods.

## Not established

No test here establishes live Salesforce record permissions, Informatica API access, MuleSoft identity propagation, Agentforce support, tenant isolation, cache safety, authenticated approvals, deployment readiness, or correct accounting treatment. Model completeness and all malformed-input cases are not exhaustively validated.

The full [sandbox acceptance packet](PLATFORM-FIT-REVIEW.md) remains unexecuted. Preserve that distinction in demos, PRs, and executive summaries.

## Registry and CLI regression controls

[test_validation.py](../test_validation.py) adds mutation checks for malformed collections, duplicate identities/relationships, dangling graph references, missing metric fields, invalid/reversed dates, missing approval/lineage, and swapped metric/source/operation bindings. It also verifies inclusive validity boundaries, deterministic scenario outcomes without model mutation, CLI execution outside the checkout directory, and nonzero exit codes for invalid input.

The generated graph in [the ontology map](ONTOLOGY-MAP.md) must match the registry relationships. The original demo output remains backward-compatible. The CLI is tested through subprocesses, not only direct function calls. The diagram text is checked; rendered GitHub appearance is not part of CI.

## Planner boundaries and decision receipt

[test_boundaries.py](../test_boundaries.py) exercises malformed request containers, missing/nested metric fields, invalid unselected records, duplicate identities, availability-filtered clarification and reconciliation input types. `resolve` validates the whole registry before returning plans or clarification choices, while preserving safely identifiable specific refusal statuses.

[test_evaluate.py](../test_evaluate.py) verifies the [fixed decision contract](EVALUATION.md), including positive controls, deliberately wrong expectations and checked-in receipt parity. These authored cases are not held out and do not measure vendor or model accuracy.
