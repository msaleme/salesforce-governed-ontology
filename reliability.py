"""Second-domain synthetic contract: request success SLO, not financial arithmetic.

Integer cross-multiplication avoids rounded-percent decisions. Counts are supplied
fixtures, not authenticated observations. No diagnosis or live monitoring.
"""
import json
from datetime import datetime
from pathlib import Path


def assess(observation, objective):
    if not isinstance(observation, dict) or not isinstance(objective, dict):
        return {'status': 'invalid_input'}
    keys = ('service', 'window_start', 'window_end', 'population')
    for row in (observation, objective):
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in keys):
            return {'status': 'invalid_input'}
    # Explicit UTC timestamps only; no implicit timezone or calendar inference.
    for row in (observation, objective):
        try:
            start, end = [datetime.strptime(row[k], '%Y-%m-%dT%H:%M:%SZ')
                          for k in ('window_start', 'window_end')]
            if start >= end:
                return {'status': 'invalid_input'}
        except ValueError:
            return {'status': 'invalid_input'}
    if any(observation[k] != objective[k] for k in keys):
        return {'status': 'incompatible_dimensions'}
    if objective.get('indicator') != 'request_success_ratio':
        return {'status': 'unsupported_indicator'}
    target = objective.get('target_basis_points')
    total, successful = observation.get('total'), observation.get('successful')
    if (any(type(v) is not int for v in (target, total, successful))
            or not 0 < target <= 10000 or not 0 <= successful <= total):
        return {'status': 'invalid_input'}
    if (not isinstance(observation.get('source'), str) or not observation['source'].strip()
            or not isinstance(objective.get('version'), str) or not objective['version'].strip()):
        return {'status': 'invalid_input'}
    if observation.get('coverage_complete') is not True or total == 0:
        return {'status': 'insufficient_evidence'}
    return {'status': 'objective_met' if successful * 10000 >= total * target else 'objective_missed',
            'successful': successful, 'total': total, 'target_basis_points': target,
            'objective_version': objective['version'], 'source': observation['source'],
            'evidence': 'synthetic_only', 'cause': 'not_established'}


def evaluate_cases(path=None):
    path = path or Path(__file__).parent / 'examples/reliability-cases.json'
    cases = json.loads(Path(path).read_text())
    results = [{'id': case['id'], 'actual': assess(case['observation'], case['objective']),
                'expected': case['expected']} for case in cases]
    for result in results:
        result['passed'] = (json.dumps(result['actual'], sort_keys=True, allow_nan=False)
                            == json.dumps(result['expected'], sort_keys=True, allow_nan=False))
    return {'evidence': 'synthetic_only', 'cases': results,
            'passed': bool(results) and all(r['passed'] for r in results)}


if __name__ == '__main__':
    result = evaluate_cases()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
