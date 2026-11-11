# Healthcare operations: proposed semantic reference architecture

[CTO brief](../CTO-ADVISORY.md) · [Pilot decision kit](../CTO-PILOT-KIT.md)

**Design hypothesis only.** No live industry integration, domain validation, deployment or standards conformance is established by this document. [License status](../../LICENSE-STATUS.md) is unchanged.

## Executive decision

**Question:** Why does the capacity dashboard show beds available while the unit cannot accept another patient?

Licensed, physical, staffed and immediately available beds are distinct. Operational capacity also depends on acuity, staffing, isolation and the observation time.

**Accountable owners:** Clinical operations owns capacity meaning and acceptable interpretation; staffing owns roster validity; privacy/security owners govern access; facilities owns location identity.

## Domain model and system boundary

Facility → Unit → Bed; Encounter → location interval; StaffingObservation → skill/shift/unit; AvailabilityObservation → status/reason/time. Relationships do not infer clinical suitability.

Proposed data path: Bed-management and staffing systems → reviewed facility/unit and time mappings → native operational semantic catalog → authorized read adapter → bounded capacity answer with freshness evidence.

Use the shared [trust-boundary architecture](../CTO-ADVISORY.md). Native sources retain authorization and data authority; the semantic catalog does not grant access. Resolve identifiers and effective-time relationships before aggregation. Do not join on display names.

## First decision contract

Use unit/observation-time grain, explicit bed-status exclusions and staffing coverage interval. Count available staffed beds only under a locally approved rule. Keep patient-level records outside the demonstration.

Record the contract revision, source schema revision, identity/purpose reference, freshness threshold, completeness observations and permitted answer type. Thresholds must be chosen by the domain owner before execution, not invented by an agent. These fields are design requirements, not supported inputs to the current CLI.

## Counterexamples and expected behavior

Challenge set: Discharged patient still occupies a bed awaiting turnover; stale staffing roster; midnight shift boundary; isolation capacity excludes nominal beds; facility IDs collide; missing unit feed looks like zero occupancy.

Required behavior: Clarify physical versus staffed availability. Withhold a complete unit capacity answer when occupancy or staffing feeds are stale or incomplete. A capacity count never recommends an individual placement.

Include a valid answerable control as well as refusals. Have a domain reviewer freeze expected complete results independently of implementation, then retain untouched cases for the final evaluation. The proposed behavior above is not a claim that existing tests cover this industry.

## Smallest credible pilot

One fictional facility and two units using synthetic aggregate observations. Operations steward supplies one complete case, one stale-feed case and one restriction-sensitive case, with expected interpretations.

Compare against the incumbent workflow on the same cases. Capture incorrect answers, false refusals, missing provenance and steward correction time. Progress only with a signed domain disposition, reviewed native bindings and the [shared sandbox gates](../CTO-PILOT-KIT.md). An offline synthetic pass cannot satisfy real identity-boundary proof.

## Non-goals and failure handling

No clinical recommendation, triage, automated placement or protected patient data in public artifacts. A successful count does not establish privacy compliance or clinical safety.

On stale definitions, schema drift or unresolved identity, stop the affected read path and route to the named owner. Preserve a redacted failure receipt. Disable the adapter on an unauthorized disclosure; revalidate revoked versions and caches before resuming. A previous approved revision may be restored only if still valid and authorized.

## Reuse and standards mapping

HL7 FHIR resources are candidate exchange inputs, not a ready-made staffed-capacity model. Select a specific release and local profile; record where occupancy, staffing and availability meaning requires extensions. No FHIR conformance claim.

Review mappings field by field, retain explicit loss reports, and refuse required meaning that the selected exchange cannot represent. The current [SKOS export](../STANDARDS-EXPORT.md) exchanges vocabulary only, not these rules.

## Evidence boundary

Reliability examples illustrate completeness and window checks only. Healthcare terms, staffing rules and capacity calculations are not implemented.

A credible next artifact is a steward-reviewed native mapping plus a reproducible counterexample, not an unverified claim of industry adoption. Submit synthetic evidence using the [team evaluation disposition](../TEAM-EVALUATION.md).
