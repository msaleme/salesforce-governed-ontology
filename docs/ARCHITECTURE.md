# Architecture, design decisions and roadmap

- [Architecture and implementation brief](#architecture)
- [Design decisions](#design-decisions)
- [Evidence-gated roadmap](#roadmap)

<a id="architecture"></a>

## Architecture and implementation brief

### 1. Ownership and boundaries

“Salesforce-governed” means definitions, versions, approvals, and action bindings are managed through a Salesforce-centered control plane. Business/domain stewards retain authority over their definitions. It does not mean Salesforce becomes the system of record for every ERP transaction, or that its policy overrides a source system's access controls.

Proposed responsibilities, not verified statements of available end-to-end functionality:

- **Salesforce semantic registry:** canonical concept IDs; definitions; domain extensions; version lifecycle; effective dates; approver evidence; source and action bindings.
- **Informatica adapter:** metadata identifiers, classifications, glossary candidates, lineage, quality observations, refresh timestamps. Imports propose mappings; they cannot approve themselves.
- **MuleSoft adapter:** versioned read/action APIs with bounded schemas, authenticated caller context, policies, runtime authorization, and receipts.
- **Semantic resolution service:** match a request to an approved definition, ask about ambiguity, assemble a bounded read plan, and package cited evidence. Deploy location is an open implementation choice.
- **Agentforce:** proposed conversational entry point and action consumer. The agent proposes a plan; deterministic services validate it.
- **Source systems:** authoritative transaction data and final source authorization.

```mermaid
flowchart TD
  A[Agentforce request] --> B[Semantic resolution service]
  B --> C[Salesforce governed registry]
  I[Informatica metadata and lineage] --> D[Candidate mappings]
  D --> E[Domain steward approval]
  E --> C
  B --> P[Authorization and plan validation]
  P --> M[MuleSoft governed read APIs]
  M --> S[CRM / ERP / operational sources]
  S --> R[Evidence and execution receipts]
  R --> B
  B --> A
```

### 2. Proposed registry implementation

Check existing platform capabilities first. If a custom registry is necessary, the following are **proposed custom objects**, not existing Salesforce standard objects:

- `BusinessConcept__c`: stable semantic ID, label, domain, description, steward.
- `ConceptVersion__c`: immutable definition payload/hash, version, status, effective interval, approval reference, superseded version.
- `SemanticRelationship__c`: source and target concept-version references, predicate, cardinality, temporal qualifiers.
- `SourceBinding__c`: concept-version reference, external catalog ID, source schema version, transformation, provenance, refresh policy.
- `ActionBinding__c`: concept-version reference, API/version/operation, input/output schema hashes, required scope, side-effect class.
- `SemanticDecision__c`: request/correlation ID, definition version, policy decision reference, source receipts, outcome; redact sensitive values and apply retention.

Use records for governed runtime definitions; use deployable configuration only for stable bootstrap settings. Storage, limits, sharing, retention, and deployment approach need sandbox validation. Do not store source credentials in ontology records.

Lifecycle: **draft → review → approved → deprecated/revoked**. Rejection returns to draft. Definition changes create a new immutable version, not silent edits. Production approvals require authenticated steward evidence. LLM suggestions and catalog imports remain drafts. Rollback selects an earlier still-valid approved version; it does not bypass revocation.

### 3. Oil & Gas scope

Model a graph, not a linear chain:

- Account participates in an OperatorRole; an operator is a business role, not universally a separate legal entity.
- OperatorRole operates an Asset for an effective interval; operation and ownership are separate predicates.
- Well is a specialization of Asset; IDs are namespaced and require verified cross-system mapping.
- ProductionObservation measures a Well for a period, commodity, quantity unit, and measurement basis.
- Contract links counterparties and covered assets; coverage can be many-to-many.
- RevenueEntry references a contract, account, accounting period, currency, and recognition basis.
- A production observation does **not** imply a revenue amount without prices, allocation, entitlement, and accounting rules.

The starter JSON is a lightweight semantic registry format, not an OWL reasoner or an industry-standard ontology. A later RDF/OWL or JSON-LD export is optional. Do not claim industry-standard alignment until mappings are reviewed.

### 4. Semantic contract

Every metric version needs: business definition; aggregation grain; time basis; unit/currency; exclusions; source binding; lineage; approval; effective interval; and action binding. Global concepts can have customer/domain extensions with explicit scope. Identical labels do not imply equivalent definitions.

For revenue, preserve distinctions among bookings, invoicing, cash receipts, and recognized revenue. Closed-won Opportunity Amount is only a possible bookings proxy, not automatically an approved accounting measure. The demo's booked metric is a synthetic contract-bookings fact, not a claim about Salesforce Opportunity semantics.

A runtime request carries authenticated principal context, semantic ID/version, operator ID, period, currency, and approved purpose. Caller-supplied permission strings are not trusted credentials. Effective access is the intersection of platform, API, source, row/field, and purpose restrictions. Authorization must apply to metadata visibility as well as values.

Response envelope: definition ID/version; approved definition excerpt; result grain; source record references; retrieval time; quality/freshness observations; policy/receipt IDs; limitations. Bind evidence to the query and identity. Do not cache across users or tenants without equivalent policy context and revalidation.

### 5. Adapter contracts (illustrative, not real vendor endpoints)

**Informatica → candidate mapping**

`catalogAssetId, catalogVersion, glossaryTermId, sourceFieldPath, lineageRefs[], classification, observedAt, qualityObservation, proposedConceptId`

Require stable external IDs, timestamps, schema compatibility, and steward review. Quality scores are observations with provenance, not a universal promise of trust. Unknown lineage or stale metadata is an explicit limitation.

**Registry → MuleSoft read plan**

`correlationId, conceptVersion, operationId, schemaVersion, parameters{operatorId, contractId, period, currency}, identityContextReference, purpose`

Identity reference must resolve to verified runtime identity, never a model-generated entitlement. Allowlisted operation IDs map to fixed API operations; do not execute arbitrary URLs or generated SQL. API returns a typed payload, source references, retrieval timestamp, and receipt. Handle pagination and partial results explicitly.

Future writes additionally require explicit action authority, bounded input, preview/approval where applicable, idempotency, and execution-time reauthorization. No writes in v0.1.

### 6. Proof sequence

1. **Now, local:** vocabulary and resolver; ambiguity, missing scope, stale definition, dimension mismatch, and unsupported causal explanation controls. Synthetic evidence only.
2. **Platform fit:** internal owner reviews existing semantic/data-model capability, storage choice, package boundaries, licenses, and API access. Produce an overlap/gap decision, not a parallel registry by default.
3. **Sandbox read path:** actual approved definition record, Informatica metadata binding, and read-only MuleSoft operation. Record real request/response schemas and version IDs.
4. **Identity proof:** two identities with differing permissions; demonstrate source denial, row/field restriction, metadata restriction, expired token, and no cross-user cache leakage. Local demo tests do not satisfy this gate.
5. **Business validation:** finance/domain steward signs off on grain, time basis, reconciliation bridge, exclusions, and definition lifecycle. Exercise stale metadata, identity mismatch, duplicate rows, pagination, and partial failure.
6. **Agentforce demonstration:** ask an ambiguous question, resolve it, explain a permitted result, and refuse an unauthorized read. Capture receipts before any readiness claim.

### 7. Decision log

- Salesforce-centered governance is the design objective specified by Michael.
- Original model, no NVIDIA dependency or copied implementation.
- Synthetic Oil & Gas revenue reconciliation is the first bounded scenario.
- Repository packaging and public GitHub visibility authorized on 2026-11-04. No external outreach, deployment, scheduled job, or org connection.
- Open: approved internal development location and org; existing semantic capability overlap; actual Informatica edition/API access; MuleSoft API contract; domain and finance approvers. These affect integration, not this local starter.


<a id="design-decisions"></a>

## Design decisions

These decisions describe the reference prototype. They are not claims of internal Salesforce approval or product commitments.

### ADR-001: Separate business meaning from execution authority

**Status:** accepted for the reference design.

**Context:** metadata, metric definitions, and API permissions solve different problems. Combining them can turn a plausible source mapping into apparent authority.

**Decision:** Salesforce-centered governance owns definition lifecycle in the proposed architecture. Informatica contributes metadata evidence. MuleSoft is the proposed integration plane. Agentforce consumes the approved context. Source permissions remain authoritative.

**Consequence:** a correct definition is necessary but insufficient to authorize a request. Live identity propagation must be proven separately.

### ADR-002: Start with a deterministic executable slice

Update: the packaged core now uses `jsonschema` for draft 2020-12 structural validation. The original zero-dependency choice below is historical; runtime commands remain offline after installation.

**Status:** implemented locally.

**Context:** connecting a model or org would obscure whether the basic semantic rules are correct and introduce setup barriers.

**Decision:** use Python standard-library fixtures with explicit statuses, no model calls, and no network. Demonstrate ambiguity, validity, scope checks, binding integrity, compatible grain, and bounded explanations.

**Consequence:** anyone with Python can reproduce the logic, but the result is not proof of natural-language understanding or platform integration. The JSON format is not an industry ontology standard.

### ADR-003: Bind metric, source, and operation as a single contract

**Status:** implemented locally.

**Context:** allowing an operation name in isolation permits the bookings metric to point at the recognized-revenue operation, or vice versa.

**Decision:** keep explicit expected triples in `validation.BINDINGS`. Validate registries offline and reject mismatched triples during resolution.

**Consequence:** the built-in tour retains its fixed metric/source/operation map. The separate `sgo byod` path accepts custom metric contracts from a file, validates their declared bindings and never executes them. These supplied bindings are unverified, not authenticated authority; a future live registry must supply versioned, authenticated bindings.

### ADR-004: Explain only what supplied evidence supports

**Status:** implemented locally.

**Context:** an arithmetic difference is not evidence of its cause.

**Decision:** without a matching bridge, return `difference_only`. With a compatible synthetic bridge, return its explanation and source reference. Reject incompatible dimensions.

**Consequence:** the demo cannot invent a cause. It also cannot verify the truth of the supplied bridge; authenticity and accounting correctness remain external responsibilities.

### ADR-005: Reuse platform semantics before adding custom objects

**Status:** proposed; platform-fit review pending.

**Context:** a parallel registry risks duplicating existing definitions, approvals, and controls.

**Decision:** first assess existing semantic capability and API coverage with a platform owner. Use custom objects only for demonstrated gaps.

**Consequence:** the architecture documents illustrative objects, not an installation package or a commitment to custom storage. See the [review packet](ASSURANCE.md).


<a id="roadmap"></a>

## Evidence-gated roadmap

### Available: offline reference prototype

- Lightweight vocabulary and two distinct metric definitions.
- Synthetic resolver, reconciliation, example output, and behavioral controls.
- Proposed architecture and platform-fit review packet.
- [Semantic change review](CHANGE-REVIEW.md): input fingerprints, version-drift detection and affected-record reporting.
- [Primary-source positioning](COMPARISON.md) and evidence-ranked improvement priorities.

### Available: optional sandbox preflight

The [read-only metadata probe](SANDBOX-INTEGRATION.md) checks sandbox classification and selected object/field visibility. Synthetic transport tests are included. Live connectivity and the metric read remain unverified. This is a prerequisite tool, not completion of the one-real-read milestone.

### Next: platform fit

A designated internal platform owner evaluates existing semantic capabilities, entitlements, API coverage, storage, and approved development location. Record a reuse, extend, or defer decision using the [review template](ASSURANCE.md). Proposed custom objects are not a default implementation decision.

**Exit evidence:** named owner, selected foundation, documented gaps, and designated sandbox.

### Then: one real read

Bind one finance-approved recognized-revenue definition to one actual Informatica metadata asset and one fixed read-only MuleSoft operation. Use synthetic or explicitly approved sandbox data.

**Exit evidence:** sanitized schema/version records, successful permitted read, denied restricted read, freshness and partial-result handling, and verified identity propagation.

### Then: agent consumption and reconciliation

Expose the validated read route through a supported Agentforce integration. Add the bookings definition and finance-approved reconciliation bridge only after the single-metric path is established.

**Exit evidence:** ambiguity handling, identity-isolated results, source receipts, lifecycle/revocation checks, and finance sign-off.

### Outside current scope

Production rollout, write actions, autonomous approval, broad ontology generation, standards conformance certification, and performance claims. Each requires separate implementation and evidence; no delivery dates are implied.

### Competitive gap closure (2026-11-08)

The [competitive gap ledger](COMPARISON.md) records implemented request/registry boundaries, availability-filtered clarification, bridge shape checks and the [fixed decision evaluation](ASSURANCE.md). Remaining priorities are pinned native semantic mapping, approved live identity/bindings, independent reproduction and native-platform validation. A new query engine or general graph runtime is not planned.
