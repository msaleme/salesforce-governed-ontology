# Five-minute demonstration

**Audience:** business leaders, solution architects, and domain stewards.  
**Objective:** show why an agent needs governed meaning before selecting data.  
**Setup:** Python 3.10+, a local checkout, no credentials or external services.

## 1. Start with the business question

> “Why do bookings and recognized revenue differ for this operator?”

A shared label does not make two measures interchangeable. A useful answer needs the definition, cohort, period, currency, source, and evidence for the explanation.

Run the complete tour:

```sh
python3 explore.py tour
```

The tour is deterministic. It demonstrates rules, not an LLM interpreting arbitrary language.

## 2. Show the decisions

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

## 3. Show the evidence

```sh
python3 explore.py validate
python3 scripts/verify.py
```

Open [the ontology map](ONTOLOGY-MAP.md) to see the vocabulary. Open [ontology.json](../ontology.json) for the actual definitions. The two outputs above validate the bounded fixture model and run the local regression suite, not vendor integrations.

## Questions worth answering directly

**Is this shipping Salesforce functionality?** No. It is a proposed Salesforce-centered architecture plus an offline reference prototype.

**Why not use the catalog as the ontology?** Catalog metadata contributes evidence. A business definition still needs a steward, effective version, interpretation, and approved action mapping. Existing platform semantics should be evaluated before building a separate registry.

**Does “approved” prove finance signed off?** Only inside this synthetic fixture. An authenticated approval workflow is not implemented.

**Can it query our ERP?** Not yet. The next milestone is one read-only sandbox path with actual identity, metadata, API binding, and source receipts.

**Is this a general reconciliation engine?** No. It compares one pre-aligned synthetic contract cohort. It does not align ledgers or infer accounting treatment.

## Capture feedback

Record the business question, disputed definition, source owner, required permission boundary, expected evidence, and the smallest sandbox proof. Use the [platform-fit review](PLATFORM-FIT-REVIEW.md); avoid collecting customer data in public issues.
