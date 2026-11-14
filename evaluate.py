"""Reproduce a fixed synthetic decision contract, NOT a vendor or model benchmark."""
import hashlib
import json
from pathlib import Path
from demo import fixtures, reconcile, resolve
from explore import SCENARIOS, run_scenario

ROOT = Path(__file__).resolve().parent


def result_mismatches(expected, actual):
    """Exact JSON payload comparison, including unexpected fields and scalar types.

    Expectations are reviewed fixtures, never generated during evaluation.
    """
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        raise ValueError('Decision expectations and results must be objects')
    def canonical(value):
        return json.dumps(value, sort_keys=True, allow_nan=False)
    return sorted(key for key in expected.keys() | actual.keys()
                  if key not in expected or key not in actual
                  or canonical(expected[key]) != canonical(actual[key]))


def evaluate(cases):
    rows = []
    for case in cases:
        name = case['case']
        expected = case['expected_result']
        if expected.get('status') != case['expected_status']:
            raise ValueError(f'Inconsistent status expectation: {name}')
        if name in SCENARIOS:
            result = run_scenario(name)['result']
        elif name == 'invalid-registry':
            result = resolve('recognized_revenue', ['finance:read'], model={})
        elif name == 'invalid-scopes':
            result = resolve('recognized_revenue', 'finance:read')
        elif name == 'expired-clarification':
            result = resolve('revenue', ['finance:read'], as_of='2027-01-01')
        elif name == 'malformed-bridge':
            a, b, _ = fixtures()
            result = reconcile(a, b, 'an unsupported explanation')
        else:
            raise ValueError(f'Unknown decision case: {name}')
        mismatches = result_mismatches(expected, result)
        rows.append(dict(case, actual_status=result['status'], actual_result=result,
                         mismatch_fields=mismatches, passed=not mismatches))
    return {'evidence': 'synthetic_only', 'evaluation': 'fixed_decision_contract',
            'vendor_comparison': False, 'total': len(rows),
            'passed': sum(row['passed'] for row in rows), 'cases': rows}


def report():
    result = evaluate(json.loads((ROOT / 'examples/decision-cases.json').read_text()))
    result['sha256'] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                        for name in ('ontology.json', 'demo.py', 'validation.py', 'explore.py',
                                     'evaluate.py', 'sgo/demo.py', 'sgo/validation.py', 'sgo/explore.py',
                                     'sgo/ontology.schema.json', 'examples/decision-cases.json')}
    return result


if __name__ == '__main__':
    result = report()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['total'] and result['passed'] == result['total'] else 1)
