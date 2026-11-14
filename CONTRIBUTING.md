# Contributing

This design prototype uses branches and pull requests. Keep changes focused and preserve the distinction between executable local behavior and proposed platform functionality.

## Development workflow

1. Create a branch from the latest `main`.
2. Edit the model, implementation, or documentation.
3. For behavior changes, add controls that demonstrate the intended behavior and relevant failure case.
4. Run `python3 scripts/verify.py` and `git diff --check` from the root.
5. Open a PR describing the change, executed checks, and remaining limitations. Do not push implementation changes directly to `main`.

Install development dependencies with `python3 -m pip install -e .`. Python 3.10 and 3.12 are the CI matrix; other versions are not claimed as CI-verified.

## Model changes

Keep semantic IDs stable and distinct from display labels. Document definition changes and their version impact. Preserve fixture-only approval and provenance labels. Do not introduce real customer data, secrets, production identifiers, or claims of standard ontology compatibility without reviewed mappings.

The root `ontology.json` is the editable source fixture. Copy changes to `sgo/ontology.json` for wheel distribution; CI requires byte parity. Run `python3 explore.py validate` after changing the registry. New metric types require an explicit binding in `sgo.validation.BINDINGS`, a scenario, and tests. Update the graph in `docs/ONTOLOGY-MAP.md` when relationships change; CI detects drift.

If example output intentionally changes, regenerate it with `python3 demo.py > examples/demo-output.json`, inspect the diff, and explain the change in the PR. Do not update the example solely to silence a failure.

## Documentation changes

Use repository-relative links, executable commands, explicit assumptions, and current evidence. Update architecture and API documentation when behavior changes. Prefer existing platform capabilities over an unreviewed parallel registry.

## Review criteria

- Can a new reader run the example without credentials?
- Do documented statuses match the implementation?
- Are simulated checks clearly distinguished from runtime enforcement?
- Are accounting assumptions, provenance limits, and unverified integrations explicit?
- Is the change consistent with the repository's [MIT license](LICENSE)?

## Decision counterexamples

Use the semantic decision counterexample issue form with a commit, Python version, minimal synthetic reproduction, actual outcome and expected outcome with rationale. Mark whether you ran it. See the [evaluation protocol](docs/ASSURANCE.md); do not present fixture conformance as independent validation.

## Team evaluation and second domain

Use the [team evaluation packet](docs/TEAM-EVALUATION.md) for a bounded review. Reliability is intentionally separate from finance; document new domain-specific assumptions rather than adding unrelated fields to the finance registry. Standards changes must update the loss report and preserve the non-executable boundary. Reuse is covered by the [MIT License](LICENSE).
