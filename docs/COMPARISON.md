# Competitive landscape and positioning

Research date: **2026-11-08**. Author: Michael K. Saleme.

## Executive decision

**Position this as a reproducible semantic decision testbed, not another enterprise ontology platform.** Its current deliverable is a small inspectable contract: when to clarify business meaning, refuse a read plan, and withhold an unsupported explanation. The architecture remains Salesforce-centered; the runnable evidence is synthetic Python.

The crowded claim is “trusted business context for agents.” The more defensible contribution is a runnable collection of decision failures and expected outcomes that a platform owner can inspect and eventually reproduce against an existing semantic foundation.

**Reuse first:** evaluate Tableau Semantics in a Salesforce-centered environment. Where a warehouse or semantic layer already owns a metric, reference its identity and approved definition rather than create a competing source of truth. Do not build a query engine, authorization service or general knowledge graph to support this example.

## Method and evidence limits

This is a primary-source **documentation comparison**, not a hands-on product benchmark, procurement recommendation or exhaustive market census. Product capabilities below are claims in the linked official documentation. We did not run the vendors, inspect customer entitlements, or measure quality, speed, cost or market share. Silence in a source is not proof of a missing capability.

All linked sources were fetched on the research date. dbt, Snowflake and SHACL extractions were partial; only statements present in those extracts are used. W3C's Recommendation URL returned HTTP 403; the W3C-maintained specification source was read instead. The OSI row describes an announcement, not independently verified conformance. Product versions and documentation can change.

## The space is several markets, not one

| Category | Primary-source evidence | Contrast with this repository | Decision |
| --- | --- | --- | --- |
| Salesforce-native semantics | [Tableau Semantics](https://www.salesforce.com/analytics/tableau-semantics/) describes reusable models/metrics, certification, lineage/access controls, agent business context and Data 360 integration. | Our small registry and fixture approval are not equivalent to that platform or its governance. | First platform-fit candidate; reuse existing semantic identity and stewardship. |
| Operational ontology | [Palantir Ontology](https://www.palantir.com/docs/foundry/ontology/overview) combines objects, properties and links with actions, functions, dynamic security and applications. | We return a fixed read plan and never execute an operational action. No application platform, digital twin runtime or dynamic security. | Borrow separation of meaning and action; do not compete on platform breadth. |
| Transformation-adjacent metric semantics | [dbt semantic models](https://docs.getdbt.com/docs/build/semantic-models) describes MetricFlow's semantic graph, entities, dimensions and metric configuration. The retrieved format is labeled v1.12 and later. | We do not generate SQL, plan joins or execute warehouse metrics. Versioned JSON alone is not a differentiator. | Reuse upstream definitions and grain; pin actual export version before mapping. |
| API-first semantic layer | [Cube](https://docs.cube.dev/docs/introduction) describes code-first metrics/joins, access rules, pre-aggregation caching, SQL/REST/GraphQL interfaces and agent-facing APIs. | Code review, agent grounding and deterministic validation are already established themes. Our advantage is inspection simplicity, not richer APIs or stronger controls. | Avoid an API/runtime rebuild. Use decision cases as an integration acceptance packet. |
| Warehouse-native semantics | [Snowflake Semantic Views](https://docs.snowflake.com/en/user-guide/views-semantic/overview) stores logical entities, relationships, facts, dimensions and metrics as schema-level objects, with SQL queries and Cortex consumption. | Our fixture IDs contain no physical SQL expressions, table mapping or query runtime. | Prefer the warehouse-owned metric where appropriate; preserve its native access boundary. |
| Lakehouse-native metrics | [Databricks Unity Catalog metric views](https://docs.databricks.com/aws/en/uc-semantics/metric-views) centralizes measures/dimensions, runtime computation, access/lifecycle management and agent metadata. | Our fixed cohort and sum operation do not match general grouping, joins or materialization. | Do not imply synonyms or metric governance are unique; test grain and aggregation compatibility explicitly. |
| Formal graph constraints | [W3C SHACL specification source](https://w3c.github.io/data-shapes/shacl/) defines shapes for validating RDF graphs. | Our concept/relationship JSON is neither RDF nor SHACL; the Python validator is a bounded fixture validator, not a reasoner. | If graph interchange becomes required, map vocabulary first and validate with an actual standards implementation. |
| Data contracts | [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) defines YAML contract sections including schema, quality, roles, SLAs and authoritative definitions. | Our semantic contract has narrower decision rules and lacks ODCS serialization/conformance, quality monitoring and service-level management. | Reference upstream data contracts rather than invent their quality and ownership fields again. |
| Semantic interchange | [OSI announcement](https://www.snowflake.com/en/blog/open-semantic-interchanges-specs-finalized/) describes a vendor-neutral representation of datasets, metrics, dimensions, relationships and contexts. | Our bespoke JSON is not OSI. No converter, round trip or certification exists. | Track the actual specification and pin a revision before implementing an adapter; an interchange sidecar must not silently drop our refusal rules. |

## Knowledge graphs and established BI semantics: extended review

The following additional primary sources were fetched on **2026-11-08**. Stardog, GraphDB and Looker extracts were partial; the statements below appear in the retrieved text. Neo4j's Labs page was retrieved in full after an older documentation URL returned 404. These are documentation observations, not installed-product results.

| Foundation | Verified documentation claim | Contrast and reuse decision |
| --- | --- | --- |
| [Stardog inference engine](https://docs.stardog.com/inference-engine/) | Infers types and relationships from RDFS/OWL axioms and user rules, using query-time rewriting rather than materializing inferences. | Our code does not infer new graph facts. Reuse a reasoner if formal entailment is required; evaluate the resulting decision separately. An inferred relationship is not automatically financial explanation evidence. |
| [GraphDB 11.0 reasoning](https://graphdb.ontotext.com/documentation/11.0/reasoning.html) | Forward-chaining RDF entailment rules and total materialization compute inferred statements with configured rulesets at load time. | We have no RDF store, load-time closure or inference maintenance. The query-time versus materialization trade-off belongs to a graph-platform decision, not our fixed Python registry. |
| [Neo4j Labs neosemantics](https://neo4j.com/labs/neosemantics/) | RDF import/export, ontology/taxonomy vocabularies, SHACL validation and basic inferencing. The page limits this plugin to self-hosted Neo4j, not Aura. | Our JSON has no RDF interoperability. A future graph adapter must pin deployment and plugin versions, not assume all Neo4j installations expose the same capabilities. SHACL validates graph constraints; it does not by itself establish authenticated approval. |
| [Looker / LookML](https://docs.cloud.google.com/looker/docs/what-is-lookml) | Models dimensions, aggregates, calculations and relationships; uses those models to construct database SQL. Projects are typically Git-versioned. | Git-managed definitions and reusable semantics are established capabilities, not our novelty. Preserve the existing LookML metric and join logic rather than rebuild them in this registry. |

Catalog and lineage platforms, including Informatica, remain architectural dependencies rather than products evaluated here. Domain-specific ontologies, AtScale and automatic ontology generation remain outside this bounded review. No claim of market completeness follows.

### Three meanings of “ontology” that must not be conflated

1. **Formal inference:** What facts follow from the asserted graph and axioms? Stardog and GraphDB address this category; their documented inference strategies differ.
2. **Operational or analytical meaning:** Which objects, metrics, relationships and operations represent the business? Palantir and semantic-layer platforms address different parts of this category.
3. **Decision acceptance:** Given a selected meaning and evidence, should this request clarify, produce a read plan, or withhold an explanation? This repository provides a small synthetic example of this category.

They can be composed. None substitutes automatically for the others. Our use of “ontology” describes a lightweight business vocabulary, not OWL conformance or an inference engine.

### Build, borrow, defer

- **Build now:** richer decision assertions and minimal counterexamples. Inspect exact sources, operations, amounts, provenance and absence of unsupported explanation, not just a success/refusal label.
- **Borrow next:** native metric identity and definitions from the existing platform. Select one platform with its owner before building multiple adapters.
- **Defer until evidence requires it:** graph persistence, inference, query compilation, broad domain modeling and action execution. These would turn a small acceptance testbed into an unvalidated platform rebuild.
- **Do not claim closed:** interoperability, authenticated authorization, accounting correctness or independent validation. Those require separate evidence, not another documentation page.


## Compare the implemented approach, not the aspiration

| Dimension | Implemented here | What a production foundation must supply |
| --- | --- | --- |
| Business meaning | Two distinct fixture metrics, fixed grain/unit, seven concepts and seven relationships | Authoritative metric identity, financial ownership and approved accounting semantics |
| Decision control | Clarification, lifecycle/date checks, exact source/operation matching; whole-registry validation before plans | Real caller identity, native data permissions and runtime policy enforcement |
| Change governance | Snapshot diff, changed-record reporting, version-drift refusal and input hashes | Authenticated approvals, immutable history and operational rollout/rollback |
| Explanation discipline | Only arithmetic without a matching fixture bridge | Authentic source evidence and verified financial reconciliation |
| Interoperability | Human-readable crosswalk and explicit loss register below | Version-pinned platform export, adapter tests and round-trip evidence |
| Evaluation | Fixed synthetic decision cases, negative controls and reproducible receipt | Held-out cases, independent reproduction and identity-bound live trials |
| Delivery | Dependency-free offline Python; optional metadata probe | Supported integration, observability, freshness checks and lifecycle ownership |

These are not vendor feature scores. Our read-plan checks do not establish a security boundary; hashes do not establish approval or authenticity.

## Strategic assessment

### VRIO: where an advantage could come from

- **Valuable:** making a wrong-definition or unsupported-explanation failure easy to reproduce can help platform owners review agent behavior. This value is a hypothesis until independently used.
- **Rare:** not established. The inspected platforms already address semantics and governance. We have no evidence that the individual checks are unique.
- **Hard to imitate:** no. The small codebase is readily reproducible. A future body of independently contributed counterexamples and cross-platform reproductions could be harder to replicate; it does not exist yet.
- **Organized to capture value:** tests and CI exist; licensing/ownership clearance, adapters, live evidence and external adoption remain unresolved.

**Verdict:** a useful reference and research contribution, not a defensible platform moat today.

### Competitive forces

- **Substitution is the main pressure:** teams can use existing platform semantics and ordinary CI. Demonstrate incremental review value, not generic feature parity.
- **Platform dependence is real:** adapters depend on access, entitlement, API version and canonical ownership. Keep the core small and explicit about what is unproven.
- **Switching incentive should be zero:** this should help validate the platform a team already uses, not require moving metrics to another catalog.
- **Standards reduce format differentiation:** prefer portable cases and explicit semantic loss reporting over a proprietary registry schema.

## Gap-closing ledger

| Priority | Gap | Action and status | Acceptance evidence |
| --- | --- | --- | --- |
| P0 | Changed meaning hidden behind unchanged versions | Implemented in this PR: [change review](CHANGE-REVIEW.md) | Version-drift, binding, removal and malformed-JSON tests |
| P0 | Planner could accept a scope string or crash on malformed registry content | Implemented in this PR: validate request shape and complete registry before any plan/choices; preserve specific refusal statuses | [Boundary regressions](../test_boundaries.py), including malformed unselected records and duplicate identities |
| P0 | Clarification could suggest expired or revoked definitions | Implemented in this PR: only approved, date-valid registry choices are offered | Revocation and expiry negative controls |
| P0 | Unsupported bridge types could crash or look like explanation evidence | Implemented in this PR: object checks and nonempty textual bridge source/reason | Reconciliation boundary controls; authenticity remains unproven |
| P1 | Claims lacked a compact, reproducible decision scorecard | Implemented in this PR: [12-case contract evaluation](EVALUATION.md), input/code hashes and CI receipt parity | Includes successful read/explanation controls as well as refusals; not a vendor benchmark |
| P1 | Visitors lacked a focused way to contribute evidence | Implemented in this PR: [attention packet](ATTENTION.md) and counterexample issue form | Reproduction steps and claim limits required; no audience response claimed |
| P1 | Status-only evaluation could miss wrong amounts, sources or unsupported explanations | Closed in follow-up: exact, type-sensitive expected-result comparison and mutation controls | Wrong-source/operation, wrong-amount, extra-explanation, missing-provenance, narrowed-choice and refusal-disclosure mutations fail evaluation |
| P1 | No standards/platform interchange | Documented, not implemented: mapping and loss register below | Future adapter must preserve units, grain, temporal semantics and evidence boundaries, and fail unsupported mappings |
| P1 | No live identity or metric execution proof | Blocked on designated sandbox, approved bindings and access | Allowed/denied real identities, source reconciliation and sanitized receipts |
| P2 | No independent evaluation or broad domain model | Open | External reproduction, held-out cases and steward-reviewed domain expansion |
| P2 | No open-source license determination | Open; see [license status](../LICENSE-STATUS.md) | Owner-approved licensing/ownership decision, not an agent assumption |

## Interoperability crosswalk and loss register

This is a design mapping, **not an implemented exporter**. None of the standards or platforms is claimed to preserve these fields automatically.

| Local field or behavior | Candidate native concept | Loss risk / required adapter test |
| --- | --- | --- |
| `id`, `definition`, `version` | Native metric identity, description and version/export revision | Name equality is not identity; preserve source namespace and pinned revision |
| `grain`, `aggregation`, `unit` | Semantic dimensions/entities, measure aggregation and unit metadata | Currency-minor units and cohort must not silently become major units or a different grain |
| `source_binding`, `lineage` | Native model/asset references; contract authoritative definitions | Fixture strings are not real asset IDs; reject unresolved references |
| `valid_from`, `valid_to`, `status` | Native lifecycle fields or explicit reviewed sidecar | Definition validity is not the metric's data time dimension; reject unsupported temporal interpretation |
| `approval` | Platform stewardship/approval record or explicit sidecar | A copied string is not an authenticated approval; preserve evidence class |
| `action` | Approved read operation binding | A metric exchange format may not carry action policy; do not silently omit it |
| Explanation bridge | Separate reconciliation evidence | Not a formula, relationship or causal inference from subtraction; require separate evidence |

An adapter is ready only after positive and deliberately lossy mappings are exercised against a pinned native schema, then checked with the platform owner. An import/export demo alone would not prove runtime authorization.

## Positioning language

**Use:** “An inspectable semantic decision testbed: clarify the metric, validate the read plan, and separate arithmetic from explanation.”

**Avoid:** “better than Palantir,” “unique governed ontology,” “production-ready control plane,” “vendor benchmark winner,” or “open-source standard.” None is supported by this repository's evidence.

**Next highest-value validation:** ask a platform owner to reproduce one wrong-binding refusal and one valid recognized-revenue read using an existing native metric. A reusable counterexample is more valuable than another architecture diagram.
