# Semantic federation pilot: recognized revenue

**Not yet executed.** Start with one approved Tableau Semantics measure over Data 360 and one Snowflake Semantic View metric. Databricks follows after that pair passes. dbt, Looker and Power BI/Fabric remain mapped designs until their own tests run.

## Inputs and owners

- Finance steward: recognized-revenue definition, exclusions, reversal handling, currency scale, accounting calendar and acceptable rounding/tolerance (no implicit tolerance).
- Data owners: sanitized matching snapshot or controlled test dataset, canonical operator/contract keys, effective-dated operator roles and expected values independently computed by finance.
- Integration owner: native metadata exports/revisions, candidate bindings, bounded queries, designated Mule/Salesforce sandboxes and required entitlements.
- Security owner: approved test principals with deliberately different row/field permissions and expected visibility. Never obtain production credentials for a documentation exercise.
- Evaluator: baseline workflow timings, correctness rubric, setup effort and execution log.

## Acceptance matrix

These are planned cases, not passed tests. Every engine must have positive controls; blanket refusal fails the pilot.

| Case | Controlled change | Required outcome |
| --- | --- | --- |
| Aligned answer | Same approved snapshot, definition, scope and principal | Correct value and native receipt from each engine; compare, do not add |
| Authorized zero | Complete empty/zero-value scope per native contract | Valid zero only when contract establishes it, not fabricated missing-data default |
| Bookings vs recognition | Substitute booked revenue under a matching label | Reject mapping; no equivalent-revenue claim |
| Currency | USD vs EUR | Reject comparison without approved conversion evidence |
| Scale | Major vs minor units | Reject unreviewed conversion; accept separately reviewed exact conversion |
| Period | Fiscal vs calendar period | Reject comparison until aligned by approved calendar |
| Temporal role | Owner or prior operator instead of current operator | Reject scope/join mismatch |
| Fan-out | Duplicate join matches | Detect/reject unsafe mapping or prove correct native grain |
| Non-additive metric | Ratio/window metric instead of sum | Reject sum translation; retain native calculation |
| Definition drift | Native revision changes after approval | Stop execution and send review action |
| Lifecycle | Mapping expired or not yet effective | No execution |
| Partial results | Truncation, failed page, missing completion | Non-answer, no success amount |
| Source denial | Principal lacks required rows/fields | Native denial/approved restriction; no broader service-account result |
| Cache isolation | Repeat query as differently entitled principal | No unauthorized result or receipt reuse |
| Failure | Timeout or unavailable engine | Typed failure; no unapproved alternate authority |
| Explanation | Equal numbers, no bridge evidence | May compare values; must not invent causal reconciliation |

## Evidence worksheet

For every run record: case, expected outcome, actual outcome, engine, principal alias (not secret), snapshot identifier, native revision/export digest, mapping revision, query ID, timestamp, completion evidence, result hash, reviewer and disposition. Keep sensitive extracts and receipts in the approved evidence store; publish only sanitized summaries.

Pair comparison requires equivalent authorized rows, snapshot, dimensions, filters, currency scale and period. Equal totals alone do not prove equivalent definitions. A native successful query does not prove permission propagation across the entire MuleSoft route.

## Evaluation and exit criteria

1. Record the same analyst question under the existing workflow and the proposed path. Alternate ordering where feasible; preserve equivalent inputs and record familiarity effects.
2. Measure active analyst minutes, elapsed time, clarification rounds, correctness and one-time setup/maintenance effort separately. Preserve unsuccessful trials.
3. Require all material semantic and authorization cases to pass with reviewable receipts; unresolved cases block promotion. State sample size and scope, without extrapolating one pilot to enterprise-wide savings.
4. Finance and security reviewers accept results before publishing a binding. Add the Databricks adapter only after the initial pair passes. Repeat platform-specific counterexamples, not just transport checks.
5. If value or correctness does not improve, document that outcome and narrow or stop the integration. No measured benefit is claimed by this repository.

[Architecture](ARCHITECTURE.md) · [MuleSoft contract](MULESOFT.md) · [Crosswalk](CROSSWALK.json)
