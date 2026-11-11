# Energy / Oil & Gas: proposed semantic reference architecture

[CTO brief](../CTO-ADVISORY.md) · [Pilot decision kit](../CTO-PILOT-KIT.md)

**Design hypothesis only.** No live industry integration, domain validation, deployment or standards conformance is established by this document. [License status](../../LICENSE-STATUS.md) is unchanged.

## Executive decision

**Question:** Why did reported production increase while recognized revenue fell?

Production volume and recognized revenue have different units, time bases and allocation rules. Neither a join nor a subtraction establishes causation.

**Accountable owners:** Production accounting owns allocation and entitlement; finance owns recognition; asset stewardship owns effective ownership/operator mappings.

## Domain model and system boundary

Well / Asset → ProductionObservation; Asset → effective OperatorRole and OwnershipInterest; Contract → covered Asset; Allocation → entitled quantity; RevenueEntry → contract and accounting period.

Proposed data path: Historian and production accounting → reviewed well-ID and allocation mappings → native semantic catalog → read adapter → ERP revenue ledger. CRM account and contract context can enrich identity only after cross-system mapping review.

Use the shared [trust-boundary architecture](../CTO-ADVISORY.md). Native sources retain authorization and data authority; the semantic catalog does not grant access. Resolve identifiers and effective-time relationships before aggregation. Do not join on display names.

## Data request and runnable subset

Use the [data-to-proof readiness check](../DATA-TO-PROOF.md) for exact objects, fields, join keys, owners and actionable missing-evidence results. This is a narrow synthetic subset, not the full architecture below.

## First decision contract

Metric A: measured production at well/day/commodity with unit and measurement basis. Metric B: recognized revenue at contract/accounting-period/currency. Compare trends separately; reconcile money only with an approved quantity/price/allocation/recognition bridge.

Record the contract revision, source schema revision, identity/purpose reference, freshness threshold, completeness observations and permitted answer type. Thresholds must be chosen by the domain owner before execution, not invented by an agent. These fields are design requirements, not supported inputs to the current CLI.

## Counterexamples and expected behavior

Challenge set: Asset ownership changes mid-period; gross operated output is mislabeled as net entitlement; standard and actual volume bases differ; late allocation revisions; accounting close differs from production date.

Required behavior: Permit the valid same-currency, same-cohort revenue comparison. Withhold a production-to-revenue explanation when price, entitlement or recognition evidence is absent. Split effective ownership intervals rather than applying current ownership retroactively.

Include a valid answerable control as well as refusals. Have a domain reviewer freeze expected complete results independently of implementation, then retain untouched cases for the final evaluation. The proposed behavior above is not a claim that existing tests cover this industry.

## Smallest credible pilot

One operator, one closed accounting period and a sanitized contract cohort. Reconcile to a finance-approved ledger extract. Include an independently chosen asset with a mid-period ownership change.

Compare against the incumbent workflow on the same cases. Capture incorrect answers, false refusals, missing provenance and steward correction time. Progress only with a signed domain disposition, reviewed native bindings and the [shared sandbox gates](../CTO-PILOT-KIT.md). An offline synthetic pass cannot satisfy real identity-boundary proof.

## Non-goals and failure handling

No well-control writes, reserve certification, royalty payment or accounting-policy approval. Asset operations and counterparties may be commercially sensitive.

On stale definitions, schema drift or unresolved identity, stop the affected read path and route to the named owner. Preserve a redacted failure receipt. Disable the adapter on an unauthorized disclosure; revalidate revoked versions and caches before resuming. A previous approved revision may be restored only if still valid and authorized.

## Reuse and standards mapping

Energistics vocabulary/data standards and OSDU identifiers are candidate mapping inputs, not implemented or certified mappings. Pin the selected schema and have a domain steward review quantity, identity and effective-time losses.

Review mappings field by field, retain explicit loss reports, and refuse required meaning that the selected exchange cannot represent. The current [SKOS export](../STANDARDS-EXPORT.md) exchanges vocabulary only, not these rules.

## Evidence boundary

The existing finance fixture exercises two revenue definitions and a supplied reconciliation bridge. It does not compute production allocation, ownership entitlement or accounting policy.

A credible next artifact is a steward-reviewed native mapping plus a reproducible counterexample, not an unverified claim of industry adoption. Submit synthetic evidence using the [team evaluation disposition](../TEAM-EVALUATION.md).
