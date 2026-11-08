# Reproduce and challenge the decision contract

The [captured terminal demonstration](TERMINAL-DEMO.md) shows clarification, an accepted read plan, a wrong-binding refusal, arithmetic without explanation and a synthetic explanation bridge. CI checks the transcript against actual CLI output. This is text, not a recorded video or live integration.

## One-command evidence packet

Use Python 3.10+ and Git in a clean checkout. No third-party packages, credentials, platform accounts or model calls are needed.

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
python3 scripts/reproduce.py > ../ontology-reproduction.json
```

The command runs the full verifier and fixed-case evaluator, records their exit codes/output, the Git commit, Python version, dirty-tree flag and SHA-256 hashes of tracked files. Either command failing produces an overall failure and nonzero exit. A timeout terminates with an error, not a success receipt. Write the receipt outside the checkout so its creation does not dirty the tree.

Hashes identify bytes, not authorship or approval. The commit identifies HEAD, not uncommitted changes. The dirty flag includes untracked files; these are not hashed. Use a clean checkout for a comparable run. The receipt explicitly leaves independence `not_established`; another automated self-run is not independent validation. Inspect logs before sharing, especially after modifying tests to use local inputs.

## Submit useful evidence

Use the [counterexample form](https://github.com/msaleme/salesforce-governed-ontology/issues/new?template=decision-counterexample.yml). State:

- Commit and clean/dirty state, Python version, commands and exit codes.
- Whether you are an independent contributor or project maintainer.
- The specific case, actual result and expected result, with a minimal synthetic input.
- Whether this reproduces existing fixture behavior or challenges a decision rule.

A passing fixed suite is not a held-out evaluation. Do not send private metadata or credentials. No external reproductions have yet been established.

## Native-platform validation handoff

The next integration cannot be selected by guessing a metric mapping. A platform owner must supply one approved native metric export with its schema/version, unit, grain and identity; a designated sandbox; and approved read-only bindings/access. Use the [platform-fit template](PLATFORM-FIT-REVIEW.md) and [sandbox checklist](SANDBOX-INTEGRATION.md).

Acceptance: retain a pinned export, prove a compatible mapping, deliberately change grain/unit/binding to show rejection, and exercise permitted and denied identities. Preserve lifecycle and explanation evidence in a reviewed sidecar when native fields cannot represent them. Do not claim an adapter or runtime authorization until those tests run against the selected foundation. Licensing remains an owner decision in [license status](../LICENSE-STATUS.md).
