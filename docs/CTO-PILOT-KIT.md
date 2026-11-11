# CTO pilot and architecture decision kit

Proposed process, not a completed deployment or compliance assessment. Start with the [CTO brief](CTO-ADVISORY.md) and [30-minute local evaluation](TEAM-EVALUATION.md). Resolve [licensing](LICENSING-DECISION.md) before reuse or deployment. Existing live-integration prerequisites still apply.

## Four evidence gates, not a promised timeline

1. **Frame:** name the domain owner and one disputed decision. Freeze the existing workflow baseline, candidate native model revision, evaluation population, intended benefit and explicit non-goals. Prefer reusing the incumbent semantics.
2. **Map:** obtain an authorized sanitized native export. Map each decision-contract field to native or reviewed sidecar fields. Record unmapped meaning and reject unsafe mappings. Pin schemas and revisions. No customer data in public issues.
3. **Challenge offline:** a domain reviewer supplies labeled normal, ambiguous, stale, incomplete and misleading cases. Keep some cases untouched until the decision rules are frozen. Compare full results, not just status labels. Record changes after failures and reserve a fresh holdout for retest.
4. **Prove in isolated sandbox:** after access approval, execute read-only with differently authorized identities. Test denial at the source, metadata visibility, pagination, partial failure, revocation and cache separation. Retain redacted receipts. No production promotion without a separate operations decision.

## Evaluation plan to freeze before execution

```text
Decision / industry:
Sponsor / domain steward / platform owner / incident owner:
Evaluator and relationship to implementation team:
Repository commit / native model and schema revisions:
Current workflow and evidence baseline:
Permitted environment, data classification and reuse authority:
In-scope question / explicit excluded actions:
Case-source provenance and held-out partition:
Expected complete result for each case, assigned by:
Acceptance thresholds, rationale and approver:
Maximum query latency / freshness / operating effort:
Receipt storage, access and retention owner:
Stop conditions and rollback trigger:
```

## Scorecard: record denominators and uncertainty

| Measure | Calculation / evidence | Decision interpretation |
| --- | --- | --- |
| Correct complete results | Fully correct outputs / adjudicated cases, split by case class | Include provenance, units and withheld explanations, not status alone |
| Unsupported answers | Unsupported substantive answers / cases lacking sufficient evidence | Any observed critical unsupported answer blocks progression pending correction |
| False refusals | Refused answerable authorized cases / answerable authorized cases | Compare with baseline so blanket refusal cannot look successful |
| Ambiguity handling | Correct clarifications / genuinely ambiguous cases | Reviewer checks choices are valid and do not disclose restricted terms |
| Unauthorized disclosure | Value or metadata disclosures in deliberately denied cases | Any observed disclosure blocks progression; zero observed does not prove security |
| Change safety | Correct handling of affected cases / selected change-impact cases | Include revoked versions, stale caches and binding drift |
| Operational burden | Measured latency distribution, steward time and correction time | Record environment, workload and sample size; thresholds set by owners |

Do not aggregate these into a flattering single score. Report all case counts, failures and exclusions. Small pilots are descriptive evidence, not a general effectiveness estimate. No thresholds or outcomes have been measured for the proposed industry architectures.

## Shared challenge matrix

| Input change | Required behavior to specify and test |
| --- | --- |
| Same label, two approved definitions | Clarify before selecting an operation |
| Unit, cohort, grain or time mismatch | Reject comparison or apply an explicitly approved transformation |
| Missing source pages or late data | Mark incomplete; do not silently present a full total |
| Revoked definition or changed source schema | Stop affected execution; require reviewed rebind |
| Evidence establishes a difference but not a cause | Return only supported difference or withhold explanation |
| Unauthorized principal or purpose | Deny at policy/source boundary, including protected metadata |
| Same query under different identities/tenants | No cached result or receipt disclosure across policy boundaries |
| Valid authorized complete case | Return correct answer and provenance, not blanket refusal |

These are proposed acceptance obligations. Existing local tests cover only a subset; see the [implementation boundary map](CTO-ADVISORY.md).

## Architecture decision record

```text
Title / decision date / reviewers:
Problem and existing native capability:
Options: native-only / reviewed sidecar / graph adapter / defer
Selected option and why alternatives are insufficient:
Versioned mapping and explicitly lost meaning:
Executed evidence links, commit hashes and environment:
Failures, unresolved risks and limits of inference:
Business usefulness compared with frozen baseline:
Licensing / security / domain approvals and actual approvers:
Disposition: reject / revise / isolated pilot / production review requested
Owner, next evidence gate and review date:
Rollback: adapter disable procedure, prior approved version, cache invalidation
```

Production review requested is not production approved. Preserve failed pilot evidence and allow a rational rejection.

## Adoption evidence ladder

1. Maintainer-authored runnable examples: available for finance and reliability.
2. External reproduction or counterexample: [request open](https://github.com/msaleme/salesforce-governed-ontology/issues/9); no response asserted here.
3. Steward-reviewed native mapping: required for each industry; not established.
4. Identity-bound sandbox result: required; not established.
5. Team-owned operational use and maintained change process: not established.

Record progression only with attributable artifacts. Do not equate stars, downloads, an automated review, or a public request with team adoption. Do not name an organization without its authorization.
