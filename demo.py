"""Synthetic semantic planner. No network, vendor SDK, credentials, or API execution."""
import json
from datetime import date
from pathlib import Path
from validation import BINDINGS

ROOT = Path(__file__).resolve().parent
MODEL = json.loads((ROOT / 'ontology.json').read_text())


def resolve(metric_id, scopes, as_of='2026-11-03', model=None):
    """scopes are a fixture input, NOT authenticated identity or production authorization."""
    if 'finance:read' not in scopes:
        return {'status': 'denied', 'reason': 'Synthetic fixture lacks finance:read scope'}
    model = MODEL if model is None else model
    if metric_id == 'revenue':
        return {'status': 'clarification_required', 'choices': ['booked_revenue', 'recognized_revenue']}
    metric = next((m for m in model['metrics'] if m['id'] == metric_id), None)
    if metric is None:
        return {'status': 'unsupported_concept'}
    if metric['status'] != 'approved' or not metric.get('approval', {}).get('reference'):
        return {'status': 'definition_unavailable'}
    if not date.fromisoformat(metric['valid_from']) <= date.fromisoformat(as_of) <= date.fromisoformat(metric['valid_to']):
        return {'status': 'definition_unavailable'}
    if metric['action']['side_effect'] != 'read' or metric['action']['operation_id'] not in {'read_contract_bookings', 'read_recognized_revenue'}:
        return {'status': 'unsupported_action'}
    if (metric['source_binding'], metric['action']['operation_id']) != BINDINGS.get(metric_id):
        return {'status': 'binding_mismatch'}
    if metric['action']['required_scope'] not in scopes:
        return {'status': 'denied'}
    return {'status': 'read_plan_only', 'evidence': 'synthetic_only', 'concept': metric['id'],
            'version': metric['version'], 'definition': metric['definition'],
            'source': metric['source_binding'], 'operation': metric['action']['operation_id']}


def fixtures():
    common = {'operator_id': 'fixture:operator:001', 'contract_id': 'fixture:contract:001',
              'period': '2026-10', 'currency': 'USD'}
    booked = dict(common, amount_minor=120000000, source='fixture:crm:contract_bookings')
    recognized = dict(common, amount_minor=90000000, source='fixture:erp:revenue_ledger')
    bridge = dict(common, amount_minor=30000000, source='fixture:reconciliation:001',
                  reason='Unfulfilled performance obligations in this synthetic contract cohort')
    return booked, recognized, bridge


def reconcile(booked, recognized, bridge=None):
    """Only compares a pre-aligned fixture cohort; not a general accounting bridge."""
    dimensions = ('operator_id', 'contract_id', 'period', 'currency')
    if any(not booked.get(k) or booked[k] != recognized.get(k) for k in dimensions):
        return {'status': 'incompatible_dimensions'}
    if booked.get('source') != 'fixture:crm:contract_bookings' or recognized.get('source') != 'fixture:erp:revenue_ledger':
        return {'status': 'missing_or_wrong_source'}
    if any(type(r.get('amount_minor')) is not int for r in (booked, recognized)):
        return {'status': 'invalid_amount'}
    delta = booked['amount_minor'] - recognized['amount_minor']
    result = {'status': 'difference_only', 'currency': booked['currency'], 'difference_minor': delta,
              'sources': [booked['source'], recognized['source']], 'evidence': 'synthetic_only'}
    if bridge is not None:
        if (any(bridge.get(k) != booked[k] for k in dimensions)
                or type(bridge.get('amount_minor')) is not int
                or bridge['amount_minor'] != delta
                or not bridge.get('source') or not bridge.get('reason')):
            return {'status': 'invalid_bridge'}
        result.update(status='explained_by_fixture_bridge', explanation=bridge['reason'])
        result['sources'].append(bridge['source'])
    return result


def demo():
    return {'scope': 'Local synthetic demonstration; no live authorization or integration',
            'ambiguous_question': resolve('revenue', {'finance:read'}),
            'bookings_plan': resolve('booked_revenue', {'finance:read'}),
            'recognized_plan': resolve('recognized_revenue', {'finance:read'}),
            'unauthorized_fixture': resolve('recognized_revenue', set()),
            'reconciliation': reconcile(*fixtures())}


if __name__ == '__main__':
    print(json.dumps(demo(), indent=2))
