"""Reproduce a fixed synthetic decision contract, NOT a vendor or model benchmark."""
import hashlib
import json
from pathlib import Path
from demo import fixtures, reconcile, resolve
from explore import SCENARIOS, run_scenario

ROOT = Path(__file__).resolve().parent


def evaluate(cases):
    rows = []
    for case in cases:
        name = case['case']
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
        rows.append(dict(case, actual_status=result['status'], passed=result['status'] == case['expected_status']))
    return {'evidence': 'synthetic_only', 'evaluation': 'fixed_decision_contract',
            'vendor_comparison': False, 'total': len(rows),
            'passed': sum(row['passed'] for row in rows), 'cases': rows}


def report():
    result = evaluate(json.loads((ROOT / 'examples/decision-cases.json').read_text()))
    result['sha256'] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                        for name in ('ontology.json', 'demo.py', 'validation.py', 'explore.py',
                                     'evaluate.py', 'examples/decision-cases.json')}
    return result


if __name__ == '__main__':
    result = report()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['total'] and result['passed'] == result['total'] else 1)
