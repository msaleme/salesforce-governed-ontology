# Bring your own metric definitions and cases

```sh
sgo byod examples/user-metrics.json
sgo validate-registry ontology.json
```

Copy the [example file](../examples/user-metrics.json), edit the embedded
`ontology.metrics`, and write your own `cases`. No special metric IDs or vendor
names are required. This command evaluates definition availability, required
scope and an explicit read plan. It does not compute metrics, interpret SQL/DAX,
translate semantic layers or reconcile arbitrary datasets.

## File contract

The top-level object contains exactly `ontology` and `cases`.

- `ontology` follows [ontology.schema.json](../sgo/ontology.schema.json), JSON
  Schema draft 2020-12. It contains registry identity/version/status/namespace,
  evidence, concepts, relationships and metrics. Use `user_supplied_unverified`
  for evidence; supplied approval records do not prove external approval.
- Each metric specifies identity, label, definition, version, lifecycle state,
  approval provenance, ISO validity dates, grain, aggregation, unit, source,
  lineage, and a read-only action with operation ID and required scope.
- Each case has exactly `id`, `request` and `expected_result`.
- `request` has exactly `metric`, `scopes` (a string array), and `as_of`
  (`YYYY-MM-DD`, explicit for reproducibility).
- `expected_result` is the **entire** result object, not just a status. Extra or
  missing fields fail the case. Expectations are supplied by you, not generated
  during evaluation.

The example uses a custom `support_tickets` count metric and includes accepted,
denied, expired and unknown-metric cases. Source and operation strings are opaque
labels. They are never imported, executed or fetched, even if they resemble URLs
or code. Keep private data local; do not submit it with issue reports.

## Outcomes and exit codes

- `read_plan_only`: approved, in-date definition and matching supplied scope.
  Returns concept, version, definition, source, operation and
  `evidence: user_supplied_unverified`.
- `denied`: supplied scopes do not include the metric's required scope.
- `definition_unavailable`: lifecycle or date excludes the definition.
- `unsupported_concept`: metric ID is absent.

Exit **0**: every full-result expectation matches. Exit **1**: at least one
expectation mismatch (or registry validation fails). Exit **2**: file, JSON,
registry or case input error for `byod`. Malformed files never produce a partial
success receipt. Empty cases, duplicate JSON keys, nonfinite numbers, duplicate
IDs, dangling relationships, invalid/reversed dates, non-read actions and lineage
missing the source are rejected.

## Validation boundaries

`sgo validate` retains the strict two-metric synthetic fixture bindings and
finance grain. `sgo validate-registry FILE` supports custom definitions: schema
validation plus ID/graph, date and lineage checks. The schema permits extension
properties for change-review compatibility; extensions are not executed or
interpreted. Schema validity alone does not prove semantic correctness.

BYOD does not establish that a source implements the stated metric. A structurally
valid swapped source is an unverified read plan, not an authenticated binding.
Use independently authored expectations to detect changes. Production binding,
identity and native-platform evidence belong in the [assurance guide](ASSURANCE.md).
