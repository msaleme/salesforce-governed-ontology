# Positioning and alternatives

Reviewed 2026-11-08. This is a primary-source documentation comparison, **not a hands-on benchmark**, exhaustive feature inventory, or independent vendor validation. Product descriptions below are vendor statements. No absence of a capability is inferred from a page not mentioning it.

## Position

**A runnable reference contract for reviewing business meaning before an agent receives a read plan.**

The project makes a small set of Oil & Gas semantic decisions inspectable: which revenue definition, which validity interval, which source/operation binding, and what evidence permits explaining a difference. It complements an existing semantic foundation; it does not replace one. The current implementation is an offline synthetic reference, not an integrated control plane.

## Comparison

| Alternative | What the primary source describes | Implication for this prototype |
| --- | --- | --- |
| [Tableau Semantics](https://www.salesforce.com/analytics/tableau-semantics/) | Governed reusable semantic models and metrics, certification workflows, lineage/access controls, business context for agents, integrated with Data 360 | First reuse candidate for a Salesforce-centered implementation. Do not build a second metric catalog by default. Validate actual API access and approved bindings with a platform owner. |
| [Palantir Ontology](https://www.palantir.com/docs/foundry/ontology/overview) | Operational layer with objects/properties/links, actions/functions, dynamic security, and integrated analytical/operational applications | Useful architectural reference for separating semantics and action. This repository has neither an operational engine nor equivalent security or application capabilities. |
| [dbt semantic models / MetricFlow](https://docs.getdbt.com/docs/build/semantic-models) | Semantic graph configured through model metadata, entities as join keys, dimensions and metrics for querying | Reuse established metric definitions and grain where available. This repository does not generate SQL, plan joins, or execute warehouse queries. Documentation inspected includes the v1.12-and-later model format; no adapter compatibility is established. |

Sources above were fetched successfully on the review date. dbt's page extraction was partial; the model/graph/entity descriptions used here were present in the retrieved section. Availability, entitlements and behavior in a particular customer environment were not tested.

## What is useful here, and what is not a moat

- **Useful now:** small reproducible fixtures, distinct bookings/recognized-revenue semantics, exact metric/source/operation checks, bounded metadata preflight, and explicit failure examples.
- **New review capability:** [change review](CHANGE-REVIEW.md) catches content changes behind unchanged versions, identifies affected registry records, and fingerprints compared inputs. This is a local policy check, not an assertion that other products lack change governance.
- **Not differentiation by itself:** a JSON registry, version labels, a graph diagram, or the word “governed.” Production semantics, identity propagation, ownership and source evidence matter more.
- **Not yet proven:** platform fit, live authorization, metadata freshness, finance approval, agent outcome quality, operational scale or independent adoption.

## Improvement priorities

1. **Implemented in this increment:** deterministic semantic change review and negative controls. Never equate a new version with approval or safe compatibility.
2. **Next offline increment:** validate the whole supplied registry at the planner boundary, with deliberate status compatibility and malformed-input tests. Today, authoring validation is separate from resolution; trusted malformed inputs can still raise exceptions.
3. **Access-dependent:** map one existing platform metric and its business grain to the approved read-only operation; test allowed and denied identity paths with sanitized evidence.
4. **Only after live proof:** measure ambiguity-resolution and reconciliation outcomes against fixed cases, including abstention and incorrect-explanation controls. No superiority or accuracy claims until a comparative evaluation exists.

The durable positioning is **inspectable semantic decisions and evidence boundaries**, not “a better Palantir” or an unofficial Salesforce capability claim.
