# MuleSoft semantic federation implementation contract

**Status: proposed v0.1 contract.** This is an implementation specification, not a deployable Mule project, generated connector or current Python API. All paths below are proposed. No vendor credentials, endpoints or native exports are bundled.

## API-led boundaries

| Layer | Proposed operation | Responsibility |
| --- | --- | --- |
| Experience | `POST /v1/decision-answers` | Accept bounded business request; return answer, clarification or gap |
| Process | `POST /v1/metric-queries` | Resolve reviewed binding, verify scope and definition, route to exactly one native engine |
| System | `GET /v1/semantic-definitions/{bindingId}` | Retrieve native metadata and pinned revision/digest |
| System | `POST /v1/approved-metric-queries` | Execute an allowlisted, parameterized native read |
| System | `GET /v1/query-receipts/{receiptId}` | Return permitted execution evidence; apply caller authorization again |

Do not expose arbitrary SQL, DAX, URLs, table names or credentials in request bodies. Binding IDs resolve only through a steward-reviewed server-side registry. Reject unsupported dimensions and filters. A digest records content, not approval.

## Bounded request example

Illustrative request to the Process API, not a runnable command:

```json
{
  "metric_id": "recognized_revenue",
  "mapping_revision": "draft-2026-11-13",
  "binding_id": "example-snowflake-revenue",
  "group_by": ["operator_id", "contract_id", "period", "currency"],
  "filters": {
    "operator_id": "synthetic-operator-001",
    "period": "2026-10",
    "currency": "USD"
  }
}
```

The draft binding must return `requires_binding_review`, never a live answer. Period means the steward-approved accounting calendar, not an inferred calendar month. Binding configuration records allowed groupings, period format, filters, limits, source identity, native revision, reviewer evidence, valid dates, currency scale and approved backend operation. Request values never override these rules.

Principal, tenant and effective source-policy context come from authenticated middleware, not client JSON. Authenticate the caller and validate its entitlement to the selected binding before revealing binding metadata. Each System API must enforce the approved caller-to-source authorization design. A gateway scope alone is insufficient.

## Response contract

All responses carry `status`, `request_id` and `mapping_revision` (nullable before resolution). IDs are generated at runtime. An answer additionally requires:

- `metric_id`, `native_platform`, `native_metric_ref` and `native_definition_revision`.
- `dimensions`, `unit`, `currency`, `period` and the approved calendar identity.
- `amount_minor_units` as an integer for this finance pilot. Never silently round a native decimal, assume cents for every currency or mix currencies.
- `data_as_of`, `query_receipt`, `complete: true` and lineage references permitted for the caller.
- Explicit limitations; reconciliation explanations need separate evidence.

A non-answer has no amount and carries an actionable `reason_code`, responsible `owner` and `next_action` where disclosure is permitted. Do not manufacture source timestamps or receipts. Query completion time is not data freshness.

| HTTP | Status / reason | Behavior |
| --- | --- | --- |
| 200 | `answered` | Only complete, approved, authorized result |
| 400 | `invalid_request` | Unknown fields, invalid dimensions/filter or unsupported metric |
| 401 / 403 | `unauthenticated` / `denied` | No result or sensitive definition details |
| 409 | `requires_binding_review`, `definition_drift`, `incompatible_semantics` | No execution on an unapproved/stale binding; semantic differences cannot become answers |
| 422 | `clarification_required` | Ask for missing business meaning or scope |
| 502 | `incomplete_result` | Reject partial/truncated results; no success amount |
| 503 / 504 | `source_unavailable` / `source_timeout` | No fallback to another metric or broader identity |

## Mule implementation sequence

1. Define RAML or OpenAPI assets in the team's existing Anypoint workflow from this contract. Select supported Mule runtime, connector versions and tenant entitlements; pin them in the implementation PR. This packet does not assert a tested runtime version.
2. Implement System API metadata adapters first. Retain namespaced native identities and opaque formulas. Use documented Data Cloud connector operations where applicable; use authenticated HTTP for Tableau Semantics APIs not exposed by that connector. Warehouse access and other APIs require individually validated interfaces.
3. Use DataWeave for field normalization only. Map native identity, label, dimensions, unit metadata, revision and lineage into candidate sidecars. Missing values stay unresolved. Never default a missing revision, unit or steward approval into validity.
4. Route candidates into review. Compare native export digests, collect finance approval and integration-owner approval, then publish immutable mapping revisions. Quarantine changes until reviewed. Keep historical bindings for audit, but do not execute expired ones.
5. Implement the Process API with explicit pre-query checks for meaning, grain, aggregation, unit/scale, calendar, lifecycle, source revision and authorization. Native SQL/DAX/MetricFlow/LookML remains in its authoritative engine. Do not equate a row-level fact with an aggregate measure.
6. Execute one approved read with parameter binding and bounded timeout/result size. Use pagination/completion markers from the native API; exhaustion must be proved before success. Never sum pages of an already aggregated metric without a reviewed aggregation contract.
7. Validate the returned schema, units, scope and completion. Normalize only reviewed representations. Return the envelope above, or a typed failure. A zero result is different from an absent/incomplete result.
8. Expose the Experience API to the selected Salesforce/Agentforce integration route only after testing it in the designated org. Keep the pilot read-only. No operational action or write-back is supplied here.

## Operational controls

- Cache only under an approved freshness policy. Key by tenant, effective principal/policy, native revision, mapping revision, filters, grouping and snapshot. Invalidate on policy or definition change; prefer no cache until isolation is proved.
- Log correlation IDs, mapping revision, native query ID and reason codes. Redact credentials and sensitive payloads. Receipt access uses the same authorization as the original result.
- Bound retries for read-only transient failures; do not retry denials or bypass stale-definition failures. Native asynchronous query execution must retain its original query ID rather than launch duplicate work blindly.
- Disable an adapter by unpublishing its active binding. Rollback selects a previously approved revision only after checking that its native definition is still available and authorized. Never roll back into a stale formula.
- Keep the native metric steward accountable for business semantics, the integration owner for transport/query correctness, and the security owner for effective source permissions.

## What remains to implement

Mule application flows, RAML/OpenAPI validation, DataWeave transformations, native query templates, authentication configuration, deployment and MUnit/live integration tests. They require approved native exports and sandbox access. This reference contract must not be marketed as any of those deliverables.

See [architecture and source references](ARCHITECTURE.md), [platform crosswalk](CROSSWALK.json), and [pilot acceptance](PILOT.md).
