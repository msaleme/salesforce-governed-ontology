# Financial services: proposed semantic reference architecture

[CTO brief](../CTO-ADVISORY.md) · [Pilot decision kit](../CTO-PILOT-KIT.md)

**Design hypothesis only.** No live industry integration, domain validation, deployment or standards conformance is established by this document. [License status](../../LICENSE-STATUS.md) is unchanged.

## Executive decision

**Question:** Why do two reports disagree on exposure to the same counterparty?

A legal entity is not its corporate group. Gross exposure, accounting balance and net exposure are different measures; collateral does not automatically imply legally eligible netting.

**Accountable owners:** Risk methodology owns exposure definitions; legal owns netting eligibility; finance owns ledger interpretation; data stewardship owns entity resolution.

## Domain model and system boundary

LegalEntity → group membership over time; Agreement → parties and eligible NettingSet; Position → instrument and counterparty; Valuation → as-of timestamp/currency; Collateral → eligibility and valuation.

Proposed data path: Position and valuation systems plus entity master → reviewed entity/agreement mappings → existing risk semantic model → policy-bound read adapter → evidence-linked report comparison.

Use the shared [trust-boundary architecture](../CTO-ADVISORY.md). Native sources retain authorization and data authority; the semantic catalog does not grant access. Resolve identifiers and effective-time relationships before aggregation. Do not join on display names.

## First decision contract

Freeze one exposure definition, valuation timestamp, legal-entity scope, currency conversion source and netting basis. Aggregate only after approved group membership and netting rules are applied; never infer eligibility from a shared parent name.

Record the contract revision, source schema revision, identity/purpose reference, freshness threshold, completeness observations and permitted answer type. Thresholds must be chosen by the domain owner before execution, not invented by an agent. These fields are design requirements, not supported inputs to the current CLI.

## Counterexamples and expected behavior

Challenge set: Same trading name for different legal entities; stale group membership; FX snapshots differ; collateral valuation is stale; netting eligibility missing; one report includes off-balance-sheet commitments.

Required behavior: Return a supported difference for aligned gross exposures. Clarify gross versus net requests. Withhold a net comparison if legal eligibility evidence is missing, even when arithmetic is possible.

Include a valid answerable control as well as refusals. Have a domain reviewer freeze expected complete results independently of implementation, then retain untouched cases for the final evaluation. The proposed behavior above is not a claim that existing tests cover this industry.

## Smallest credible pilot

One synthetic counterparty group, one valuation date and two frozen report extracts. Risk reviewer labels gross/net cases before implementation and holds back an entity-resolution counterexample.

Compare against the incumbent workflow on the same cases. Capture incorrect answers, false refusals, missing provenance and steward correction time. Progress only with a signed domain disposition, reviewed native bindings and the [shared sandbox gates](../CTO-PILOT-KIT.md). An offline synthetic pass cannot satisfy real identity-boundary proof.

## Non-goals and failure handling

No trading, credit approval, capital adequacy determination or regulatory filing. Enforce desk/legal-entity restrictions on both positions and relationship metadata.

On stale definitions, schema drift or unresolved identity, stop the affected read path and route to the named owner. Preserve a redacted failure receipt. Disable the adapter on an unauthorized disclosure; revalidate revoked versions and caches before resuming. A previous approved revision may be restored only if still valid and authorized.

## Reuse and standards mapping

FIBO and LEI identifiers are candidate semantic/identity inputs. They do not supply exposure calculation policy or prove netting eligibility. Record exact ontology revision and identifier source; do not claim FIBO conformance.

Review mappings field by field, retain explicit loss reports, and refuse required meaning that the selected exchange cannot represent. The current [SKOS export](../STANDARDS-EXPORT.md) exchanges vocabulary only, not these rules.

## Evidence boundary

Finance comparison controls are analogous only. No risk engine, netting evaluator, entity resolver or financial-services integration is implemented.

A credible next artifact is a steward-reviewed native mapping plus a reproducible counterexample, not an unverified claim of industry adoption. Submit synthetic evidence using the [team evaluation disposition](../TEAM-EVALUATION.md).
