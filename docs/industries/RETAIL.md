# Retail / distribution: proposed semantic reference architecture

[CTO brief](../CTO-ADVISORY.md) · [Pilot decision kit](../CTO-PILOT-KIT.md)

**Design hypothesis only.** No live industry integration, domain validation, deployment or standards conformance is established by this document. [License status](../../LICENSE-STATUS.md) is unchanged.

## Executive decision

**Question:** Why is one dashboard reporting strong delivery performance while customers report missed promises?

On-time shipment is not on-time delivery. Order, line and package denominators differ, and measuring against a revised promise can hide failure against the original promise.

**Accountable owners:** Fulfillment operations owns service definitions; customer operations owns promise interpretation; data stewardship owns order-line/shipment identity.

## Domain model and system boundary

Order → OrderLine → fulfillment allocations; Shipment → Package → DeliveryEvent; PromiseVersion → line and effective time; Return → original line; InventoryObservation → location/time.

Proposed data path: OMS, WMS and carrier events → reviewed line/package mappings and original-promise history → existing semantic model → authorized read adapter → comparison with coverage and late-event evidence.

Use the shared [trust-boundary architecture](../CTO-ADVISORY.md). Native sources retain authorization and data authority; the semantic catalog does not grant access. Resolve identifiers and effective-time relationships before aggregation. Do not join on display names.

## First decision contract

Freeze whether the metric is line-level or order-level and original versus revised promise. Define timezone, delivery event, cancellations, split shipments and observation cutoff. Require all required lines before calling an order delivered on time.

Record the contract revision, source schema revision, identity/purpose reference, freshness threshold, completeness observations and permitted answer type. Thresholds must be chosen by the domain owner before execution, not invented by an agent. These fields are design requirements, not supported inputs to the current CLI.

## Counterexamples and expected behavior

Challenge set: One timely package hides a late split shipment; carrier event arrives after cutoff; revised promise overwrites original; cancelled lines remain in denominator; local midnight differs from UTC; duplicate delivery scans.

Required behavior: Clarify shipped versus delivered and original versus revised promise. Mark late/missing carrier evidence incomplete. Deduplicate by reviewed event identity. A high line-level rate must not be relabeled order-level performance.

Include a valid answerable control as well as refusals. Have a domain reviewer freeze expected complete results independently of implementation, then retain untouched cases for the final evaluation. The proposed behavior above is not a claim that existing tests cover this industry.

## Smallest credible pilot

One fictional fulfillment node and a closed order cohort with synthetic carrier events. An operations reviewer independently labels split shipments, revised promises and late-arriving events.

Compare against the incumbent workflow on the same cases. Capture incorrect answers, false refusals, missing provenance and steward correction time. Progress only with a signed domain disposition, reviewed native bindings and the [shared sandbox gates](../CTO-PILOT-KIT.md). An offline synthetic pass cannot satisfy real identity-boundary proof.

## Non-goals and failure handling

No automatic refunds, order changes or inventory allocation. Avoid customer addresses and identity in receipts; source systems remain authoritative for customer access.

On stale definitions, schema drift or unresolved identity, stop the affected read path and route to the named owner. Preserve a redacted failure receipt. Disable the adapter on an unauthorized disclosure; revalidate revoked versions and caches before resuming. A previous approved revision may be restored only if still valid and authorized.

## Reuse and standards mapping

GS1 EPCIS is a candidate event-exchange input, not an on-time-delivery metric definition. Pin the event schema and preserve event/record time distinctions; map business promises separately. No EPCIS integration or certification is established.

Review mappings field by field, retain explicit loss reports, and refuse required meaning that the selected exchange cannot represent. The current [SKOS export](../STANDARDS-EXPORT.md) exchanges vocabulary only, not these rules.

## Evidence boundary

Existing examples do not implement fulfillment metrics or carrier ingestion. They demonstrate analogous dimension and incomplete-evidence checks only.

A credible next artifact is a steward-reviewed native mapping plus a reproducible counterexample, not an unverified claim of industry adoption. Submit synthetic evidence using the [team evaluation disposition](../TEAM-EVALUATION.md).
