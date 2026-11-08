# Salesforce-Governed Business Ontology

[![Verify prototype](https://github.com/msaleme/salesforce-governed-ontology/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/msaleme/salesforce-governed-ontology/actions/workflows/ci.yml)

**[Take the five-minute tour](docs/DEMO-GUIDE.md) · [Explore the ontology](docs/ONTOLOGY-MAP.md) · [Read the design decisions](docs/DESIGN-DECISIONS.md)**

**An inspectable semantic decision testbed: clarify the metric, validate the read plan, and separate arithmetic from explanation.**

A design proposal and runnable, synthetic Oil & Gas reference prototype for a Salesforce-centered semantic control plane. It separates approved business definitions from source metadata, API bindings, and execution authority.

> **Status: design prototype, not a deployed integration.** Salesforce governance, Informatica metadata ingestion, MuleSoft execution, and Agentforce consumption are proposed architecture. The core demonstration is offline Python. An optional read-only sandbox metadata probe is implemented but has not been live-verified. This repository is not an official Salesforce product and makes no determination of corporate IP ownership.

## Why this exists

“Revenue” can mean contract bookings, recognized revenue, invoicing, or cash receipts. An agent must resolve that ambiguity before selecting data or requesting an action. A shared ontology should make the definition, version, provenance, and permitted operation explicit without replacing source-system permissions.

The design assigns distinct responsibilities:

- **Salesforce:** proposed control plane for definition identity, versions, stewardship, and bindings.
- **Informatica:** proposed contributor of catalog metadata, lineage, classification, and quality observations.
- **MuleSoft:** proposed governed integration and action plane.
- **Agentforce:** proposed consumer of approved semantic context and permitted actions.

## Quick start

Requires Python 3.10 or newer. No dependencies, credentials, Salesforce org, network connection, or model endpoint are needed to run the prototype.

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
python3 explore.py tour
python3 explore.py validate
python3 demo.py
python3 scripts/verify.py
```

The demo returns an ambiguous-metric clarification, two distinct read plans, a denied fixture request, and a synthetic reconciliation. Compare its output with [the checked-in example](examples/demo-output.json).

## See the decisions, not just the diagram

```text
Which revenue?           → clarification_required
Approved definition      → read_plan_only
Missing fixture scope    → denied
Expired definition       → definition_unavailable
Wrong metric/API binding → binding_mismatch
No explanation bridge    → difference_only
Matching fixture bridge  → explained_by_fixture_bridge
Different currencies     → incompatible_dimensions
```

Run one case with `python3 explore.py scenario binding-mismatch`, or get machine-readable results with `python3 explore.py tour --json`. All eight scenarios are local, synthetic, and repeatable.

## Review semantic changes

Compare registry snapshots before accepting changed business meaning:

```sh
python3 change_review.py ontology.json ontology.json
```

The [change-review tool](docs/CHANGE-REVIEW.md) flags silent version drift and reports affected definitions, relationships and contracts. All actual changes require review; it never grants approval. See the [primary-source comparison and positioning](docs/COMPARISON.md) for how this reference complements Tableau Semantics, Palantir Ontology and dbt MetricFlow.

## Compare, reproduce, challenge

- [Competitive landscape and gap ledger](docs/COMPARISON.md): thirteen platform/standards perspectives, explicit trade-offs and reuse decisions.
- [Reproduce the 12-case decision contract](docs/EVALUATION.md): `python3 evaluate.py`, full-result assertions, checked-in outcomes and input/code hashes. This is not a vendor benchmark.
- [Report a synthetic counterexample](https://github.com/msaleme/salesforce-governed-ontology/issues/new?template=decision-counterexample.yml): include the commit, command, observed decision and expected behavior.
- [Evidence-led attention packet](docs/ATTENTION.md): draft walkthrough and distribution experiments, not published outreach.

## Optional sandbox readiness

The [sandbox integration guide](docs/SANDBOX-INTEGRATION.md) provides an opt-in REST metadata probe, local token setup and explicit evidence gates. It checks sandbox identity and approved object/field names, not revenue values. The offline quick start above remains credential-free and network-free.

## Demonstration

**Question:** Why do contract bookings differ from recognized revenue for this operator?

The aligned synthetic contract cohort has USD 1,200,000 of bookings and USD 900,000 of recognized revenue. The difference is USD 300,000. A separately supplied fixture bridge attributes the difference to unfulfilled performance obligations. Without that bridge, the code reports only the arithmetic difference, not a causal explanation.

Amounts are integer minor units. The demo's default evaluation date is deliberately fixed at `2026-11-03`, within the fixture definitions' validity interval, so the example is reproducible after that interval ends. Call `resolve(..., as_of="YYYY-MM-DD")` to evaluate another date.

## Documentation

| Guide | Purpose |
| --- | --- |
| [Five-minute demo](docs/DEMO-GUIDE.md) | Presentation script, runnable scenarios, and candid FAQ |
| [Ontology map](docs/ONTOLOGY-MAP.md) | Registry-derived concept graph and metric bindings |
| [Design decisions](docs/DESIGN-DECISIONS.md) | Trade-offs, rationale, and consequences |
| [Architecture](docs/ARCHITECTURE.md) | Components, trust boundaries, lifecycle, and proposed adapter contracts |
| [Data model and API](docs/DATA-MODEL.md) | Vocabulary, metric fields, function contracts, and result statuses |
| [Walkthrough](docs/WALKTHROUGH.md) | Reproduce the scenario and interpret the evidence |
| [Validation](docs/VALIDATION.md) | Executed local controls versus unverified integration requirements |
| [Platform-fit review](docs/PLATFORM-FIT-REVIEW.md) | Reuse-first evaluation and sandbox acceptance packet |
| [Roadmap](docs/ROADMAP.md) | Evidence-gated progression to a sandbox integration |
| [Contributing](CONTRIBUTING.md) | Change, review, and verification workflow |
| [Security](SECURITY.md) | Prototype limitations and private reporting guidance |
| [License status](LICENSE-STATUS.md) | Distribution and ownership status |

## Repository layout

```text
ontology.json             Synthetic vocabulary, metric definitions, and bindings
demo.py                   Offline resolver and reconciliation functions
explore.py                Guided tour, individual scenarios, and validation CLI
validation.py             Structural checks and metric/source/operation contracts
test_*.py                 Behavioral and malformed-registry regression controls
examples/demo-output.json Deterministic reference output
scripts/verify.py         Tests, registry/tour checks, diagram parity, and doc links
docs/                     Architecture, contracts, review packet, and roadmap
.github/workflows/ci.yml  Python verification on pull requests and branch pushes
```

## Scope and limitations

- Seven concepts, seven relationships, and two metric definitions in a lightweight JSON registry. This is not an OWL reasoner, JSON-LD implementation, or validated industry-standard ontology.
- Approval records, scope strings, source IDs, and reconciliation evidence are fixtures. They do not authenticate a caller, validate accounting policy, or establish a security boundary.
- No vendor SDK, deployment package, metadata refresh, persistence, metric execution, verified live authorization, or production data is present. The optional sandbox probe issues bounded REST metadata reads only when explicitly invoked.
- No NVIDIA code was copied and no NVIDIA runtime is required. This is original design work, not a fork of Auto Ontology.
- Reuse existing platform semantics before introducing custom registry objects. Product availability, entitlement, and API compatibility remain unverified.

**Next milestone:** select the existing semantic foundation with an internal platform owner, then prove one recognized-revenue read in a designated sandbox. See the [platform-fit packet](docs/PLATFORM-FIT-REVIEW.md).
