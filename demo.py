"""Synthetic semantic planner. No network, vendor SDK, credentials, or API execution."""
import json
import re
from datetime import date
from pathlib import Path
from validation import BINDINGS, validate_model

ROOT = Path(__file__).resolve().parent
MODEL = json.loads((ROOT / 'ontology.json').read_text())


def _registry_refusal(model, metric_id):
    """Preserve specific legacy refusals when safely identifiable; never allow a plan."""
    if not isinstance(model, dict) or not isinstance(model.get('metrics'), list):
        return 'invalid_registry'
    matches = [m for m in model['metrics'] if isinstance(m, dict) and m.get('id') == metric_id]
    if len(matches) != 1:
        return 'invalid_registry'
    metric = matches[0]
    approval = metric.get('approval')
    if (metric.get('status') in ('draft', 'review', 'deprecated', 'revoked')
            or isinstance(approval, dict) and not approval.get('reference')):
        return 'definition_unavailable'
    action = metric.get('action')
    if not isinstance(action, dict):
        return 'invalid_registry'
    if (action.get('side_effect') != 'read'
            or action.get('operation_id') not in ('read_contract_bookings', 'read_recognized_revenue')):
        return 'unsupported_action'
    if (metric.get('source_binding'), action.get('operation_id')) != BINDINGS.get(metric_id):
        return 'binding_mismatch'
    return 'invalid_registry'


def resolve(metric_id, scopes, as_of='2026-11-03', model=None):
    """Validate JSON-shaped registry and request before returning any plan.

    Scope strings remain synthetic inputs, never authenticated authorization.
    """
    if (not isinstance(scopes, (list, tuple, set, frozenset))
            or not all(isinstance(s, str) and s.strip() for s in scopes)):
        return {'status': 'invalid_request'}
    if 'finance:read' not in scopes:
        return {'status': 'denied', 'reason': 'Synthetic fixture lacks finance:read scope'}
    if not isinstance(metric_id, str) or not metric_id.strip():
        return {'status': 'invalid_request'}
    try:
        if not isinstance(as_of, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', as_of):
            raise ValueError
        evaluation_date = date.fromisoformat(as_of)
    except ValueError:
        return {'status': 'invalid_request'}
    model = MODEL if model is None else model
    if validate_model(model):
        # Do not leak supplied definitions or diagnostics through this boundary.
        return {'status': _registry_refusal(model, metric_id)}
    if metric_id == 'revenue':
        choices = [m['id'] for m in model['metrics']
                   if m['status'] == 'approved'
                   and date.fromisoformat(m['valid_from']) <= evaluation_date <= date.fromisoformat(m['valid_to'])]
        return ({'status': 'clarification_required', 'choices': sorted(choices)}
                if choices else {'status': 'definition_unavailable'})
    metric = next((m for m in model['metrics'] if m['id'] == metric_id), None)
    if metric is None:
        return {'status': 'unsupported_concept'}
    if metric['status'] != 'approved':
        return {'status': 'definition_unavailable'}
    if not date.fromisoformat(metric['valid_from']) <= evaluation_date <= date.fromisoformat(metric['valid_to']):
        return {'status': 'definition_unavailable'}
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
    if not isinstance(booked, dict) or not isinstance(recognized, dict):
        return {'status': 'invalid_input'}
    if bridge is not None and not isinstance(bridge, dict):
        return {'status': 'invalid_bridge'}
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
                or any(not isinstance(bridge.get(k), str) or not bridge[k].strip()
                       for k in ('source', 'reason'))):
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
