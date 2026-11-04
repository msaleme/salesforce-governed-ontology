# Reproduce the revenue demonstration

Run all commands from the repository root with Python 3.10+.

## 1. Inspect the definitions

Read [ontology.json](../ontology.json). Notice that contract bookings and recognized revenue have different definitions, sources, and operations despite sharing dimensions.

## 2. Run the scenario

```sh
python3 demo.py
```

Expected results:

- `ambiguous_question.status`: `clarification_required`.
- `bookings_plan.status` and `recognized_plan.status`: `read_plan_only`.
- `unauthorized_fixture.status`: `denied`.
- `reconciliation.status`: `explained_by_fixture_bridge`.
- `reconciliation.difference_minor`: `30000000`, or USD 300,000.

The source identifiers start with `fixture:`. They are not retrieved records or receipts from a vendor system.

## 3. Remove the explanation

```sh
python3 - <<'PYTHON'
from demo import fixtures, reconcile
booked, recognized, _ = fixtures()
print(reconcile(booked, recognized))
PYTHON
```

The result is `difference_only` and has no explanation. This is intentional: subtraction is not causal evidence.

## 4. Exercise a date outside validity

```sh
python3 - <<'PYTHON'
from demo import resolve
print(resolve('recognized_revenue', {'finance:read'}, as_of='2027-01-01'))
PYTHON
```

The result is `definition_unavailable`. The regular demo uses a fixed in-range date for reproducibility, not the host's current date.

## 5. Verify the checkout

```sh
python3 scripts/verify.py
```

This runs the unit controls, compares generated and checked-in example JSON, and checks repository-relative Markdown file links. It does not contact vendor platforms or validate external documentation URLs. See [validation](VALIDATION.md) for evidence limits.
