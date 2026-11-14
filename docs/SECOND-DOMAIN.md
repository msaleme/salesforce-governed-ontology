# Second domain: service reliability

Run `python3 reliability.py`. Eight fixed synthetic cases compare complete structured results against reviewed expected outputs in [the fixture](../examples/reliability-cases.json).

## Different problem, same evidence discipline

Finance compares integer monetary amounts from an aligned cohort. Reliability compares a request-success ratio against a versioned service objective. It has a denominator, sampling coverage, a time window and an eligible population; neither currency nor an accounting bridge applies.

At 9,990 successful requests out of 10,000 and a 99.90% objective, the objective is met. At 9,989 it is missed. At incomplete coverage or zero requests, neither conclusion is established. A latency objective cannot be evaluated using request-success counts. A missed objective never establishes a cause.

The implementation uses exact integer cross-multiplication, not rounded display percentages. Objective and observation must match on service, UTC window and population. Windows are half-open: start inclusive, end exclusive. The caller supplies aggregate counts for that window; the code does not verify raw events, detect duplicated events or authenticate coverage.

## What generalizes

- Validate evidence before computing a decision.
- Align dimensions before comparing values.
- Distinguish unavailable evidence from a negative result.
- Return provenance and version alongside a positive decision.
- Do not infer causes from arithmetic.

## What does not generalize

This is a separate bounded decision contract, not a new metric accepted by the financial resolver. No shared arbitrary-domain engine is claimed. The finance registry's grain, scope, binding rules and accounting assumptions remain finance-specific. Reliability needs its own count validity, denominator, completeness and threshold logic. A native monitor integration would need authenticated observations, deduplication, authoritative objective history and coverage validation.

All cases are maintainer-authored synthetic examples, not a statistical benchmark or independent domain validation. See [the evaluation packet](ASSURANCE.md#team-evaluation) for how to challenge them.
