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

Accepts a metric identifier, a container of fixture scope strings, an ISO date, and an optional model dictionary. Returns a dictionary. The default model is loaded from the adjacent JSON file at import time.

| Status | Condition |
| --- | --- |
| `denied` | Required fixture scope is absent |
| `clarification_required` | The generic `revenue` identifier is requested |
| `unsupported_concept` | No matching metric exists |
| `definition_unavailable` | Definition is not approved, lacks approval reference, or is outside validity dates |
| `unsupported_action` | Operation is outside the fixed allowlist or is not read-only |
| `read_plan_only` | Fixture checks allow returning a definition, source, version, and operation |

Checks are ordered: the initial finance scope check occurs before concept resolution. Read plans do not execute anything. The resolver does not enforce general model schema validity, immutable versions, authenticity, metadata freshness, or operation-to-source consistency. Malformed trusted fixture input can raise Python exceptions; it is not a public request-validation API.

### `fixtures()`

Returns fresh bookings, recognized-revenue, and explanation-bridge dictionaries. All share operator, contract, period, and currency. Values are deterministic and synthetic.

### `reconcile(booked, recognized, bridge=None)`

Expects dictionaries with matching nonempty dimensions, approved fixture source strings, and integer `amount_minor` values. Booleans and floating-point values are rejected as amounts. The function compares a pre-aligned cohort; it does not align arbitrary accounting ledgers.

| Status | Meaning |
| --- | --- |
| `incompatible_dimensions` | Operator, contract, period, or currency does not match or is absent |
| `missing_or_wrong_source` | A value does not identify the expected fixture source |
| `invalid_amount` | Either amount is not an integer |
| `difference_only` | Valid subtraction without an explanation bridge |
| `invalid_bridge` | Supplied bridge lacks matching dimensions, amount, source, or reason |
| `explained_by_fixture_bridge` | Supplied fixture bridge matches the difference |

Bridge source and reason are checked for presence, not authenticity. No cryptographic provenance or financial verification is implied.

### `demo()`

Returns the combined scenario dictionary printed as JSON by `python3 demo.py`. [Example output](../examples/demo-output.json) is checked for semantic JSON equality by the verification script.
