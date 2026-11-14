"""Offline guided tour. All scenarios use local synthetic fixtures."""
import argparse
import copy
import json
from pathlib import Path

from .demo import MODEL, fixtures, reconcile, resolve
from .validation import validate_model

SCENARIOS = {
    'ambiguity': ('Which revenue?', 'Clarify the metric before choosing a source.', 'clarification_required'),
    'approved-read': ('An approved definition', 'Return a read plan, never execute an API.', 'read_plan_only'),
    'denied': ('A missing fixture scope', 'Stop before returning semantic context.', 'denied'),
    'expired': ('An expired definition', 'A previously approved definition is not valid forever.', 'definition_unavailable'),
    'binding-mismatch': ('The wrong source', 'An allowlisted API is insufficient if it is bound to the wrong metric.', 'binding_mismatch'),
    'difference-only': ('Arithmetic is not causality', 'Without a bridge, report only the difference.', 'difference_only'),
    'explained': ('An evidence-backed explanation', 'A matching synthetic bridge supplies the explanation.', 'explained_by_fixture_bridge'),
    'incompatible': ('Apples and oranges', 'Do not reconcile different currencies or cohorts.', 'incompatible_dimensions'),
}


def run_scenario(name):
    """Run a named deterministic scenario and return its teaching point and result."""
    a, b, bridge = fixtures()
    scopes = {'finance:read'}
    if name == 'ambiguity':
        result = resolve('revenue', scopes)
    elif name == 'approved-read':
        result = resolve('recognized_revenue', scopes)
    elif name == 'denied':
        result = resolve('recognized_revenue', set())
    elif name == 'expired':
        result = resolve('recognized_revenue', scopes, as_of='2027-01-01')
    elif name == 'binding-mismatch':
        model = copy.deepcopy(MODEL)
        model['metrics'][1]['source_binding'] = 'fixture:crm:contract_bookings'
        result = resolve('recognized_revenue', scopes, model=model)
    elif name == 'difference-only':
        result = reconcile(a, b)
    elif name == 'explained':
        result = reconcile(a, b, bridge)
    elif name == 'incompatible':
        b['currency'] = 'EUR'
        result = reconcile(a, b, bridge)
    else:
        raise ValueError(f'Unknown scenario: {name}')
    title, lesson, expected = SCENARIOS[name]
    return {'scenario': name, 'title': title, 'lesson': lesson,
            'expected_status': expected, 'result': result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    tour = sub.add_parser('tour', help='Walk through all eight local scenarios')
    tour.add_argument('--json', action='store_true', help='Machine-readable results')
    scenario = sub.add_parser('scenario', help='Run one scenario as JSON')
    scenario.add_argument('name', choices=SCENARIOS)
    validate = sub.add_parser('validate', help='Check the bounded fixture registry format')
    validate.add_argument('path', nargs='?', type=Path, default=Path(__file__).with_name('ontology.json'))
    args = parser.parse_args(argv)
    if args.command == 'validate':
        try:
            errors = validate_model(json.loads(args.path.read_text(encoding='utf-8')))
        except (OSError, UnicodeError, ValueError) as exc:
            errors = [f'Cannot load registry: {exc}']
        print(json.dumps({'valid': not errors, 'errors': errors}, indent=2))
        return 1 if errors else 0
    if args.command == 'scenario':
        print(json.dumps(run_scenario(args.name), indent=2))
        return 0
    results = [run_scenario(name) for name in SCENARIOS]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print('SALESFORCE-GOVERNED ONTOLOGY | OFFLINE SYNTHETIC TOUR\n')
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['title']} [{item['scenario']}]")
            print(f"   {item['lesson']}")
            print(f"   Outcome: {item['result']['status']}")
            if 'difference_minor' in item['result']:
                amount = item['result']['difference_minor']
                print(f'   Synthetic USD difference: {amount // 100:,}.{amount % 100:02d}')
            print()
        print('No live vendor integration, authenticated authorization, or API execution.')
    return 0 if all(x['result']['status'] == x['expected_status'] for x in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
