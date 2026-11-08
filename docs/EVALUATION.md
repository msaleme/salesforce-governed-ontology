# Reproducible decision contract

This is a fixed **synthetic contract evaluation**, not an LLM accuracy study or competitive product benchmark. No external model, vendor runtime, production data or network access is involved.

```sh
python3 evaluate.py
python3 scripts/verify.py
```

[Cases](../examples/decision-cases.json) declare expected outcomes. The [runner](../evaluate.py) executes eight tour scenarios and four boundary scenarios. The checked-in [receipt](../examples/decision-results.json) contains each observed outcome plus SHA-256 hashes of the registry, case list and relevant implementation files. CI checks exact receipt parity. After an intentional implementation or case change, regenerate with `python3 evaluate.py > examples/decision-results.json` and review the diff.

## What it measures

- Clarification instead of silently selecting a meaning for “revenue.”
- Valid read plans as well as missing-scope, expiry and wrong-binding refusals.
- Arithmetic without explanation, matching fixture explanation, and incompatible dimensions.
- Invalid registry, invalid scope container, expired clarification and malformed bridge handling.

The valid-read and valid-explanation controls prevent an implementation that refuses every request from passing. Expected outcomes were authored with the prototype and are not held-out data. Matching them demonstrates regression conformance only. The broader test suite also mutates malformed inputs; its test count is not a dataset size or accuracy score.

## Limits and independent reproduction

The receipt is reproducible, not signed or independently attested. A hash identifies content, not its truth. The fixed date and USD fixture do not validate other periods, currencies, accounting policies or domains. No latency, scale, security-boundary or financial correctness claim follows.

For independent reproduction, record the commit, Python version, command, output, and any counterexample in a repository issue. Use synthetic inputs only. Do not paste credentials, customer data or private org metadata. A useful counterexample states both what the code did and why the expected semantic decision differs.

## Future comparative protocol

Before a platform comparison, fix a shared case corpus, native platform/version and approved mappings. Separate semantic-decision outcomes from query execution, authorization, unsupported features and setup failures. Include positive and abstention controls. Have a domain steward review expected outcomes, hold out cases before implementation, and report every failure and unsupported case. No selected success examples, no synthesized vendor scores, and no apples-to-oranges comparison of an offline plan with an executed query.
