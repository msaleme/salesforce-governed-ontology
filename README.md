# Salesforce-Governed Business Ontology

**Business meaning, governed in Salesforce, connected to enterprise evidence and permitted action.**

A design proposal and runnable, synthetic Oil & Gas reference prototype for a Salesforce-centered semantic control plane. It separates approved business definitions from source metadata, API bindings, and execution authority.

> **Status: design prototype, not a deployed integration.** Salesforce governance, Informatica metadata ingestion, MuleSoft execution, and Agentforce consumption are proposed architecture. The executable code is an offline Python demonstration only. This repository is not an official Salesforce product and makes no determination of corporate IP ownership.

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
python3 demo.py
python3 -m unittest -v test_demo.py
python3 scripts/verify.py
```

The demo returns an ambiguous-metric clarification, two distinct read plans, a denied fixture request, and a synthetic reconciliation. Compare its output with [the checked-in example](examples/demo-output.json).

## Demonstration

**Question:** Why do contract bookings differ from recognized revenue for this operator?

The aligned synthetic contract cohort has USD 1,200,000 of bookings and USD 900,000 of recognized revenue. The difference is USD 300,000. A separately supplied fixture bridge attributes the difference to unfulfilled performance obligations. Without that bridge, the code reports only the arithmetic difference, not a causal explanation.

Amounts are integer minor units. The demo's default evaluation date is deliberately fixed at `2026-11-03`, within the fixture definitions' validity interval, so the example is reproducible after that interval ends. Call `resolve(..., as_of="YYYY-MM-DD")` to evaluate another date.

## Documentation

| Guide | Purpose |
| --- | --- |
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
test_demo.py              Behavioral controls using unittest
examples/demo-output.json Deterministic reference output
scripts/verify.py         Tests, output parity, and local Markdown link checks
docs/                     Architecture, contracts, review packet, and roadmap
.github/workflows/ci.yml  Python verification on pull requests and branch pushes
```

## Scope and limitations

- Seven concepts, seven relationships, and two metric definitions in a lightweight JSON registry. This is not an OWL reasoner, JSON-LD implementation, or validated industry-standard ontology.
- Approval records, scope strings, source IDs, and reconciliation evidence are fixtures. They do not authenticate a caller, validate accounting policy, or establish a security boundary.
- No vendor SDK, deployment package, metadata refresh, persistence, API execution, live authorization, or production data is present.
- No NVIDIA code was copied and no NVIDIA runtime is required. This is original design work, not a fork of Auto Ontology.
- Reuse existing platform semantics before introducing custom registry objects. Product availability, entitlement, and API compatibility remain unverified.

**Next milestone:** select the existing semantic foundation with an internal platform owner, then prove one recognized-revenue read in a designated sandbox. See the [platform-fit packet](docs/PLATFORM-FIT-REVIEW.md).
