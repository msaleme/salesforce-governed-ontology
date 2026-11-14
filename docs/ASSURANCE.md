# Validation, evaluation and platform fit

[Local checks](#validation-and-evidence-boundaries) · [Decision contract](#reproducible-decision-contract) · [Platform-fit packet](#platform-fit-decision-packet)

Install with `python3 -m pip install -e .` before running the checks.
The [package tests](../tests/test_package.py) cover JSON Schema, custom registries,
full-result BYOD evaluation, malformed files and non-execution of bindings.
[Wheel verification](../scripts/check_wheel.py) builds and installs into a fresh
environment and exercises commands outside the checkout. This check downloads
build/runtime dependencies; the installed commands run offline.

## Validation and evidence boundaries

### Reproducible local checks

```sh
python3 -m unittest discover -v
python3 scripts/verify.py
git diff --check
```

The verification script exits nonzero on a failed unit control, invalid registry, unexpected tour outcome, drifted ontology diagram, changed example output, or broken repository-relative Markdown file link. CI runs the same script on Python 3.10 and 3.12. CI results must be read from the actual workflow run; this document is not a predeclared passing result.

### Existing behavioral controls

The 15 test methods in [tests/test_demo.py](../tests/test_demo.py) cover:

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

### Not established

No test here establishes live Salesforce record permissions, Informatica API access, MuleSoft identity propagation, Agentforce support, tenant isolation, cache safety, authenticated approvals, deployment readiness, or correct accounting treatment. Model completeness and all malformed-input cases are not exhaustively validated.

The full [sandbox acceptance packet](ASSURANCE.md) remains unexecuted. Preserve that distinction in demos, PRs, and executive summaries.

### Registry and CLI regression controls

[tests/test_validation.py](../tests/test_validation.py) adds mutation checks for malformed collections, duplicate identities/relationships, dangling graph references, missing metric fields, invalid/reversed dates, missing approval/lineage, and swapped metric/source/operation bindings. It also verifies inclusive validity boundaries, deterministic scenario outcomes without model mutation, CLI execution outside the checkout directory, and nonzero exit codes for invalid input.

The generated graph in [the ontology map](ONTOLOGY-MAP.md) must match the registry relationships. The original demo output remains backward-compatible. The CLI is tested through subprocesses, not only direct function calls. The diagram text is checked; rendered GitHub appearance is not part of CI.

### Planner boundaries and decision receipt

[tests/test_boundaries.py](../tests/test_boundaries.py) exercises malformed request containers, missing/nested metric fields, invalid unselected records, duplicate identities, availability-filtered clarification and reconciliation input types. `resolve` validates the whole registry before returning plans or clarification choices, while preserving safely identifiable specific refusal statuses.

[tests/test_evaluate.py](../tests/test_evaluate.py) verifies the [fixed decision contract](ASSURANCE.md), including positive controls, deliberately wrong expectations and checked-in receipt parity. These authored cases are not held out and do not measure vendor or model accuracy.

## Reproducible decision contract

This is a fixed **synthetic contract evaluation**, not an LLM accuracy study or competitive product benchmark. No external model, vendor runtime, production data or network access is involved.

```sh
python3 evaluate.py
python3 scripts/verify.py
```

[Cases](../examples/decision-cases.json) declare expected statuses and full result objects. The [runner](../evaluate.py) executes eight tour scenarios and four boundary scenarios. The checked-in [receipt](../examples/decision-results.json) contains each observed result, mismatched field names and SHA-256 hashes of the registry, case list and relevant implementation files. CI checks exact receipt parity. After an intentional implementation or case change, regenerate with `python3 evaluate.py > examples/decision-results.json` and review the diff.

### What it measures

- Clarification instead of silently selecting a meaning for “revenue.”
- Valid read plans as well as missing-scope, expiry and wrong-binding refusals.
- Arithmetic without explanation, matching fixture explanation, and incompatible dimensions.
- Invalid registry, invalid scope container, expired clarification and malformed bridge handling.

The valid-read and valid-explanation controls prevent an implementation that refuses every request from passing. Expected outcomes were authored with the prototype and are not held-out data. Matching them demonstrates regression conformance only. The broader test suite also mutates malformed inputs; its test count is not a dataset size or accuracy score.

### Limits and independent reproduction

The receipt is reproducible, not signed or independently attested. A hash identifies content, not its truth. The fixed date and USD fixture do not validate other periods, currencies, accounting policies or domains. No latency, scale, security-boundary or financial correctness claim follows.

For independent reproduction, record the commit, Python version, command, output, and any counterexample in a repository issue. Use synthetic inputs only. Do not paste credentials, customer data or private org metadata. A useful counterexample states both what the code did and why the expected semantic decision differs.

### Future comparative protocol

Before a platform comparison, fix a shared case corpus, native platform/version and approved mappings. Separate semantic-decision outcomes from query execution, authorization, unsupported features and setup failures. Include positive and abstention controls. Have a domain steward review expected outcomes, hold out cases before implementation, and report every failure and unsupported case. No selected success examples, no synthesized vendor scores, and no apples-to-oranges comparison of an offline plan with an executed query.


### Payload correctness, not just outcome labels

A `difference_only` result with the wrong amount is a failure. A refusal that also discloses a definition is a failure. A result that says `difference_only` but adds an invented explanation is also a failure.

The runner compares the full reviewed expected JSON object with the observed object. Missing and unexpected keys fail; list order matters; JSON scalar types matter (an integer is not a boolean or float). Object key order does not matter. Each failed case reports `mismatch_fields` and includes the actual payload for inspection. The current fixtures are synthetic; do not run this reporting path against private data without a separate sanitization design.

Mutation controls in [tests/test_evaluate.py](../tests/test_evaluate.py) deliberately preserve the correct status while corrupting sources, operations, amounts, explanations, provenance, clarification choices or refusal contents. These prove the evaluator detects those regressions; they do not add independently authored domain cases.

**Changing the contract:** review `expected_result` in the case file against the intended behavior first. Never regenerate expectations from the implementation being tested. Regenerate only the receipt after reviewing the contract and code changes. Exact payload checks intentionally require review for wording or schema changes too. This remains a fixed regression contract, not an extensible external-input benchmark or held-out evaluation.

### Reproduction packet

See the [one-command reproduction guide](RUN-GUIDE.md) and [captured synthetic demonstration](RUN-GUIDE.md). The transcript is regenerated and checked by CI. External reproduction remains unverified.

## Platform-fit decision packet

Internal working draft | 2026-11-03 | Continuation of SF-ONTOLOGY-001

### Decision requested from the internal platform owner

Where should governed business definitions and their approved source/action bindings live within the existing Salesforce architecture?

Recommendation: reuse the existing semantic/data-model foundation wherever it can meet the requirements below; add only missing governance and execution bindings. Do not create the six proposed custom objects merely because they appear in the starter design. This packet specifies evaluation criteria, not verified product capabilities.

### Preserve the ownership model

Salesforce is the proposed control plane for definition identity, approved versions, lifecycle and action bindings. Customer/domain stewards approve business meaning. Informatica contributes catalog and lineage evidence; MuleSoft supplies governed integrations; Agentforce consumes approved context and actions. Source systems retain transaction authority and access controls. “From Salesforce” describes the intended architecture, not a claim that this prototype is an official product or that IP ownership has been determined.

### Reuse-first evaluation

For each requirement, the reviewer records an existing feature/API, edition and entitlement, documentary evidence, sandbox result, and gap. All entries currently remain UNVERIFIED.

1. Stable semantic IDs and relationships: distinguish business concepts from physical tables and fields; preserve scoped customer/domain extensions.
2. Metric semantics: represent grain, period basis, currency, exclusions, aggregation and effective dates without relying on a display label.
3. Governed version lifecycle: retain immutable approved versions, approver identity and revocation; imports and agent suggestions cannot approve themselves.
4. External provenance: bind Informatica asset/version IDs and lineage timestamps to a specific definition version; flag stale or missing evidence.
5. API/action binding: resolve a semantic ID to an allowlisted MuleSoft operation and schema version, not generated URLs or unrestricted queries.
6. Access control: establish identity propagation and intersection of metadata, row, field, API and source restrictions; demonstrate denial as well as success.
7. Agent consumption: return a typed definition/evidence envelope and clarification for ambiguous metrics through a supported Agentforce integration route.
8. Operations: establish limits, retention, audit access, promotion between environments and rollback without reviving revoked definitions.

Decision outcomes:
- **Reuse:** existing capabilities satisfy the requirement with evidence.
- **Extend:** preserve the existing canonical model and add a bounded missing component.
- **Defer:** required authority, entitlement or capability is unavailable.

A second registry is justified only by a documented gap. Avoid separate canonical definitions in the catalog, agent prompt and Salesforce registry.

### First sandbox slice

Question: “What is recognized revenue for this operator and accounting period?”

Start with one metric and one read operation. Keep the two-metric bookings/recognized-revenue reconciliation as the second increment, after finance approves both definitions and the explanation bridge.

Required inputs, none assumed available:
- Designated development org and approved internal artifact location.
- Named platform owner and finance/domain steward.
- One approved metric version with grain, accounting period, currency and exclusions.
- One actual Informatica metadata asset, API contract and permitted read mechanism.
- One actual MuleSoft read operation with request/response schema and source references.
- Two sandbox identities with intentionally different access.
- Synthetic or specifically approved test records; no production data required.

Expected trace:
1. Resolve the request to the approved metric version; clarify an unqualified “revenue” request.
2. Validate parameters, definition state, metadata freshness and authenticated identity.
3. Invoke the fixed read operation with caller identity conveyed through the supported mechanism.
4. Preserve source authorization, handle partial/paginated responses explicitly and attach evidence.
5. Return a result only with the correct definition, scope, currency, period and source receipt.

### Acceptance evidence

Capture sanitized requests/responses, definition and schema versions, timestamps, principal aliases, policy outcomes and source references. Never record tokens.

Required cases:
- Permitted identity gets the expected fixture value and provenance.
- Restricted identity cannot obtain disallowed data or disallowed metadata.
- Ambiguous revenue request produces clarification, not a guessed metric.
- Revoked definition or incompatible binding prevents execution.
- Stale metadata, unavailable source and partial results are visible limitations, not complete answers.
- Repeating a request under the second identity does not reuse the first identity's protected cached result.

These are proposed acceptance cases, not executed tests. The existing 15 local controls establish only synthetic prototype behavior.

### Review disposition template

- Platform owner / review date:
- Existing semantic foundation selected:
- Evidence links and entitlement confirmation:
- Reused capabilities:
- Bounded gaps and extension location:
- Approved sandbox / artifact location:
- Finance steward and approved metric version:
- Informatica asset / MuleSoft operation:
- Identity propagation design:
- Decision: reuse / extend / defer
- Remaining blocker and owner:

### Current disposition

REVIEW READY, NOT PLATFORM VALIDATED. The existing starter is preserved. Repository packaging and public GitHub visibility were authorized on 2026-11-04. No org connection, platform object creation, API execution, or external platform review request was made.
