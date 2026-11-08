# Changelog

## 2026-11-08 - Semantic change review

- Added offline snapshot comparison, conservative change classification, version-drift checks and input fingerprints.
- Added mutation and CLI regression controls; no approval or runtime authorization implied.
- Documented primary-source comparison with Tableau Semantics, Palantir Ontology and dbt MetricFlow.

## Guided experience and binding integrity - 2026-11-04

- Add an eight-scenario CLI tour and registry validation command.
- Reject swapped metric/source/operation bindings in the resolver.
- Add malformed-registry and CLI regression controls.
- Add a registry-derived ontology map, five-minute demo guide, and design decisions.
- Verify diagram parity and all discovered tests in CI.

## Metadata type contracts - 2026-11-08

- Add optional exact field-type contracts to the read-only sandbox probe.
- Fail on missing/mismatched types and reject malformed or duplicate contracts.
- Keep receipts sanitized and distinguish name-only checks from type verification.
- Add synthetic regression controls; no live connectivity or semantic approval claimed.

## Unreleased

- Package the original local prototype as a standalone repository.
- Public repository visibility authorized on 2026-11-04; no open-source license assigned.
- Add onboarding, data model/API reference, walkthrough, validation boundaries, roadmap, contribution guidance, and security/license status.
- Add deterministic example verification, local documentation link checks, and Python CI.
- Preserve original synthetic resolver behavior and 15 behavioral controls.

## 0.1.0 design starter - 2026-11-03

- Original Salesforce-centered governance architecture and platform-fit review packet.
- Seven Oil & Gas concepts, seven relationships, and two metric definitions.
- Dependency-free local resolver and synthetic revenue reconciliation.
