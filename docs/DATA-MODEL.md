# Data model and local API

## Vocabulary

The authoritative example is [ontology.json](../ontology.json). Its namespace is `urn:example:sf-governed-og:` and its evidence classification is `synthetic_only`.

| Concept | Meaning |
| --- | --- |
| Account | Business party in a commercial relationship |
| OperatorRole | Time-bounded operation role, distinct from asset ownership |
| Asset | Identified physical operational resource |
| Well | Specialized Asset with a namespaced identifier |
| ProductionObservation | Quantity by well, period, commodity, unit, and basis |
| Contract | Agreement covering counterparties, assets, and obligations |
| RevenueEntry | Monetary entry with accounting and contract context |

Relationships connect Account to OperatorRole, OperatorRole to Asset, Well to Asset, ProductionObservation to Well, Contract to Asset and Account, and RevenueEntry to Contract. The JSON lists relationship types, not instance records. Temporal qualifiers and cardinality are architecture requirements, not implemented constraints in this fixture.

## Metric record

Each fixture metric contains `id`, `label`, `version`, `definition`, `status`, `approval`, `valid_from`, `valid_to`, `grain`, `aggregation`, `unit`, `source_binding`, `lineage`, and `action`.

- `approval`: synthetic steward/reference evidence, not an authenticated approval.
- `valid_from` / `valid_to`: ISO dates, inclusive at both ends.
- `grain`: operator, contract, period, and currency.
- `unit`: currency minor units; USD examples use cents. No currency conversion is implemented.
- `source_binding` / `lineage`: fixture identifiers, not real catalog assets.
- `action`: fixed operation ID, read-only side-effect class, required fixture scope, and local-only implementation label.

`booked_revenue` is an internal identifier for contract bookings, not recognized revenue or a claim that Opportunity Amount is an accounting measure. The approved state means approved **within the synthetic fixture only**.

## Python functions

### `resolve(metric_id, scopes, as_of="2026-11-03", model=None)`

Accepts a metric identifier, a list, tuple, set or frozenset of nonempty fixture scope strings, an ISO date, and an optional model dictionary. Returns a dictionary. The default model is loaded from the adjacent JSON file at import time.

| Status | Condition |
| --- | --- |
| `invalid_request` | Malformed scope container/member, metric ID or evaluation date |
| `invalid_registry` | Supplied registry fails validation without a more specific refusal |
| `denied` | Required fixture scope is absent |
| `clarification_required` | Generic `revenue` requested; choices contain only approved, date-valid metrics |
| `unsupported_concept` | No matching metric exists |
| `definition_unavailable` | Definition is not approved, lacks approval reference, or is outside validity dates |
| `unsupported_action` | Operation is outside the fixed allowlist or is not read-only |
| `binding_mismatch` | Metric, source, and allowed read operation do not match their expected triple |
| `read_plan_only` | Fixture checks allow returning a definition, source, version, and operation |

Checks are ordered: scope shape, missing finance scope, request identity/date, then whole-registry validation. An invalid registry cannot produce a plan or clarification choices, even if the malformed record is not selected. Specific legacy refusals (`definition_unavailable`, `unsupported_action`, `binding_mismatch`) are preserved where safely identifiable; other registry errors return `invalid_registry` without supplied content. Use authoring validation for detailed diagnostics. A valid registry then supports clarification, unknown-concept, lifecycle/date and read-plan decisions. If no approved date-valid choices remain, clarification returns `definition_unavailable`.

`model=None` selects the default fixture. Read plans do not execute anything. These checks do not enforce immutable versions, authenticity, identity or metadata freshness. This is an in-process JSON-shaped fixture API, not a hardened network service with size/rate/depth limits.

### `fixtures()`

Returns fresh bookings, recognized-revenue, and explanation-bridge dictionaries. All share operator, contract, period, and currency. Values are deterministic and synthetic.

### `reconcile(booked, recognized, bridge=None)`

Expects dictionaries with matching nonempty dimensions, approved fixture source strings, and integer `amount_minor` values. Booleans and floating-point values are rejected as amounts. The function compares a pre-aligned cohort; it does not align arbitrary accounting ledgers.

| Status | Meaning |
| --- | --- |
| `invalid_input` | Booked or recognized input is not an object |
| `incompatible_dimensions` | Operator, contract, period, or currency does not match or is absent |
| `missing_or_wrong_source` | A value does not identify the expected fixture source |
| `invalid_amount` | Either amount is not an integer |
| `difference_only` | Valid subtraction without an explanation bridge |
| `invalid_bridge` | Supplied bridge lacks matching dimensions, amount, source, or reason |
| `explained_by_fixture_bridge` | Supplied fixture bridge matches the difference |

Bridge must be an object; source and reason must be nonempty strings, but their authenticity is not checked. No cryptographic provenance or financial verification is implied.

### `demo()`

Returns the combined scenario dictionary printed as JSON by `python3 demo.py`. [Example output](../examples/demo-output.json) is checked for semantic JSON equality by the verification script.

## Registry validation and guided CLI

`python3 explore.py validate [path]` checks the bounded fixture registry with `validate_model(model)` from [validation.py](../validation.py). It returns path-qualified diagnostics and exits 1 for invalid input, 0 for a valid registry. The same validator is now an automatic precondition before any plan or clarification inside `resolve`; authoring validation additionally returns detailed diagnostics.

The validator checks required fields, unique identities/relationships, relationship references, lifecycle states, date intervals, approval fixture fields, grain/unit/aggregation, lineage inclusion, and exact metric/source/operation bindings. Extra fields are allowed. This is neither a general JSON Schema implementation nor a proof of real approval, lineage truth, or complete business semantics.

`python3 explore.py tour` explains eight local scenarios. `tour --json` emits structured results. `scenario NAME` emits one scenario. Unknown commands exit 2. See the [demo guide](RUN-GUIDE.md).
