"""Offline, synthetic object-readiness checks and five deliberately narrow calculations.

This is not an ingestion adapter, independent validation, or authorization boundary.
Local maps are trusted code/configuration. Supplied JSON is bounded pilot input.
"""
import argparse
from datetime import datetime
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'examples/industry-proof'
INDUSTRIES = ('energy', 'financial-services', 'healthcare', 'manufacturing', 'retail')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def timestamp(value):
    if not isinstance(value, str):
        return False
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ') == value
    except ValueError:
        return False


def valid(value, kind):
    if kind == 'text':
        return isinstance(value, str) and bool(value.strip())
    if kind == 'bool':
        return type(value) is bool
    if kind in ('positive_int', 'nonnegative_int'):
        return type(value) is int and value >= (1 if kind == 'positive_int' else 0)
    if kind == 'timestamp':
        return timestamp(value)
    return type(value) is str and value == kind


def assess(industry, payload):
    if industry not in INDUSTRIES:
        raise ValueError('unsupported industry')
    mapping = json.loads((DATA / f'{industry}-map.json').read_text())
    blockers = []
    specs = {o['name']: o for o in mapping['objects']}

    def block(name, reason, action):
        blockers.append({'object': name, 'reason': reason,
                         'owner': specs.get(name, {}).get('owner', 'Pilot data owner'),
                         'next_action': action})

    if not isinstance(payload, dict) or payload.get('industry') != industry:
        block('Input', 'wrong_or_missing_industry', 'Supply an object with the selected industry ID.')
    scope = payload.get('scope') if isinstance(payload, dict) else None
    if (not isinstance(scope, dict) or set(scope) != {'cohort', 'window_start', 'window_end'}
            or not valid(scope.get('cohort'), 'text')
            or not timestamp(scope.get('window_start')) or not timestamp(scope.get('window_end'))
            or scope['window_start'] >= scope['window_end']):
        block('Scope', 'invalid_scope', 'Freeze one cohort and a positive UTC interval.')
    sources = payload.get('sources') if isinstance(payload, dict) else None
    if not isinstance(sources, dict):
        sources = {}
    if set(sources) - set(specs):
        block('Input', 'unmapped_objects', 'Remove or explicitly review objects outside the fixed contract.')
    rows = {}
    for name, spec in specs.items():
        source = sources.get(name)
        if not isinstance(source, dict):
            block(name, 'missing_object', f'Obtain a sanitized {name} extract from {spec["candidate_source"]}.')
            continue
        if source.get('schema_revision') != spec['schema_revision']:
            block(name, 'schema_drift', 'Review the field binding against the pinned synthetic-v1 schema.')
        if source.get('scope') != scope:
            block(name, 'scope_mismatch', 'Re-extract for the same frozen cohort and time interval.')
        if not valid(source.get('source_ref'), 'text'):
            block(name, 'missing_provenance', 'Attach a non-secret source revision reference.')
        if not isinstance(scope, dict) or source.get('observed_at') != scope.get('window_end'):
            block(name, 'snapshot_mismatch', 'Supply the frozen end-of-window snapshot; do not relabel stale data.')
        if source.get('complete') is not True:
            block(name, 'incomplete_extract', 'Resolve pagination or feed gaps before asserting completeness.')
        records, expected = source.get('rows'), source.get('expected_ids')
        if (not isinstance(records, list) or not records
                or not isinstance(expected, list) or not expected
                or any(not valid(i, 'text') for i in expected)
                or len(set(expected)) != len(expected)):
            block(name, 'invalid_manifest', 'Supply nonempty rows and a unique frozen expected-ID manifest.')
            continue
        invalid_fields = set()
        for row in records:
            if not isinstance(row, dict):
                invalid_fields.add('<row must be an object>')
                continue
            invalid_fields.update(set(row) - set(spec['fields']))
            invalid_fields.update(field for field, kind in spec['fields'].items()
                                  if not valid(row.get(field), kind))
        if invalid_fields:
            block(name, 'invalid_fields',
                  'Correct mapped fields: ' + ', '.join(sorted(invalid_fields))
                  + '; match contract names, types and units without coercion.')
            continue
        ids = [r['id'] for r in records]
        if len(set(ids)) != len(ids):
            block(name, 'duplicate_identity', 'Reconcile duplicate record IDs at the source.')
        if set(ids) != set(expected):
            block(name, 'coverage_gap', 'Reconcile rows against the separately frozen expected-ID manifest.')
        rows[name] = records
    for name, spec in specs.items():
        for join in spec['joins']:
            if name in rows and join['target'] in rows:
                targets = {r['id'] for r in rows[join['target']]}
                if any(r[join['field']] not in targets for r in rows[name]):
                    block(name, 'orphan_join', f'Resolve {join["field"]} to {join["target"]}.id; never join labels.')
    result = None
    if not blockers:
        def exact_cover(name, field, target):
            keys = [r[field] for r in rows[name]]
            if len(set(keys)) != len(keys) or set(keys) != {r['id'] for r in rows[target]}:
                block(name, 'grain_or_coverage_mismatch', f'Provide exactly one record per {target}; reconcile missing or duplicate joins.')
        if industry == 'energy':
            # Multiple ledger entries per contract are allowed, but each contract needs both sides.
            for name in ('Bookings', 'RevenueEntry'):
                if {r['contract_id'] for r in rows[name]} != {r['id'] for r in rows['Contract']}:
                    block(name, 'contract_coverage_gap', 'Provide both ledger sides for every contract in scope.')
            a = sum(r['amount_minor'] for r in rows['Bookings'])
            b = sum(r['amount_minor'] for r in rows['RevenueEntry'])
            result = {'status': 'difference_only', 'values': {'booked_minor': a, 'recognized_minor': b,
                      'difference_minor': a-b, 'currency': 'USD', 'cause': 'not_established'}}
        elif industry == 'financial-services':
            for name in ('ReportA', 'ReportB'):
                exact_cover(name, 'position_id', 'Position')
            a = sum(r['amount_minor'] for r in rows['ReportA'])
            b = sum(r['amount_minor'] for r in rows['ReportB'])
            result = {'status': 'gross_difference_only', 'values': {'report_a_minor': a, 'report_b_minor': b,
                      'difference_minor': a-b, 'currency': 'USD', 'netting': 'not_evaluated', 'cause': 'not_established'}}
        elif industry == 'healthcare':
            exact_cover('BedAvailability', 'bed_id', 'Bed')
            exact_cover('StaffingCoverage', 'bed_id', 'Bed')
            ready = {r['bed_id'] for r in rows['BedAvailability'] if r['ready']}
            staffed = {r['bed_id'] for r in rows['StaffingCoverage'] if r['staffed']}
            result = {'status': 'bounded_capacity_count', 'values': {'available_staffed_beds': len(ready & staffed),
                      'beds_observed': len(rows['Bed']), 'clinical_suitability': 'not_established'}}
        elif industry == 'manufacturing':
            exact_cover('RateDefinition', 'run_id', 'Run')
            exact_cover('QualityObservation', 'run_id', 'Run')
            if len(rows['Run']) != 1:
                block('Run', 'unsupported_multi_run', 'Select one completed single-product run; no weighted aggregation is implemented.')
            run, rate, quality = rows['Run'][0], rows['RateDefinition'][0], rows['QualityObservation'][0]
            if rate['product_id'] != run['product_id']:
                block('RateDefinition', 'product_mismatch', 'Select the reviewed ideal rate for this product and run.')
            a = Fraction(run['runtime_seconds'], run['planned_seconds'])
            p = Fraction(rate['ideal_cycle_seconds'] * quality['total'], run['runtime_seconds'])
            q = Fraction(quality['good'], quality['total'])
            if any(f > 1 for f in (a, p, q)):
                block('Run', 'implausible_factor', 'Reconcile durations, rate and quality counts; do not cap a factor at one.')
            result = {'status': 'bounded_oee', 'values': {'availability': str(a), 'performance': str(p),
                      'quality': str(q), 'oee': str(a*p*q), 'cause': 'not_established'}}
        else:
            exact_cover('Promise', 'line_id', 'OrderLine')
            exact_cover('DeliverySummary', 'line_id', 'OrderLine')
            if any(not r['full_quantity'] for r in rows['DeliverySummary']):
                block('DeliverySummary', 'partial_delivery', 'Resolve all split quantities before treating a line as delivered.')
            if any(r['delivered_at'] > scope['window_end'] for r in rows['DeliverySummary']):
                block('DeliverySummary', 'after_cutoff', 'Exclude evidence unavailable at the frozen cutoff and re-evaluate completeness.')
            if any(r['original_due_at'] > scope['window_end'] for r in rows['Promise']):
                block('Promise', 'open_cohort', 'Choose a closed cohort whose original promises are due by cutoff.')
            due = {r['line_id']: r['original_due_at'] for r in rows['Promise']}
            on_time = sum(r['line_id'] in due and r['delivered_at'] <= due[r['line_id']] for r in rows['DeliverySummary'])
            total = len(rows['OrderLine'])
            result = {'status': 'original_promise_line_rate', 'values': {'on_time_lines': on_time,
                      'required_lines': total, 'ratio': str(Fraction(on_time, total)), 'grain': 'line', 'cause': 'not_established'}}
    receipt = {'industry': industry, 'evidence': 'synthetic_only', 'mapping_sha256': digest(mapping),
               'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'input_sha256': digest(payload), 'native_mapping': 'unverified',
               'source_refs': sorted({s['source_ref'] for s in sources.values()
                                      if isinstance(s, dict) and valid(s.get('source_ref'), 'text')})}
    return {**receipt, **({'status': 'blocked', 'blockers': blockers} if blockers else result)}


def run_all():
    results = []
    for industry in INDUSTRIES:
        result = assess(industry, json.loads((DATA / f'{industry}-input.json').read_text()))
        expected = json.loads((DATA / f'{industry}-expected.json').read_text())
        result['matches_authored_expectation'] = {k: result.get(k) for k in expected} == expected
        results.append(result)
    return {'evidence': 'synthetic_only', 'results': results,
            'passed': all(r['matches_authored_expectation'] for r in results)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Emit full hash-bound receipts')
    parser.add_argument('--industry', choices=INDUSTRIES)
    parser.add_argument('--input', type=Path, help='Sanitized JSON matching the selected fixed object contract')
    args = parser.parse_args()
    if bool(args.industry) != bool(args.input):
        parser.error('--industry and --input must be provided together')
    try:
        if args.input:
            result = assess(args.industry, json.loads(args.input.read_text(), parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON'))))
            passed = result['status'] != 'blocked'
        else:
            result = run_all()
            passed = result['passed']
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Cannot evaluate input: {type(exc).__name__}\n')
    if args.json:
        print(json.dumps(result, indent=2, allow_nan=False))
    else:
        for row in result.get('results', [result]):
            print(f"{row['industry']}: {row['status']}")
            for blocker in row.get('blockers', []):
                print(f"  {blocker['object']} | {blocker['owner']} | {blocker['reason']}: {blocker['next_action']}")
            if 'values' in row:
                print('  ' + json.dumps(row['values'], sort_keys=True))
        print('Synthetic only. Native bindings, source truth and independent validation remain unverified.')
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
