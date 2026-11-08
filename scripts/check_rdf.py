"""Optional third-party parser smoke test. Requires rdflib==7.1.4.

This is maintainer-run parser compatibility, not independent human validation.
"""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rdflib import Graph, Namespace, RDF, Literal
from standards_export import export

SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
root = Path(__file__).resolve().parents[1]
model = json.loads((root / 'ontology.json').read_text())
result = export(model)
graph = Graph().parse(data=json.dumps(result['document']), format='json-ld')
concepts = set(graph.subjects(RDF.type, SKOS.Concept))
schemes = set(graph.subjects(RDF.type, SKOS.ConceptScheme))
assert len(concepts) == len(model['concepts'])
assert len(schemes) == 1
for concept in model['concepts']:
    nodes = list(graph.subjects(SKOS.notation, Literal(concept['id'])))
    assert len(nodes) == 1
    assert (nodes[0], SKOS.definition, Literal(concept['definition'], lang='en')) in graph
    assert (nodes[0], SKOS.inScheme, next(iter(schemes))) in graph
# Test a real RDF serialization round-trip, not only our projection reader.
from rdflib.compare import isomorphic
assert isomorphic(graph, Graph().parse(data=graph.serialize(format='turtle'), format='turtle'))
print(json.dumps({'parser':'rdflib', 'concepts':len(concepts), 'triples':len(graph),
                  'turtle_round_trip':'isomorphic', 'independence':'not_established',
                  'vendor_import_verified':False}))
