# Platform-fit decision packet

Internal working draft | 2026-11-03 | Continuation of SF-ONTOLOGY-001

## Decision requested from the internal platform owner

Where should governed business definitions and their approved source/action bindings live within the existing Salesforce architecture?

Recommendation: reuse the existing semantic/data-model foundation wherever it can meet the requirements below; add only missing governance and execution bindings. Do not create the six proposed custom objects merely because they appear in the starter design. This packet specifies evaluation criteria, not verified product capabilities.

## Preserve the ownership model

Salesforce is the proposed control plane for definition identity, approved versions, lifecycle and action bindings. Customer/domain stewards approve business meaning. Informatica contributes catalog and lineage evidence; MuleSoft supplies governed integrations; Agentforce consumes approved context and actions. Source systems retain transaction authority and access controls. “From Salesforce” describes the intended architecture, not a claim that this prototype is an official product or that IP ownership has been determined.

## Reuse-first evaluation

For each requirement, the reviewer records an existing feature/API, edition and entitlement, documentary evidence, sandbox result, and gap. All entries currently remain UNVERIFIED.

1. Stable semantic IDs and relationships: distinguish business concepts from physical tables and fields; preserve scoped customer/domain extensions.
2. Metric semantics: represent grain, period basis, currency, exclusions, aggregation and effective dates without relying on a display label.
3. Governed version lifecycle: retain immutable approved versions, approver identity and revocation; imports and agent suggestions cannot approve themselves.
4. External provenance: bind Informatica asset/version IDs and lineage timestamps to a specific definition version; flag stale or missing evidence.
5. API/action binding: resolve a semantic ID to an allowlisted MuleSoft operation and schema version, not generated URLs or unrestricted queries.
6. Access control: establish identity propagation and intersection of metadata, row, field, API and source restrictions; demonstrate denial as well as success.
7. Agent consumption: return a typed definition/evidence envelope and clarification for ambiguous metrics through a supported Agentforce integration route.
8. Operations: establish limits, retention, audit access, promotion between environments and rollback without reviving revoked definitions.

Decision outcomes:
- **Reuse:** existing capabilities satisfy the requirement with evidence.
- **Extend:** preserve the existing canonical model and add a bounded missing component.
- **Defer:** required authority, entitlement or capability is unavailable.

A second registry is justified only by a documented gap. Avoid separate canonical definitions in the catalog, agent prompt and Salesforce registry.

## First sandbox slice

Question: “What is recognized revenue for this operator and accounting period?”

Start with one metric and one read operation. Keep the two-metric bookings/recognized-revenue reconciliation as the second increment, after finance approves both definitions and the explanation bridge.

Required inputs, none assumed available:
- Designated development org and approved internal artifact location.
- Named platform owner and finance/domain steward.
- One approved metric version with grain, accounting period, currency and exclusions.
- One actual Informatica metadata asset, API contract and permitted read mechanism.
- One actual MuleSoft read operation with request/response schema and source references.
- Two sandbox identities with intentionally different access.
- Synthetic or specifically approved test records; no production data required.

Expected trace:
1. Resolve the request to the approved metric version; clarify an unqualified “revenue” request.
2. Validate parameters, definition state, metadata freshness and authenticated identity.
3. Invoke the fixed read operation with caller identity conveyed through the supported mechanism.
4. Preserve source authorization, handle partial/paginated responses explicitly and attach evidence.
5. Return a result only with the correct definition, scope, currency, period and source receipt.

## Acceptance evidence

Capture sanitized requests/responses, definition and schema versions, timestamps, principal aliases, policy outcomes and source references. Never record tokens.

Required cases:
- Permitted identity gets the expected fixture value and provenance.
- Restricted identity cannot obtain disallowed data or disallowed metadata.
- Ambiguous revenue request produces clarification, not a guessed metric.
- Revoked definition or incompatible binding prevents execution.
- Stale metadata, unavailable source and partial results are visible limitations, not complete answers.
- Repeating a request under the second identity does not reuse the first identity's protected cached result.

These are proposed acceptance cases, not executed tests. The existing 15 local controls establish only synthetic prototype behavior.

## Review disposition template

- Platform owner / review date:
- Existing semantic foundation selected:
- Evidence links and entitlement confirmation:
- Reused capabilities:
- Bounded gaps and extension location:
- Approved sandbox / artifact location:
- Finance steward and approved metric version:
- Informatica asset / MuleSoft operation:
- Identity propagation design:
- Decision: reuse / extend / defer
- Remaining blocker and owner:

## Current disposition

REVIEW READY, NOT PLATFORM VALIDATED. The existing starter is preserved. Repository packaging and public GitHub visibility were authorized on 2026-11-04. No org connection, platform object creation, API execution, or external platform review request was made.
