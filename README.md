# Salesforce-Governed Business Ontology

**Eight inspectable verdicts for an agent deciding whether to answer, clarify or stop.**

```sh
sgo tour
```

```text
Which revenue?           -> clarification_required
Approved definition      -> read_plan_only
Missing fixture scope    -> denied
Expired definition       -> definition_unavailable
Wrong metric/API binding -> binding_mismatch
No explanation bridge    -> difference_only
Matching fixture bridge  -> explained_by_fixture_bridge
Different currencies     -> incompatible_dimensions
```

Bookings of USD 1.2M minus recognized revenue of USD 0.9M gives a USD 0.3M
difference. It does not explain why. This offline testbed makes that boundary
visible, alongside definition lifecycle, source bindings and evidence checks.

## Install and run

Python 3.10+:

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
sgo tour
sgo validate
sgo byod examples/user-metrics.json
```

Install from this checkout; no package release is claimed. Installation fetches
`jsonschema` and build dependencies. Installed commands run offline without
credentials or model calls. For development use `python -m pip install -e .`.
Existing `python3 explore.py tour` and other root script commands remain supported.

## Bring your own definitions

`sgo byod FILE.json` loads a registry and explicit expected-result cases. Custom
metric IDs, units, grains, scopes and read bindings are supported. It emits only
local read plans and labels all supplied evidence unverified. It never runs SQL,
executes a binding or contacts a platform. See the [input contract and example](docs/BRING-YOUR-OWN-DATA.md).

## CTO and industry architecture pack

[CTO decision brief](docs/CTO-ADVISORY.md) · [Pilot scorecard and decision record](docs/CTO-PILOT-KIT.md)

Proposed reference architectures for [energy](docs/industries/ENERGY.md), [financial services](docs/industries/FINANCIAL-SERVICES.md), [healthcare operations](docs/industries/HEALTHCARE.md), [manufacturing](docs/industries/MANUFACTURING.md), and [retail / distribution](docs/industries/RETAIL.md). Each identifies a bounded business decision, native-system boundaries, semantic counterexamples, ownership and a first pilot. These are design blueprints, not additional implemented domains or validated integrations.


## Go deeper

- [Run, demonstrate and reproduce](docs/RUN-GUIDE.md): walkthrough, presentation script, captured output and reproducible receipts.
- [Validation, evaluation and platform fit](docs/ASSURANCE.md): controls, fixed-case evaluation and native-platform acceptance gates.
- [Architecture](docs/ARCHITECTURE.md), [data model](docs/DATA-MODEL.md) and [ontology map](docs/ONTOLOGY-MAP.md).
- [Platform comparison](docs/COMPARISON.md), [change review](docs/CHANGE-REVIEW.md) and [design decisions](docs/DESIGN-DECISIONS.md).
- [Team evaluation](docs/TEAM-EVALUATION.md), [second domain](docs/SECOND-DOMAIN.md) and [SKOS export limitations](docs/STANDARDS-EXPORT.md).
- [Sandbox integration](docs/SANDBOX-INTEGRATION.md), [roadmap](docs/ROADMAP.md), [contributing](CONTRIBUTING.md) and [security](SECURITY.md).
- [Draft issue ideas and demo recording outline](docs/CONTRIBUTOR-DRAFTS.md) (not posted or recorded).

## Verify

```sh
python3 scripts/verify.py
```

Tests live in `tests/`; the installed core and [JSON Schema](sgo/ontology.schema.json)
live in `sgo/`. The verifier checks behavior, fixture/schema validity, packaged
registry parity, generated output and documentation links. CI also tests a wheel
outside the checkout.

## Scope and license

Offline reference prototype, not an official Salesforce product. The built-in
examples are synthetic; user inputs are unverified. No live semantic adapters,
authenticated authorization, general reconciliation engine or independent
validation is established. Reuse existing platform semantics before building a
parallel registry.

[MIT License](LICENSE). Copyright (c) 2026 Michael Saleme.
