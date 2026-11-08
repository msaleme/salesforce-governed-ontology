# Evidence-led attention packet

Status: **draft distribution assets, not published outreach**. The goal is qualified reproduction and counterexamples, not traffic or sales. This is a reference prototype, not an official vendor product or a project with a granted open-source license.

## The memorable idea

**A correct subtraction is not an explanation.**

Lead with a familiar failure: contract bookings and recognized revenue differ; the agent explains why without evidence. Show the refusal and the evidence needed to move beyond it. The [decision evaluation](EVALUATION.md) gives a reader something concrete to run and challenge.

## Repository improvements included

- [Comparison](COMPARISON.md): explicit alternatives, reuse decisions, trade-offs and remaining gaps.
- [Evaluation](EVALUATION.md): a reproducible result with both successful and refused decisions.
- [Counterexample form](../.github/ISSUE_TEMPLATE/decision-counterexample.yml): a structured path to contribute an observed failure.
- README entry points: one positioning statement and direct links to the evidence and contribution path.

- [Complete technical article draft](ARTICLE-DRAFT.md): runnable narrative, expected outcomes and a narrow counterexample request.

## Proposed distribution experiments

These are proposed actions, not scheduled jobs or promises of delivery. Post only after the reviewed code is available on the linked default branch, or link an immutable reviewed commit and identify it as a candidate.

| Priority | Surface and artifact | Audience hypothesis | Outcome to measure | Stop/change rule |
| --- | --- | --- | --- | --- |
| 1 | One manual LinkedIn post using the draft below | Analytics/platform owners recognize the bookings-versus-revenue failure | Substantive counterexample or independently reported reproduction | After 14 days, if no qualified response, change the concrete case instead of reposting the thesis |
| 2 | One dev.to walkthrough: “A correct subtraction is not an explanation” | Engineers want inspectable agent decision controls | Reported commands/results and actionable issues, not page views alone | If visits arrive but no reproductions, simplify the run instructions and ask one narrower technical question |
| 3 | A short synthetic terminal demonstration linked from the walkthrough | Readers need to see refusal and success in the same flow | Reproduction reports citing the demonstrated cases | Do not claim a video exists until recorded and checked |
| 4 | A neutral standards mapping note after adapter evidence exists | Interoperability reviewers care about lost temporal/action semantics | Concrete mapping correction or accepted technical feedback | Hold until a reproducible mapping loss exists; do not post project plugs on third-party repos |

Before any original post, check that surface's last 7 days and the last 30 days for a near-duplicate thesis; at most one original post per surface per week. Do not auto-post LinkedIn, create empty GitHub Discussions, or promote on third-party issue threads. No outreach or publication has been performed by this change.

## LinkedIn draft

An agent sees contract bookings of $1.2 million and recognized revenue of $900,000.

The difference is $300,000. That does not tell it why.

A correct subtraction is not an explanation.

I built a small synthetic reference that makes the distinction explicit: clarify the revenue definition, validate the read plan, and report only the difference unless a matching explanation bridge is supplied.

It is not a deployed integration or a replacement semantic platform. The code, fixed decision cases and limitations are inspectable here:
https://github.com/msaleme/salesforce-governed-ontology

Which case should force an agent to withhold an explanation in your domain?

## Walkthrough outline and demo script

1. State the ambiguity: “revenue” is not a unique definition.
2. Run `python3 explore.py scenario ambiguity`.
3. Run `python3 explore.py scenario approved-read` and point out that a plan is not execution.
4. Run `python3 explore.py scenario binding-mismatch`.
5. Run `python3 explore.py scenario difference-only`, then `python3 explore.py scenario explained`.
6. Show `python3 evaluate.py` and explain that all cases are synthetic, not held-out or vendor comparisons.
7. Link the gap ledger. Ask for one minimal counterexample, not a meeting or commercial inquiry.

## Measurement discipline

Record publication URL/date, linked commit, meaningful comments, independent reproduction reports, counterexamples accepted, and defects corrected. Keep self-runs separate from independent runs. Stars and views can describe reach, but do not prove adoption, accuracy or authority. No external baseline has been collected for this packet and no numeric growth forecast is offered.
