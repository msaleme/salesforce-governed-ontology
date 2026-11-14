# Run, demonstrate and reproduce

[Five-minute demo](#five-minute-demonstration) · [Walkthrough](#reproduce-the-revenue-demonstration) · [Reproduction receipt](#reproduce-and-challenge-the-decision-contract) · [Captured output](#captured-synthetic-terminal-demonstration)

Install once in a virtual environment with `python3 -m pip install -e .`.
Commands below run offline after installation. For custom inputs, see
[bring your own data](BRING-YOUR-OWN-DATA.md).

## Five-minute demonstration

**Audience:** business leaders, solution architects, and domain stewards.

**Objective:** show why an agent needs governed meaning before selecting data.

**Setup:** Python 3.10+, a local checkout, no credentials or external services.

### 1. Start with the business question

> “Why do bookings and recognized revenue differ for this operator?”

A shared label does not make two measures interchangeable. A useful answer needs the definition, cohort, period, currency, source, and evidence for the explanation.

Run the complete tour:

```sh
python3 explore.py tour
```

The tour is deterministic. It demonstrates rules, not an LLM interpreting arbitrary language.

### 2. Show the decisions

| Time | Run | Explain |
| --- | --- | --- |
| 0:00 | `python3 explore.py scenario ambiguity` | “Revenue” is ambiguous. Ask which definition the user means. |
| 0:45 | `python3 explore.py scenario approved-read` | Resolve recognized revenue to a versioned definition and a fixed read plan. No API executes. |
| 1:30 | `python3 explore.py scenario binding-mismatch` | Even an allowed source or API can be wrong for this metric. Reject the mismatch. |
| 2:00 | `python3 explore.py scenario denied` | Missing fixture scope stops the plan. Real identity enforcement is a later integration gate. |
| 2:30 | `python3 explore.py scenario difference-only` | USD 1.2M minus USD 0.9M is USD 0.3M. Subtraction alone does not explain why. |
| 3:15 | `python3 explore.py scenario explained` | A separate, matching fixture bridge supplies the explanation and its source reference. |
| 4:00 | `python3 explore.py scenario incompatible` | EUR and USD cannot be reconciled by subtraction without a defined conversion policy. |
| 4:30 | `python3 explore.py scenario expired` | Approval does not make a definition valid forever. |

**Closing line:** “The agent should know which meaning is approved before it decides which action to request.”

### 3. Show the evidence

```sh
python3 explore.py validate
python3 scripts/verify.py
```

Open [the ontology map](DATA-MODEL.md#ontology-map) to see the vocabulary. Open [ontology.json](../ontology.json) for the actual definitions. The two outputs above validate the bounded fixture model and run the local regression suite, not vendor integrations.

### Questions worth answering directly

**Is this shipping Salesforce functionality?** No. It is a proposed Salesforce-centered architecture plus an offline reference prototype.

**Why not use the catalog as the ontology?** Catalog metadata contributes evidence. A business definition still needs a steward, effective version, interpretation, and approved action mapping. Existing platform semantics should be evaluated before building a separate registry.

**Does “approved” prove finance signed off?** Only inside this synthetic fixture. An authenticated approval workflow is not implemented.

**Can it query our ERP?** Not yet. The next milestone is one read-only sandbox path with actual identity, metadata, API binding, and source receipts.

**Is this a general reconciliation engine?** No. It compares one pre-aligned synthetic contract cohort. It does not align ledgers or infer accounting treatment.

### Capture feedback

Record the business question, disputed definition, source owner, required permission boundary, expected evidence, and the smallest sandbox proof. Use the [platform-fit review](ASSURANCE.md); avoid collecting customer data in public issues.

## Reproduce the revenue demonstration

Run all commands from the repository root with Python 3.10+.

### 1. Inspect the definitions

Read [ontology.json](../ontology.json). Notice that contract bookings and recognized revenue have different definitions, sources, and operations despite sharing dimensions.

### 2. Run the scenario

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

### 3. Remove the explanation

```sh
python3 - <<'PYTHON'
from demo import fixtures, reconcile
booked, recognized, _ = fixtures()
print(reconcile(booked, recognized))
PYTHON
```

The result is `difference_only` and has no explanation. This is intentional: subtraction is not causal evidence.

### 4. Exercise a date outside validity

```sh
python3 - <<'PYTHON'
from demo import resolve
print(resolve('recognized_revenue', {'finance:read'}, as_of='2027-01-01'))
PYTHON
```

The result is `definition_unavailable`. The regular demo uses a fixed in-range date for reproducibility, not the host's current date.

### 5. Verify the checkout

```sh
python3 scripts/verify.py
```

This runs the unit controls, compares generated and checked-in example JSON, and checks repository-relative Markdown file links. It does not contact vendor platforms or validate external documentation URLs. See [validation](ASSURANCE.md) for evidence limits.

## Reproduce and challenge the decision contract

The [captured terminal demonstration](RUN-GUIDE.md) shows clarification, an accepted read plan, a wrong-binding refusal, arithmetic without explanation and a synthetic explanation bridge. CI checks the transcript against actual CLI output. This is text, not a recorded video or live integration.

### One-command evidence packet

Use Python 3.10+ and Git in a clean checkout. Install first with `python3 -m pip install -e .`. No credentials, platform accounts or model calls are needed.

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
python3 -m pip install -e .
python3 scripts/reproduce.py > ../ontology-reproduction.json
```

The command runs the full verifier and fixed-case evaluator, records their exit codes/output, the Git commit, Python version, dirty-tree flag and SHA-256 hashes of tracked files. Either command failing produces an overall failure and nonzero exit. A timeout terminates with an error, not a success receipt. Write the receipt outside the checkout so its creation does not dirty the tree.

Hashes identify bytes, not authorship or approval. The commit identifies HEAD, not uncommitted changes. The dirty flag includes untracked files; these are not hashed. Use a clean checkout for a comparable run. The receipt explicitly leaves independence `not_established`; another automated self-run is not independent validation. Inspect logs before sharing, especially after modifying tests to use local inputs.

### Submit useful evidence

Use the [counterexample form](https://github.com/msaleme/salesforce-governed-ontology/issues/new?template=decision-counterexample.yml). State:

- Commit and clean/dirty state, Python version, commands and exit codes.
- Whether you are an independent contributor or project maintainer.
- The specific case, actual result and expected result, with a minimal synthetic input.
- Whether this reproduces existing fixture behavior or challenges a decision rule.

A passing fixed suite is not a held-out evaluation. Do not send private metadata or credentials. No external reproductions have yet been established.

### Native-platform validation handoff

The next integration cannot be selected by guessing a metric mapping. A platform owner must supply one approved native metric export with its schema/version, unit, grain and identity; a designated sandbox; and approved read-only bindings/access. Use the [platform-fit template](ASSURANCE.md) and [sandbox checklist](SANDBOX-INTEGRATION.md).

Acceptance: retain a pinned export, prove a compatible mapping, deliberately change grain/unit/binding to show rejection, and exercise permitted and denied identities. Preserve lifecycle and explanation evidence in a reviewed sidecar when native fields cannot represent them. Do not claim an adapter or runtime authorization until those tests run against the selected foundation. Reuse is covered by the [MIT License](../LICENSE).

<!-- BEGIN GENERATED TRANSCRIPT -->
# Captured synthetic terminal demonstration

Generated by `python3 scripts/reproduce.py --demo`. These are local synthetic outputs, not a video, live platform read or independent reproduction.

```text
$ python3 explore.py scenario ambiguity
{
  "scenario": "ambiguity",
  "title": "Which revenue?",
  "lesson": "Clarify the metric before choosing a source.",
  "expected_status": "clarification_required",
  "result": {
    "status": "clarification_required",
    "choices": [
      "booked_revenue",
      "recognized_revenue"
    ]
  }
}
```

```text
$ python3 explore.py scenario approved-read
{
  "scenario": "approved-read",
  "title": "An approved definition",
  "lesson": "Return a read plan, never execute an API.",
  "expected_status": "read_plan_only",
  "result": {
    "status": "read_plan_only",
    "evidence": "synthetic_only",
    "concept": "recognized_revenue",
    "version": "0.1.0",
    "definition": "Synthetic demonstration definition: revenue recognized for satisfied performance obligations during the accounting period, net of reversals.",
    "source": "fixture:erp:revenue_ledger",
    "operation": "read_recognized_revenue"
  }
}
```

```text
$ python3 explore.py scenario binding-mismatch
{
  "scenario": "binding-mismatch",
  "title": "The wrong source",
  "lesson": "An allowlisted API is insufficient if it is bound to the wrong metric.",
  "expected_status": "binding_mismatch",
  "result": {
    "status": "binding_mismatch"
  }
}
```

```text
$ python3 explore.py scenario difference-only
{
  "scenario": "difference-only",
  "title": "Arithmetic is not causality",
  "lesson": "Without a bridge, report only the difference.",
  "expected_status": "difference_only",
  "result": {
    "status": "difference_only",
    "currency": "USD",
    "difference_minor": 30000000,
    "sources": [
      "fixture:crm:contract_bookings",
      "fixture:erp:revenue_ledger"
    ],
    "evidence": "synthetic_only"
  }
}
```

```text
$ python3 explore.py scenario explained
{
  "scenario": "explained",
  "title": "An evidence-backed explanation",
  "lesson": "A matching synthetic bridge supplies the explanation.",
  "expected_status": "explained_by_fixture_bridge",
  "result": {
    "status": "explained_by_fixture_bridge",
    "currency": "USD",
    "difference_minor": 30000000,
    "sources": [
      "fixture:crm:contract_bookings",
      "fixture:erp:revenue_ledger",
      "fixture:reconciliation:001"
    ],
    "evidence": "synthetic_only",
    "explanation": "Unfulfilled performance obligations in this synthetic contract cohort"
  }
}
```
<!-- END GENERATED TRANSCRIPT -->
