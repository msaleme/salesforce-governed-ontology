# Walkthrough update (unpublished draft for GB review)

Editorial hold: pinned to the merged #14 source snapshot, not a published release.
No tag, release or dev.to publication is authorized. Before publication, confirm
the approved release SHA, update the pin if needed, and reverify the commands.

## Proposed update

The walkthrough now has an installable CLI and a bring-your-own-definitions path.
This [source snapshot](https://github.com/msaleme/salesforce-governed-ontology/tree/b5348c9c0fc9635ffc2d6fd7751644da71a57458)
includes the inline terminal demo, JSON Schema, MIT license, and industry and
semantic-federation guides.

```sh
git clone https://github.com/msaleme/salesforce-governed-ontology.git
cd salesforce-governed-ontology
git checkout b5348c9c0fc9635ffc2d6fd7751644da71a57458
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
sgo tour
sgo byod examples/user-metrics.json
```

The tour shows when to answer, clarify or stop. BYOD evaluates your registry and
expected-result cases locally. It produces read plans, not executed queries;
built-in examples are synthetic, and no live platform integration is claimed.
