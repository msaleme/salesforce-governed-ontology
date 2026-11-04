# Validation and evidence boundaries

## Reproducible local checks

```sh
python3 -m unittest -v test_demo.py
python3 scripts/verify.py
git diff --check
```

The verification script exits nonzero on a failed unit control, changed example output, or broken repository-relative Markdown file link. CI runs the same script on Python 3.10 and 3.12. CI results must be read from the actual workflow run; this document is not a predeclared passing result.

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
