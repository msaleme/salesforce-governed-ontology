"""Offline user-defined read plans. Supplied scopes and approvals are not trusted identity."""
from datetime import date
import json
from .validation import schema_errors


def load_json(path):
    """Reject ambiguous duplicate keys and non-JSON numeric constants."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result

    def constant(value):
        raise ValueError(f'Not a JSON number: {value}')

    with open(path, encoding='utf-8') as stream:
        return json.load(stream, object_pairs_hook=pairs, parse_constant=constant)


def validate_registry(model):
    errors = schema_errors(model)
    if errors:
        return errors
    for collection in ('concepts', 'metrics'):
        ids = [row['id'] for row in model[collection]]
        if len(ids) != len(set(ids)):
            errors.append(f'{collection}: duplicate ID')
    concepts = {row['id'] for row in model['concepts']}
    edges = set()
    for edge in model['relationships']:
        key = tuple(edge[k] for k in ('source', 'predicate', 'target'))
        if key in edges or not {edge['source'], edge['target']} <= concepts:
            errors.append('relationships: duplicate edge or unknown concept')
        edges.add(key)
    for metric in model['metrics']:
        if metric['valid_from'] > metric['valid_to']:
            errors.append(f"{metric['id']}: reversed validity interval")
        if metric['source_binding'] not in metric['lineage']:
            errors.append(f"{metric['id']}: lineage must include source_binding")
    return errors


def plan(model, case):
    """Never imports, evaluates, resolves URLs or executes a supplied binding."""
    request = case['request']
    metric = next((m for m in model['metrics'] if m['id'] == request['metric']), None)
    if metric is None:
        return {'status': 'unsupported_concept'}
    if metric['action']['required_scope'] not in request['scopes']:
        return {'status': 'denied'}
    if (metric['status'] != 'approved'
            or not metric['valid_from'] <= request['as_of'] <= metric['valid_to']):
        return {'status': 'definition_unavailable'}
    return {'status': 'read_plan_only', 'evidence': 'user_supplied_unverified',
            'concept': metric['id'], 'version': metric['version'],
            'definition': metric['definition'], 'source': metric['source_binding'],
            'operation': metric['action']['operation_id']}


def evaluate_file(path):
    payload = load_json(path)
    if not isinstance(payload, dict) or set(payload) != {'ontology', 'cases'}:
        raise ValueError('Expected an object containing exactly ontology and cases')
    errors = validate_registry(payload['ontology'])
    if errors:
        raise ValueError('Invalid ontology: ' + '; '.join(errors))
    cases = payload['cases']
    if not isinstance(cases, list) or not cases:
        raise ValueError('cases must be a nonempty array')
    ids = set()
    # Validate the entire file before running any case, so malformed tails fail closed.
    for case in cases:
        if not isinstance(case, dict) or set(case) != {'id', 'request', 'expected_result'}:
            raise ValueError('Each case requires exactly id, request and expected_result')
        if not isinstance(case['id'], str) or not case['id'].strip() or case['id'] in ids:
            raise ValueError('Case IDs must be unique nonempty strings')
        ids.add(case['id'])
        req = case['request']
        if not isinstance(req, dict) or set(req) != {'metric', 'scopes', 'as_of'}:
            raise ValueError('request requires exactly metric, scopes and as_of')
        if not isinstance(req['metric'], str) or not req['metric'].strip():
            raise ValueError('metric must be a nonempty string')
        if not isinstance(req['scopes'], list) or any(not isinstance(s, str) or not s.strip() for s in req['scopes']):
            raise ValueError('scopes must be an array of nonempty strings')
        if not isinstance(req['as_of'], str):
            raise ValueError('as_of must be YYYY-MM-DD')
        parsed = date.fromisoformat(req['as_of'])
        if parsed.isoformat() != req['as_of']:
            raise ValueError('as_of must be YYYY-MM-DD')
        expected = case['expected_result']
        if not isinstance(expected, dict) or not isinstance(expected.get('status'), str):
            raise ValueError('expected_result requires a status and the full expected result')
    rows = []
    for case in cases:
        actual = plan(payload['ontology'], case)
        expected = case['expected_result']
        # Exact JSON comparison prevents status-only assertions from hiding payload drift.
        same = json.dumps(actual, sort_keys=True, allow_nan=False) == json.dumps(expected, sort_keys=True, allow_nan=False)
        rows.append({'id': case['id'], 'expected_result': expected, 'actual_result': actual, 'passed': same})
    return {'evidence': 'user_supplied_unverified', 'execution': 'offline_read_plans_only',
            'total': len(rows), 'passed': sum(row['passed'] for row in rows), 'cases': rows}
