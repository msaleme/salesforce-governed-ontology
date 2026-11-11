# Manufacturing: proposed semantic reference architecture

[CTO brief](../CTO-ADVISORY.md) · [Pilot decision kit](../CTO-PILOT-KIT.md)

**Design hypothesis only.** No live industry integration, domain validation, deployment or standards conformance is established by this document. [License status](../../LICENSE-STATUS.md) is unchanged.

## Executive decision

**Question:** Why do two plants report different equipment effectiveness for apparently similar output?

OEE depends on approved availability, performance and quality definitions. Different planned-time exclusions, ideal rates or rework rules make the resulting percentages incomparable.

**Accountable owners:** Plant operations owns planned time and downtime classification; engineering owns ideal rates; quality owns good-count and rework rules.

## Domain model and system boundary

Site → Line → Equipment; WorkOrder → product and schedule; Run → time interval; DowntimeEvent → reason; QualityObservation → inspected/good/rework counts; RateDefinition → product/equipment/revision.

Proposed data path: MES, historian and quality systems → reviewed equipment/order and event-time mappings → native manufacturing semantic model → read-only adapter → bounded comparison and evidence receipt.

Use the shared [trust-boundary architecture](../CTO-ADVISORY.md). Native sources retain authorization and data authority; the semantic catalog does not grant access. Resolve identifiers and effective-time relationships before aggregation. Do not join on display names.

## First decision contract

For the pilot, define availability as runtime/planned production time, performance as ideal cycle time × total count/runtime, and quality as good count/total count. Require compatible duration units, positive denominators and steward-approved exclusions. This proposed formula is not repository executable behavior.

Record the contract revision, source schema revision, identity/purpose reference, freshness threshold, completeness observations and permitted answer type. Thresholds must be chosen by the domain owner before execution, not invented by an agent. These fields are design requirements, not supported inputs to the current CLI.

## Counterexamples and expected behavior

Challenge set: Mixed products with different ideal rates; microstops excluded in one plant; rework counted twice; overlapping downtime; zero planned time; missing quality sample; performance above one due to invalid ideal rate.

Required behavior: Return factors only for a valid aligned run. Reject overlapping durations, invalid denominators and duplicate counts. Escalate implausible factors rather than silently capping them. Do not identify a failure cause from an OEE decline alone.

Include a valid answerable control as well as refusals. Have a domain reviewer freeze expected complete results independently of implementation, then retain untouched cases for the final evaluation. The proposed behavior above is not a claim that existing tests cover this industry.

## Smallest credible pilot

One line, one product and one completed shift in synthetic MES extracts. Reconcile durations/counts manually with operations and quality; hold out a rework double-count and schedule-exclusion case.

Compare against the incumbent workflow on the same cases. Capture incorrect answers, false refusals, missing provenance and steward correction time. Progress only with a signed domain disposition, reviewed native bindings and the [shared sandbox gates](../CTO-PILOT-KIT.md). An offline synthetic pass cannot satisfy real identity-boundary proof.

## Non-goals and failure handling

No PLC commands, safety interlock changes, predictive-maintenance action or production scheduling writes. Separate operational technology from the advisory read path.

On stale definitions, schema drift or unresolved identity, stop the affected read path and route to the named owner. Preserve a redacted failure receipt. Disable the adapter on an unauthorized disclosure; revalidate revoked versions and caches before resuming. A previous approved revision may be restored only if still valid and authorized.

## Reuse and standards mapping

ISA-95 / IEC 62264 are candidate conceptual references for enterprise/control boundaries. Select applicable versions and licensed source material where needed. This blueprint does not claim standards conformity.

Review mappings field by field, retain explicit loss reports, and refuse required meaning that the selected exchange cannot represent. The current [SKOS export](../STANDARDS-EXPORT.md) exchanges vocabulary only, not these rules.

## Evidence boundary

The reliability contract supplies a useful refusal pattern, not an OEE engine. Equipment identities, event reconciliation and manufacturing metrics require new reviewed implementation.

A credible next artifact is a steward-reviewed native mapping plus a reproducible counterexample, not an unverified claim of industry adoption. Submit synthetic evidence using the [team evaluation disposition](../TEAM-EVALUATION.md).
