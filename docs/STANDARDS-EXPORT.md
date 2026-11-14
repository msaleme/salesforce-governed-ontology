# Narrow SKOS export and explicit loss

```sh
python3 standards_export.py > /tmp/ontology-skos-packet.json
```

The output is an envelope: `document` is an expanded-form JSON-LD array; `report` is a non-RDF loss report. Import **only `document`**, not the entire envelope, into an RDF tool. There is no remote JSON-LD context to resolve. [Checked-in output](../examples/skos-export.json) is compared with the producer in CI.

## Mapping contract

This bounded profile uses the [W3C SKOS Recommendation, 18 August 2009](https://www.w3.org/TR/2009/REC-skos-reference-20090818/), specifically Concept, ConceptScheme, notation, definition and inScheme. Primary reference retrieved 2026-11-08 through the W3C current-reference URL after the dated URL returned an access challenge. It is not a full SKOS validator or an OWL ontology conversion.

- Each source concept becomes a `skos:Concept` in one `skos:ConceptScheme`.
- The source ID becomes `skos:notation`; its meaning is not promoted to a preferred human-language label.
- The source definition becomes an English `skos:definition` literal. This profile assumes English input; multilingual conversion is not implemented.
- IRIs use a content-addressed synthetic URN namespace. Every source change creates a new scheme identity. Stable cross-version identity reconciliation is not implemented.
- All other top-level fields are listed as omitted paths, including relationships, metrics, approvals, bindings, namespace and version. Unknown concept fields are also reported.

The original relationships are deliberately not coerced into `skos:broader` or `owl:sameAs`: operating an asset is not a taxonomic relation. The source `subClassOf` relation is also omitted rather than silently changing OWL class semantics into SKOS concept semantics.

## Verification levels

The core tests verify preserved concept identity/definition, explicit loss, unknown-field reporting, malformed-source refusal, content hashes and deterministic output. The projection reader is only for this producer's shape; it is not an independent JSON-LD implementation or an inverse registry importer.

An optional third-party RDF parser smoke test checks parsed identities, English definitions, scheme membership and Turtle graph isomorphism:

```sh
python3 -m venv /tmp/ontology-rdf
/tmp/ontology-rdf/bin/pip install rdflib==7.1.4 pyparsing==3.3.3
/tmp/ontology-rdf/bin/python scripts/check_rdf.py
```

This optional command needs a package download. Install the core package first; ordinary commands then run offline. A maintainer running RDFLib is parser compatibility evidence, not an independent reviewer, native Stardog/GraphDB/Neo4j import test, SKOS conformance certification, or lossless semantic interoperability.

**Never execute an API or authorize a request from this export.** No executable approval or binding semantics survive it. A team should reject this profile if it needs metric definitions, graph edges or governance transported intact.

## Maintainer-run result (2026-11-08)

RDFLib 7.1.4 parsed seven concepts and 30 triples. Concept identities, English definitions and scheme membership matched the source projection; the Turtle round-trip was graph-isomorphic. The dedicated CI job repeats this smoke test. This does not close the independent human evaluation gate.
