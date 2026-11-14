# Project notes

- [Evidence-led attention packet](#attention)
- [Distribution evidence: 2026-11-08](#publication-record)
- [Licensing decision](#licensing-decision)
- [A correct subtraction is not an explanation](#article-draft)

<a id="attention"></a>

## Evidence-led attention packet

Status: **dev.to walkthrough published 2026-11-08; LinkedIn remains a manual draft**. The goal is qualified reproduction and counterexamples, not traffic or sales. This is a reference prototype, not an official vendor product. Reuse is covered by the MIT License.

### The memorable idea

**A correct subtraction is not an explanation.**

Lead with a familiar failure: contract bookings and recognized revenue differ; the agent explains why without evidence. Show the refusal and the evidence needed to move beyond it. The [decision evaluation](ASSURANCE.md) gives a reader something concrete to run and challenge.

### Repository improvements included

- [Comparison](COMPARISON.md): explicit alternatives, reuse decisions, trade-offs and remaining gaps.
- [Evaluation](ASSURANCE.md): a reproducible result with both successful and refused decisions.
- [Counterexample form](../.github/ISSUE_TEMPLATE/decision-counterexample.yml): a structured path to contribute an observed failure.
- README entry points: one positioning statement and direct links to the evidence and contribution path.

- [Complete technical article draft](PROJECT-NOTES.md#article-draft): runnable narrative, expected outcomes and a narrow counterexample request.

### Proposed distribution experiments

The dev.to walkthrough and captured text demonstration are delivered; other rows remain proposed, not scheduled jobs or promises. Post only after the reviewed code is available on the linked default branch, or link an immutable reviewed commit and identify it as a candidate.

| Priority | Surface and artifact | Audience hypothesis | Outcome to measure | Stop/change rule |
| --- | --- | --- | --- | --- |
| 1 | One manual LinkedIn post using the draft below | Analytics/platform owners recognize the bookings-versus-revenue failure | Substantive counterexample or independently reported reproduction | After 14 days, if no qualified response, change the concrete case instead of reposting the thesis |
| 2 | One dev.to walkthrough: “A correct subtraction is not an explanation” | Engineers want inspectable agent decision controls | Reported commands/results and actionable issues, not page views alone | If visits arrive but no reproductions, simplify the run instructions and ask one narrower technical question |
| 3 | A short synthetic terminal demonstration linked from the walkthrough | Readers need to see refusal and success in the same flow | Reproduction reports citing the demonstrated cases | Do not claim a video exists until recorded and checked |
| 4 | A neutral standards mapping note after adapter evidence exists | Interoperability reviewers care about lost temporal/action semantics | Concrete mapping correction or accepted technical feedback | Hold until a reproducible mapping loss exists; do not post project plugs on third-party repos |

Before any original post, check that surface's last 7 days and the last 30 days for a near-duplicate thesis; at most one original post per surface per week. Do not auto-post LinkedIn, create empty GitHub Discussions, or promote on third-party issue threads. The dev.to walkthrough was published after these checks; see the [publication record](PROJECT-NOTES.md#publication-record).

### LinkedIn draft

An agent sees contract bookings of $1.2 million and recognized revenue of $900,000.

The difference is $300,000. That does not tell it why.

A correct subtraction is not an explanation.

I built a small synthetic reference that makes the distinction explicit: clarify the revenue definition, validate the read plan, and report only the difference unless a matching explanation bridge is supplied.

It is not a deployed integration or a replacement semantic platform. The code, fixed decision cases and limitations are inspectable here:
https://github.com/msaleme/salesforce-governed-ontology

Which case should force an agent to withhold an explanation in your domain?

### Walkthrough outline and demo script

1. State the ambiguity: “revenue” is not a unique definition.
2. Run `python3 explore.py scenario ambiguity`.
3. Run `python3 explore.py scenario approved-read` and point out that a plan is not execution.
4. Run `python3 explore.py scenario binding-mismatch`.
5. Run `python3 explore.py scenario difference-only`, then `python3 explore.py scenario explained`.
6. Show `python3 evaluate.py` and explain that all cases are synthetic, not held-out or vendor comparisons.
7. Link the gap ledger. Ask for one minimal counterexample, not a meeting or commercial inquiry.

### Measurement discipline

Record publication URL/date, linked commit, meaningful comments, independent reproduction reports, counterexamples accepted, and defects corrected. Keep self-runs separate from independent runs. Stars and views can describe reach, but do not prove adoption, accuracy or authority. No external baseline has been collected for this packet and no numeric growth forecast is offered.

### Reproduction packet

See the [one-command reproduction guide](RUN-GUIDE.md) and [captured synthetic demonstration](RUN-GUIDE.md). The transcript is regenerated and checked by CI. External reproduction remains unverified.


<a id="publication-record"></a>

## Distribution evidence: 2026-11-08

### Delivered

- [dev.to walkthrough](https://dev.to/mspro3210/a-correct-subtraction-is-not-an-explanation-j5f), published 2026-11-08 19:19:44 UTC, article ID 5000005.
- Links and commands pinned to reviewed merged commit `9747a4810b5312a62dce75b9b75bbce5a9e1f4a8` from PR #6. Clean detached-checkout verification passed before publication, including all article scenario commands and evaluation.
- Publication API read-back confirmed title, public URL and pinned commit in the body.
- The authenticated published-article list was checked immediately before publishing. Previous original: October 31, outside seven days. Recent 30-day titles/bodies were reviewed; none duplicated the financial explanation case.
- [Captured CLI demonstration](RUN-GUIDE.md) and [reproduction instructions](RUN-GUIDE.md) added in this follow-up. These are not part of the older pinned article checkout.

### Measure outcomes, not distribution alone

Publication is verified; independent reproduction and useful counterexamples are **not established**. No adoption or growth claim follows. Check the article and repository issues around November 22 for command-bearing reproduction reports and substantive counterexamples. This is a review date, not a scheduled model job. If there are no qualified responses, change the concrete case rather than repeat the thesis.

LinkedIn stays manual-only. Use the draft in [attention packet](PROJECT-NOTES.md#attention); do not automatically post it. Standards outreach remains held until actual mapping-loss evidence exists. No third-party repo promotion or private outreach was performed.

### Still requires owner inputs

- Platform owner, selected native metric/export version, designated sandbox and approved bindings/access.
- Finance review of the selected metric and any explanation evidence.
- Historical licensing blocker: resolved by the MIT license in PR #12; see [licensing decision](#licensing-decision).
- Independent contributor results. Maintainer and CI runs are not independent validation.


<a id="licensing-decision"></a>

## Licensing decision

The repository is licensed under the [MIT License](../LICENSE), copyright
2026 Michael Saleme. This supersedes the earlier no-license status and the
Apache-2.0 recommendation. Preserve the copyright and permission notice in
copies or substantial portions. No platform endorsement is implied.


<a id="article-draft"></a>

## A correct subtraction is not an explanation

**Source draft, published on dev.to on 2026-11-08.** The [published walkthrough](https://dev.to/mspro3210/a-correct-subtraction-is-not-an-explanation-j5f) uses absolute links and pins the verified merged commit. This file preserves the source narrative; not a claim of independent validation or vendor superiority.

An agent sees $1.2 million in contract bookings and $900,000 in recognized revenue. It subtracts correctly and then says the $300,000 difference is caused by unfulfilled performance obligations.

The arithmetic did not establish that explanation.

That distinction is the point of this small semantic decision testbed. It separates three questions: which metric did you mean, which read plan matches that definition, and what evidence supports explaining the difference?

### Run the distinction locally

Historical article source, updated for the packaged checkout: use Python 3.10 or later and install with `python3 -m pip install .` first. Installation fetches dependencies; commands then run offline without accounts, credentials or model endpoints.

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

### What to look for

**Ambiguity:** “revenue” produces `clarification_required`, offering bookings and recognized revenue rather than silently choosing one.

**Binding mismatch:** a recognized-revenue definition pointed at the bookings fixture produces `binding_mismatch`. A known source is not necessarily the right source for a metric.

**Difference only:** the aligned cohort produces `difference_only`, `currency: USD` and `difference_minor: 30000000`. Amounts are integer minor units, so that value is $300,000. There is no explanation field.

**Explained:** a separately supplied bridge with matching dimensions and amount produces `explained_by_fixture_bridge`. The result includes the bridge's source and stated reason. That bridge is synthetic. The program does not authenticate it or prove the accounting policy is correct.

A correct subtraction is not an explanation.

### Why another semantic example?

Existing semantic layers already define metrics and generate queries. Operational ontology platforms connect business objects to actions. Knowledge-graph systems support graph interchange and inference. Reimplementing those capabilities would not make this example stronger.

The narrower contribution is an inspectable acceptance test: make the decision and its evidence easy to challenge. The [comparison](COMPARISON.md) distinguishes these categories and documents where to reuse existing platforms.

The intended role is complementary. Keep authoritative metric definitions in the platform that owns them. Eventually, reproduce these acceptance cases against that native model instead of introducing a second source of truth.

### A passing label can hide a failing answer

An evaluator that checks only `difference_only` can pass a result with the wrong amount. It can also miss an invented explanation appended to that result.

The [fixed decision contract](ASSURANCE.md) now checks complete result objects: source, operation, amount, currency, evidence markers and unexpected fields. Mutation tests deliberately keep the status correct while corrupting important payload fields. The evaluator must reject those results.

This is regression evidence, not a vendor leaderboard or model accuracy score. The expected cases were authored with the prototype. They are not held out. Exact fixture agreement does not establish production correctness.

### The next useful contribution is a counterexample

Pick a case where this decision rule is insufficient. Could a matching bridge still describe the wrong accounting treatment? Could a metric mapping preserve its name but change its grain? What should happen when a lifecycle date is confused with the data period?

Use the repository's [counterexample issue form](https://github.com/msaleme/salesforce-governed-ontology/issues/new?template=decision-counterexample.yml). Include the commit, command, minimal synthetic input, actual result and the expected decision with a reason. A conceptual gap is welcome; distinguish it from an executable reproduction.

Do not include customer data, tokens or private metadata. One reproducible disagreement is more useful than a general endorsement.

### What remains unproven

No live metric execution, native-platform interoperability, authenticated authorization, independent reproduction or general accounting validation is demonstrated here. The [gap ledger](COMPARISON.md) keeps those boundaries explicit. This is a reference prototype, not an official vendor product; see [MIT license](../LICENSE) for reuse terms.
