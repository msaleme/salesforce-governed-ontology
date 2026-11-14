# Data-to-proof readiness check

**Use this to identify the smallest data request, not start another architecture project.** Pick one decision, run one check, send only the reported gaps to the named owners. All current examples are maintainer-authored synthetic evidence, not external validation or real source verification.

## One command, five bounded results

```sh
sgo industry-proof
# Full receipts for reproducibility:
sgo industry-proof --json
# Check a sanitized normalized extract against one fixed contract:
sgo industry-proof --industry energy --input examples/industry-proof/energy-input.json
```

No credentials or dependencies. Exit 0 means the narrow local calculation succeeded (or all bundled examples matched their authored results); 1 means evidence is blocked or an example mismatched; 2 means invalid CLI/JSON. Use `--json` to retain input, mapping and implementation SHA-256 hashes, source references and full results. Hashes identify bytes/normalized inputs; they do not authenticate evidence. Do not feed private records into public receipts.

**Example actionable blocker:** remove `RevenueEntry` from the energy input and the checker returns `missing_object`, owner **Accounting**, action **obtain a sanitized RevenueEntry extract from ERP recognition subledger**. It emits no amount when blocked. Multiple missing objects are reported together, avoiding one-at-a-time requests.

## What to request, and what it proves

Names below are **local logical objects**, not verified Salesforce API names, FHIR resources or vendor-native schema mappings. Every mapped field is explicit in the linked JSON contract; the existing `ontology.json` schema is unchanged. These are fixed, narrow examples, not a general ontology execution engine.

| Decision | Minimum object set | Supported local result | Still not proved |
| --- | --- | --- | --- |
| Energy: bookings vs recognition | Contract, Bookings, RevenueEntry | USD minor-unit difference for aligned contracts | Production/revenue cause, entitlement or ownership |
| Finance: gross report difference | LegalEntity, Position, ReportA, ReportB | Positive gross valuations, same positions and currency | Group consolidation, netting eligibility or FX |
| Healthcare: bounded capacity | Bed, BedAvailability, StaffingCoverage | Ready AND explicitly staffed count at snapshot | Clinical suitability, staffing derivation or placement |
| Manufacturing: one-run OEE | Run, RateDefinition, QualityObservation | Exact availability, performance, quality and product | Event-level overlap, rework reconciliation or root cause |
| Retail: original-promise line rate | OrderLine, Promise, DeliverySummary | Fully delivered lines vs original due time | Raw scan ingestion, split-quantity reconciliation or order-level rate |

## Object-level request sheet

Field types: `text` = nonblank string; `positive_int` > 0; `nonnegative_int` >= 0; `bool` is a JSON boolean; `timestamp` is canonical UTC `YYYY-MM-DDTHH:MM:SSZ`; `USD` is a literal required value. Floats and booleans are not integer amounts/counts. No nulls or undeclared row fields. IDs are unique within each object; source-system namespacing is the upstream mapper's responsibility.

### Energy

[Machine-readable mapping](../examples/industry-proof/energy-map.json) · [Runnable input](../examples/industry-proof/energy-input.json) · [Expected result](../examples/industry-proof/energy-expected.json)

| Object / grain | Required fields | Join | Accountable owner / candidate source |
| --- | --- | --- | --- |
| Contract: one contract | `id: text`, `account_id: text` | Root cohort object | Commercial data steward; Reviewed CRM/ERP contract master |
| Bookings: one booking entry | `id: text`, `contract_id: text`, `amount_minor: nonnegative_int`, `currency: USD` | `contract_id` → `Contract.id` (many-to-one) | Commercial finance; Approved bookings ledger, not Opportunity.Amount by assumption |
| RevenueEntry: one recognition entry | `id: text`, `contract_id: text`, `amount_minor: nonnegative_int`, `currency: USD` | `contract_id` → `Contract.id` (many-to-one) | Accounting; ERP recognition subledger |

Rule: `difference_minor = sum(Bookings.amount_minor) - sum(RevenueEntry.amount_minor)`.

### Financial-Services

[Machine-readable mapping](../examples/industry-proof/financial-services-map.json) · [Runnable input](../examples/industry-proof/financial-services-input.json) · [Expected result](../examples/industry-proof/financial-services-expected.json)

| Object / grain | Required fields | Join | Accountable owner / candidate source |
| --- | --- | --- | --- |
| LegalEntity: one legal entity | `id: text`, `legal_name: text` | Root cohort object | Entity data steward; Entity master; LEI mapping requires review |
| Position: one position | `id: text`, `entity_id: text` | `entity_id` → `LegalEntity.id` (many-to-one) | Risk operations; Position book |
| ReportA: one valuation per position | `id: text`, `position_id: text`, `amount_minor: nonnegative_int`, `currency: USD` | `position_id` → `Position.id` (many-to-one) | Risk methodology; Frozen risk report A |
| ReportB: one valuation per position | `id: text`, `position_id: text`, `amount_minor: nonnegative_int`, `currency: USD` | `position_id` → `Position.id` (many-to-one) | Risk methodology; Frozen risk report B |

Rule: `difference_minor = sum(ReportA.amount_minor) - sum(ReportB.amount_minor); no netting`.

### Healthcare

[Machine-readable mapping](../examples/industry-proof/healthcare-map.json) · [Runnable input](../examples/industry-proof/healthcare-input.json) · [Expected result](../examples/industry-proof/healthcare-expected.json)

| Object / grain | Required fields | Join | Accountable owner / candidate source |
| --- | --- | --- | --- |
| Bed: one bed | `id: text`, `unit_id: text` | Root cohort object | Facilities data steward; Bed/location master; not a claimed FHIR profile |
| BedAvailability: one bed at snapshot | `id: text`, `bed_id: text`, `ready: bool` | `bed_id` → `Bed.id` (many-to-one) | Clinical operations; Bed-management snapshot, no patient records |
| StaffingCoverage: one bed at snapshot | `id: text`, `bed_id: text`, `staffed: bool` | `bed_id` → `Bed.id` (many-to-one) | Staffing operations; Locally approved derived staffing coverage, not inferred from headcount |

Rule: `count(BedAvailability.ready AND StaffingCoverage.staffed), exactly one of each per Bed`.

### Manufacturing

[Machine-readable mapping](../examples/industry-proof/manufacturing-map.json) · [Runnable input](../examples/industry-proof/manufacturing-input.json) · [Expected result](../examples/industry-proof/manufacturing-expected.json)

| Object / grain | Required fields | Join | Accountable owner / candidate source |
| --- | --- | --- | --- |
| Run: one completed single-product run | `id: text`, `product_id: text`, `planned_seconds: positive_int`, `runtime_seconds: positive_int` | Root cohort object | Plant operations; MES reconciled run summary |
| RateDefinition: one approved rate per run | `id: text`, `run_id: text`, `product_id: text`, `ideal_cycle_seconds: positive_int` | `run_id` → `Run.id` (many-to-one) | Industrial engineering; Versioned engineering rate selection |
| QualityObservation: one reconciled count per run | `id: text`, `run_id: text`, `total: positive_int`, `good: nonnegative_int` | `run_id` → `Run.id` (many-to-one) | Quality; MES/QMS reconciled counts; rework handled upstream |

Rule: `availability=runtime/planned; performance=ideal_cycle*total/runtime; quality=good/total`.

### Retail

[Machine-readable mapping](../examples/industry-proof/retail-map.json) · [Runnable input](../examples/industry-proof/retail-input.json) · [Expected result](../examples/industry-proof/retail-expected.json)

| Object / grain | Required fields | Join | Accountable owner / candidate source |
| --- | --- | --- | --- |
| OrderLine: one noncancelled required line | `id: text`, `order_id: text` | Root cohort object | Fulfillment operations; Frozen OMS line cohort |
| Promise: one original promise per line | `id: text`, `line_id: text`, `original_due_at: timestamp` | `line_id` → `OrderLine.id` (many-to-one) | Customer operations; Immutable original OMS promise extract |
| DeliverySummary: one full-quantity delivery per line | `id: text`, `line_id: text`, `delivered_at: timestamp`, `full_quantity: bool` | `line_id` → `OrderLine.id` (many-to-one) | Fulfillment operations; Reviewed WMS/carrier aggregation, not raw scans |

Rule: `on_time = count(DeliverySummary.delivered_at <= Promise.original_due_at), one per required line`.

## Shared envelope: evidence that facilitates each proof

Every source object has `source_ref`, pinned `schema_revision` (`synthetic-v1`), identical `scope`, `observed_at`, `complete`, `expected_ids` and `rows`. Scope contains a nonblank `cohort` plus a positive UTC `window_start` / `window_end` interval. Source observation must equal the frozen window end in this bounded version: there is no configurable freshness policy. Healthcare uses the end-of-window snapshot, not average capacity over the window. Finance compares frozen as-of reports, not a time series.

- **Completeness:** freeze expected record IDs separately before extraction, then compare returned IDs and explicit feed/page completion. Missing, duplicate or orphan rows block calculation. The fixture manifest is self-asserted, not proof of real source completeness; an upstream mapper could omit the same record from rows and manifest and evade detection.
- **Alignment:** the envelope asserts a common cohort/time. A steward must verify that row-level event/accounting/valuation times were mapped correctly. Relabeling two mismatched extracts with the same scope is not detected. USD-only positive ledger inputs exclude credits, signed positions and FX; these require a reviewed extension.
- **Grain:** finance requires exactly one valuation per position in each report. Healthcare requires one availability and staffing record per bed. Manufacturing accepts one run, one product-matched rate and one quality count; factors above one block instead of being capped. Retail requires one original promise and one complete delivery summary per required line; due times and delivery times cannot exceed cutoff. Energy allows many ledger entries per contract, but every contract must appear on both sides.
- **Provenance:** source reference and schema are supplied claims. The receipt binds inputs and code, not source authenticity, steward approval or permission. There is no live connector, authentication, pagination fetcher, persistence or signed receipt.
- **Interpretation:** successful arithmetic never establishes causation. Staffed capacity never establishes clinical suitability. Gross exposure does not establish netting. Every output remains labeled `synthetic_only`, even when the CLI accepts a user-supplied normalized file.

These guardrails validate a **pre-normalized evidence packet**. They do not replace the upstream aggregation/identity/time rules that prepare it.

## Native binding handoff: fill only the selected pilot

For each required object/field, the platform owner supplies this row. Leave unknowns unknown; do not invent API names.

```text
Logical object.field | native system / object / field | schema/model revision
Primary and foreign keys / cardinality | event and accounting time semantics
Unit / conversion / transformation | exclusions and expected-ID manifest origin
Read-only operation / approved identity and policy | owner / actual approval reference
Sanitized export hash | observed failure / next action | acceptance evidence
```

Reconcile the mapper against manually adjudicated source rows, especially quantities, split deliveries, effective intervals and timestamps. Current native mappings are **unverified**. Use the existing [sandbox gates](CTO-PILOT-KIT.md) to prove source-enforced permissions separately. Do not interpret a local `complete: true` or owner label as authenticated approval.

## Saving time: one next action per gap

1. Choose one decision where there is an actual disputed answer. If no decision owner or data need exists, stop.
2. Request only its mapped objects and manifest. Do not gather the entire enterprise catalog.
3. Run the check; route the consolidated missing-object/field/join list to its listed owners. Retain the receipt and unresolved gaps.
4. Have an evaluator outside the implementation team freeze expected outputs for new cases. Compare against the existing workflow on the same cases, including valid answers, false refusals and unsupported answers.
5. Record elapsed data-discovery time, clarification round trips and correction time for both workflows. If this adds effort without decision improvement, reject or simplify it. **Time savings have not yet been measured.**

[Counterexample tests](../tests/test_industry_proof.py) exercise every mapped object's missing/stale/duplicate/coverage failures, every foreign-key join, invalid numeric inputs and domain-specific traps. Alternative valid values check that the implementation computes answers rather than memorizing fixtures. The labels are maintainer-authored, not held out or independent. Run all checks with `python3 scripts/verify.py`.

Broader domain challenges in the [CTO brief](CTO-ADVISORY.md) remain proposals until separately implemented and tested. Licensing, domain review and live access gates remain unchanged.

The compatibility command `python3 industry_proof.py` remains supported. The implementation and bundled fixtures live in `sgo/`; regression tests live in `tests/`.
