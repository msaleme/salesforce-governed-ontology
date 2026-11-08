"""Lossy SKOS vocabulary projection, not a registry or authorization export.

Produces JSON-LD expanded form: absolute IRIs, no remote context or network.
Only concept identity and definition survive. No inverse registry importer exists.
"""
import hashlib
import json
from pathlib import Path
from validation import validate_model

SKOS = 'http://www.w3.org/2004/02/skos/core#'
DCT = 'http://purl.org/dc/terms/'
BASE = 'urn:example:governed-ontology:vocabulary:'


def export(model):
    errors = validate_model(model)
    if errors:
        raise ValueError('Invalid source registry: ' + '; '.join(errors))
    # Unknown source fields must be accounted for too, not silently discarded.
    digest = hashlib.sha256(json.dumps(model, sort_keys=True, separators=(',', ':'),
                                      ensure_ascii=False).encode()).hexdigest()
    scheme = BASE + digest + ':'
    graph = [{'@id': scheme, '@type': [SKOS + 'ConceptScheme'],
              DCT + 'description': [{'@value': 'Synthetic vocabulary projection; not executable governance.'}]}]
    for concept in sorted(model['concepts'], key=lambda c: c['id']):
        graph.append({'@id': scheme + concept['id'], '@type': [SKOS + 'Concept'],
                      SKOS + 'notation': [{'@value': concept['id']}],
                      SKOS + 'definition': [{'@value': concept['definition'], '@language': 'en'}],
                      SKOS + 'inScheme': [{'@id': scheme}]})
    def pointer(key):
        return key.replace('~', '~0').replace('/', '~1')
    omitted = ['/' + pointer(key) for key in sorted(model) if key != 'concepts']
    for i, concept in enumerate(model['concepts']):
        omitted.extend(f'/concepts/{i}/{pointer(key)}' for key in sorted(concept)
                       if key not in ('id', 'definition'))
    return {'document': graph, 'report': {
        'profile': 'concept-vocabulary-skos-v1', 'source_sha256': digest,
        'preserved': ['concepts[].id (skos:notation)', 'concepts[].definition (English literal)'],
        'omitted_source_paths': omitted, 'lossless': False,
        'executable': False, 'vendor_import_verified': False,
        'warning': 'Relationships, metrics, approvals, versions and action bindings are not transported. Do not execute from this export.'}}


def recovered_concepts(document):
    """Inspect this producer's bounded projection, NOT a general JSON-LD parser."""
    return sorted([{'id': node[SKOS + 'notation'][0]['@value'],
                    'definition': node[SKOS + 'definition'][0]['@value']}
                   for node in document if node.get('@type') == [SKOS + 'Concept']],
                  key=lambda c: c['id'])


if __name__ == '__main__':
    model = json.loads((Path(__file__).parent / 'ontology.json').read_text())
    print(json.dumps(export(model), indent=2, ensure_ascii=False))
