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

## Watch the terminal demo

[Download the short asciinema recording](docs/assets/sgo-demo.cast) of
`sgo tour` and `sgo byod examples/user-metrics.json`. It shows all eight tour
verdicts and all four passing BYOD cases, with the complete command output.

GitHub does not play `.cast` files inline. With asciinema installed, replay locally:

```sh
asciinema play docs/assets/sgo-demo.cast
```

The recording identifies its source commit and Python version. Output is paced
for readability; this is not a performance benchmark. Only synthetic local data
is shown, not live platform validation. No external recording host is used.

## Bring your own definitions

`sgo byod FILE.json` loads a registry and explicit expected-result cases. Custom
metric IDs, units, grains, scopes and read bindings are supported. It emits only
local read plans and labels all supplied evidence unverified. It never runs SQL,
executes a binding or contacts a platform. See the [input contract and example](docs/BRING-YOUR-OWN-DATA.md).

## Go deeper

- [Run, demonstrate and reproduce](docs/RUN-GUIDE.md): walkthrough, presentation script, captured output and reproducible receipts.
- [Validation, evaluation and platform fit](docs/ASSURANCE.md): controls, fixed-case evaluation and native-platform acceptance gates.
- [Architecture, decisions and roadmap](docs/ARCHITECTURE.md); [data model, API and ontology map](docs/DATA-MODEL.md).
- [Platform comparison](docs/COMPARISON.md) and [semantic change review](docs/CHANGE-REVIEW.md).
- [Second domain](docs/SECOND-DOMAIN.md), [SKOS export limitations](docs/STANDARDS-EXPORT.md) and [sandbox integration](docs/SANDBOX-INTEGRATION.md).
- [Project notes](docs/PROJECT-NOTES.md): publication history, licensing decision and retained article/outreach drafts.
- [Draft issue ideas and demo outline](docs/CONTRIBUTOR-DRAFTS.md); [contributing](CONTRIBUTING.md) and [security](SECURITY.md).

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
