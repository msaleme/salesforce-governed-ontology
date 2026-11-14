# A correct subtraction is not an explanation

**Source draft, published on dev.to on 2026-11-08.** The [published walkthrough](https://dev.to/mspro3210/a-correct-subtraction-is-not-an-explanation-j5f) uses absolute links and pins the verified merged commit. This file preserves the source narrative; not a claim of independent validation or vendor superiority.

An agent sees $1.2 million in contract bookings and $900,000 in recognized revenue. It subtracts correctly and then says the $300,000 difference is caused by unfulfilled performance obligations.

The arithmetic did not establish that explanation.

That distinction is the point of this small semantic decision testbed. It separates three questions: which metric did you mean, which read plan matches that definition, and what evidence supports explaining the difference?

## Run the distinction locally

Use Python 3.10 or later. No account, credentials, model endpoint or third-party packages are needed.

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
git rev-parse HEAD
python3 explore.py scenario ambiguity
python3 explore.py scenario binding-mismatch
python3 explore.py scenario difference-only
python3 explore.py scenario explained
python3 evaluate.py
python3 scripts/verify.py
```

Record the commit printed by `git rev-parse HEAD` when reporting a result. Before distributing this article, verify these commands on the linked default-branch commit. A PR version should instead be linked and identified as a candidate.

## What to look for

**Ambiguity:** “revenue” produces `clarification_required`, offering bookings and recognized revenue rather than silently choosing one.

**Binding mismatch:** a recognized-revenue definition pointed at the bookings fixture produces `binding_mismatch`. A known source is not necessarily the right source for a metric.

**Difference only:** the aligned cohort produces `difference_only`, `currency: USD` and `difference_minor: 30000000`. Amounts are integer minor units, so that value is $300,000. There is no explanation field.

**Explained:** a separately supplied bridge with matching dimensions and amount produces `explained_by_fixture_bridge`. The result includes the bridge's source and stated reason. That bridge is synthetic. The program does not authenticate it or prove the accounting policy is correct.

A correct subtraction is not an explanation.

## Why another semantic example?

Existing semantic layers already define metrics and generate queries. Operational ontology platforms connect business objects to actions. Knowledge-graph systems support graph interchange and inference. Reimplementing those capabilities would not make this example stronger.

The narrower contribution is an inspectable acceptance test: make the decision and its evidence easy to challenge. The [comparison](COMPARISON.md) distinguishes these categories and documents where to reuse existing platforms.

The intended role is complementary. Keep authoritative metric definitions in the platform that owns them. Eventually, reproduce these acceptance cases against that native model instead of introducing a second source of truth.

## A passing label can hide a failing answer

An evaluator that checks only `difference_only` can pass a result with the wrong amount. It can also miss an invented explanation appended to that result.

The [fixed decision contract](ASSURANCE.md) now checks complete result objects: source, operation, amount, currency, evidence markers and unexpected fields. Mutation tests deliberately keep the status correct while corrupting important payload fields. The evaluator must reject those results.

This is regression evidence, not a vendor leaderboard or model accuracy score. The expected cases were authored with the prototype. They are not held out. Exact fixture agreement does not establish production correctness.

## The next useful contribution is a counterexample

Pick a case where this decision rule is insufficient. Could a matching bridge still describe the wrong accounting treatment? Could a metric mapping preserve its name but change its grain? What should happen when a lifecycle date is confused with the data period?

Use the repository's [counterexample issue form](https://github.com/msaleme/salesforce-governed-ontology/issues/new?template=decision-counterexample.yml). Include the commit, command, minimal synthetic input, actual result and the expected decision with a reason. A conceptual gap is welcome; distinguish it from an executable reproduction.

Do not include customer data, tokens or private metadata. One reproducible disagreement is more useful than a general endorsement.

## What remains unproven

No live metric execution, native-platform interoperability, authenticated authorization, independent reproduction or general accounting validation is demonstrated here. The [gap ledger](COMPARISON.md) keeps those boundaries explicit. This is a reference prototype, not an official vendor product; see [MIT license](../LICENSE) for reuse terms.
