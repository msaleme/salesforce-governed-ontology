# Design decisions

These decisions describe the reference prototype. They are not claims of internal Salesforce approval or product commitments.

## ADR-001: Separate business meaning from execution authority

**Status:** accepted for the reference design.

**Context:** metadata, metric definitions, and API permissions solve different problems. Combining them can turn a plausible source mapping into apparent authority.

**Decision:** Salesforce-centered governance owns definition lifecycle in the proposed architecture. Informatica contributes metadata evidence. MuleSoft is the proposed integration plane. Agentforce consumes the approved context. Source permissions remain authoritative.

**Consequence:** a correct definition is necessary but insufficient to authorize a request. Live identity propagation must be proven separately.

## ADR-002: Start with a deterministic, dependency-free executable slice

**Status:** implemented locally.

**Context:** connecting a model or org would obscure whether the basic semantic rules are correct and introduce setup barriers.

**Decision:** use Python standard-library fixtures with explicit statuses, no model calls, and no network. Demonstrate ambiguity, validity, scope checks, binding integrity, compatible grain, and bounded explanations.

**Consequence:** anyone with Python can reproduce the logic, but the result is not proof of natural-language understanding or platform integration. The JSON format is not an industry ontology standard.

## ADR-003: Bind metric, source, and operation as a single contract

**Status:** implemented locally.

**Context:** allowing an operation name in isolation permits the bookings metric to point at the recognized-revenue operation, or vice versa.

**Decision:** keep explicit expected triples in `validation.BINDINGS`. Validate registries offline and reject mismatched triples during resolution.

**Consequence:** introducing a new metric requires deliberate code and fixture updates, not only editing a JSON label. A future registry must supply versioned, authenticated bindings instead of relying on this two-metric hardcoded map.

## ADR-004: Explain only what supplied evidence supports

**Status:** implemented locally.

**Context:** an arithmetic difference is not evidence of its cause.

**Decision:** without a matching bridge, return `difference_only`. With a compatible synthetic bridge, return its explanation and source reference. Reject incompatible dimensions.

**Consequence:** the demo cannot invent a cause. It also cannot verify the truth of the supplied bridge; authenticity and accounting correctness remain external responsibilities.

## ADR-005: Reuse platform semantics before adding custom objects

**Status:** proposed; platform-fit review pending.

**Context:** a parallel registry risks duplicating existing definitions, approvals, and controls.

**Decision:** first assess existing semantic capability and API coverage with a platform owner. Use custom objects only for demonstrated gaps.

**Consequence:** the architecture documents illustrative objects, not an installation package or a commitment to custom storage. See the [review packet](PLATFORM-FIT-REVIEW.md).
