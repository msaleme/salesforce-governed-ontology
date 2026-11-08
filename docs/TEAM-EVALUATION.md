# A bounded team evaluation

**Decision:** Is this decision-contract pattern worth adapting to our own semantic layer? Not: is this a supported production platform?

Intended evaluators: a semantic-layer architect paired with an agent-evaluation or data-platform engineer. No vendor account or model endpoint is required for the core exercise. Start by reviewing [license status](../LICENSE-STATUS.md); this repository does not currently grant open-source reuse rights. Do not treat this packet as permission to redistribute or deploy it.

## Suggested 30-minute review

1. **Understand the failure (5 minutes).** Run `python3 explore.py scenario difference-only` and `python3 explore.py scenario explained`. Inspect which extra fixture evidence changes the result. The bridge is supplied evidence, not independently verified causality.
2. **Reproduce (5 minutes).** Run `python3 scripts/verify.py` and `python3 scripts/reproduce.py > /tmp/ontology-receipt.json`. Record the commit and Python version. A dirty tree must be disclosed.
3. **Challenge transfer (10 minutes).** Run `python3 reliability.py`. Inspect `examples/reliability-cases.json`. Propose a synthetic case the current policy gets wrong, with expected result and rationale. Do not merely increase the existing test count.
4. **Inspect portability (5 minutes).** Run `python3 standards_export.py`. Read `report.omitted_source_paths`. Decide whether retaining only concept identity and definition is useful. Optional RDFLib parser check: [export guide](STANDARDS-EXPORT.md).
5. **Make a decision (5 minutes).** Complete the disposition below. Stop if the assumptions do not match your use case.

## Review disposition

Copy into an issue or your own review record:

```text
Reviewed commit:
Reviewer role / relationship to project:
Actually executed? yes/no; Python/OS:
Commands and receipt (synthetic only, inspect before posting):
Problem this could solve for our team:
Counterexample input, expected output and rationale:
Observed output:
What would need replacement in our stack:
License/ownership clearance: pending/confirmed by authorized owner
Disposition: reject / revisit after named evidence / candidate for isolated spike
Blocking evidence:
```

A self-run receipt is not an attestation. An automated peer is not an independent human team. Maintainer-written expected outputs establish regression behavior, not unbiased correctness.

## Acceptance gates

- **Local inspection:** commands pass at an identified commit; both domains and export losses are understood.
- **Independent evidence:** an outside evaluator supplies a reproducible result or counterexample, with relationship and execution disclosed. Currently unverified; a request is not a result.
- **Reuse:** authorized ownership/distribution decision and appropriate license. Currently unresolved.
- **Native adapter:** platform owner provides versioned native export, approved bindings and sandbox access. Currently unverified.
- **Deployment:** separate identity-boundary, availability, monitoring, audit retention and incident ownership review. Not offered by this prototype.

## Integration seam and stop conditions

Keep existing semantic/graph infrastructure. Adapt native metadata into reviewed decision inputs; do not replace your registry with this fixture format. Execute live reads only through your existing authenticated policy boundary. The planner's scope strings are not that boundary.

Reject or defer if you need general-purpose metric execution, lossless graph exchange, statistical SLO monitoring, verified causal inference, production SLAs or immediately cleared redistribution rights. No implementation here supplies them.

## External review request

A single focused request belongs on this repository's issue tracker, not promotional comments on other vendors' repositories. Requested artifact: one synthetic counterexample or a clean reproduction with execution disclosure. No stars, endorsements, customer data or access tokens requested. No outside response is assumed.
