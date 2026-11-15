The walkthrough now has an installable CLI and a bring-your-own-definitions path.
This [source snapshot](https://github.com/msaleme/salesforce-governed-ontology/tree/90c922d0fe3b73c72f45cd7a1a0c6906b128e58b)
includes the [inline terminal demo](https://github.com/msaleme/salesforce-governed-ontology/blob/90c922d0fe3b73c72f45cd7a1a0c6906b128e58b/README.md#watch-the-terminal-demo),
JSON Schema, MIT license, and industry and semantic-federation design guides
(not deployed adapters).

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
git checkout 90c922d0fe3b73c72f45cd7a1a0c6906b128e58b
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
sgo --version
sgo tour
sgo byod examples/user-metrics.json
```

Offline reference prototype, not an official Salesforce product.
The tour shows when to answer, clarify or stop. BYOD evaluates your registry and
expected-result cases locally. It produces read plans, not executed queries;
built-in examples are synthetic, and no live platform integration is claimed.
