"""Counterexamples target inflated totals, wrong joins, stale/missing evidence and blanket refusal."""
from copy import deepcopy
import json
import subprocess
import sys
import unittest

from industry_proof import DATA, INDUSTRIES, ROOT, assess, run_all


def fixture(industry):
    return json.loads((DATA / f'{industry}-input.json').read_text())


class IndustryProofTests(unittest.TestCase):
    def assert_blocked(self, industry, data, reason):
        result = assess(industry, data)
        self.assertEqual(result['status'], 'blocked')
        self.assertNotIn('values', result)
        self.assertIn(reason, [b['reason'] for b in result['blockers']])
        for blocker in result['blockers']:
            self.assertTrue(blocker['owner'])
            self.assertTrue(blocker['next_action'])

    def test_five_complete_results_match_separately_authored_values(self):
        result = run_all()
        self.assertEqual(len(result['results']), 5)
        self.assertTrue(result['passed'])
        for industry in INDUSTRIES:
            actual = assess(industry, fixture(industry))
            expected = json.loads((DATA / f'{industry}-expected.json').read_text())
            self.assertEqual({k: actual[k] for k in ('status', 'values')}, expected)

    def test_all_objects_require_complete_typed_versioned_aligned_evidence(self):
        for industry in INDUSTRIES:
            original = fixture(industry)
            for name in original['sources']:
                mutations = {
                    'schema_drift': lambda s: s.update(schema_revision='changed'),
                    'scope_mismatch': lambda s: s['scope'].update(cohort='different'),
                    'snapshot_mismatch': lambda s: s.update(observed_at='2026-11-01T00:00:00Z'),
                    'incomplete_extract': lambda s: s.update(complete=False),
                    'missing_provenance': lambda s: s.update(source_ref=''),
                    'invalid_manifest': lambda s: s.update(expected_ids=[]),
                    'coverage_gap': lambda s: s['expected_ids'].append('missing-row'),
                    'duplicate_identity': lambda s: s['rows'].append(deepcopy(s['rows'][0])),
                    'invalid_fields': lambda s: s['rows'][0].update(id=True),
                }
                for reason, mutate in mutations.items():
                    with self.subTest(industry=industry, object=name, mutation=reason):
                        data = deepcopy(original)
                        mutate(data['sources'][name])
                        self.assert_blocked(industry, data, reason)
                with self.subTest(industry=industry, object=name, mutation='missing_object'):
                    data = deepcopy(original)
                    del data['sources'][name]
                    self.assert_blocked(industry, data, 'missing_object')

    def test_missing_fields_are_named_in_one_actionable_request(self):
        data = fixture('energy')
        row = data['sources']['RevenueEntry']['rows'][0]
        del row['currency']
        del row['amount_minor']
        result = assess('energy', data)
        self.assertEqual(result['status'], 'blocked')
        gaps = [b for b in result['blockers'] if b['object'] == 'RevenueEntry']
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]['owner'], 'Accounting')
        self.assertIn('amount_minor, currency', gaps[0]['next_action'])
        self.assertNotIn('values', result)

    def test_every_join_rejects_orphans(self):
        for industry in INDUSTRIES:
            mapping = json.loads((DATA / f'{industry}-map.json').read_text())
            for obj in mapping['objects']:
                for join in obj['joins']:
                    with self.subTest(industry=industry, object=obj['name']):
                        data = fixture(industry)
                        data['sources'][obj['name']]['rows'][0][join['field']] = 'unknown'
                        self.assert_blocked(industry, data, 'orphan_join')

    def test_booleans_and_floats_are_not_money_or_counts(self):
        for industry in INDUSTRIES:
            mapping = json.loads((DATA / f'{industry}-map.json').read_text())
            for obj in mapping['objects']:
                for field, kind in obj['fields'].items():
                    if kind.endswith('_int'):
                        for value in (True, 1.5, -1, None):
                            with self.subTest(industry=industry, field=field, value=value):
                                data = fixture(industry)
                                data['sources'][obj['name']]['rows'][0][field] = value
                                self.assert_blocked(industry, data, 'invalid_fields')

    def test_duplicate_logical_grain_despite_unique_record_ids(self):
        for industry, name, key in (
                ('financial-services', 'ReportA', 'position_id'),
                ('healthcare', 'BedAvailability', 'bed_id'),
                ('manufacturing', 'RateDefinition', 'run_id'),
                ('retail', 'Promise', 'line_id')):
            with self.subTest(industry=industry):
                data = fixture(industry)
                source = data['sources'][name]
                row = deepcopy(source['rows'][0])
                row['id'] = 'duplicate-logical-grain'
                source['rows'].append(row)
                source['expected_ids'].append(row['id'])
                self.assert_blocked(industry, data, 'grain_or_coverage_mismatch')

    def test_energy_contract_coverage_and_wrong_currency(self):
        data = fixture('energy')
        data['sources']['Contract']['rows'].append({'id': 'contract-2', 'account_id': 'party-1'})
        data['sources']['Contract']['expected_ids'].append('contract-2')
        self.assert_blocked('energy', data, 'contract_coverage_gap')
        data = fixture('energy')
        data['sources']['RevenueEntry']['rows'][0]['currency'] = 'EUR'
        self.assert_blocked('energy', data, 'invalid_fields')

    def test_manufacturing_invalid_factor_zero_denominator_and_product(self):
        for name, field, value, reason in (
                ('Run', 'planned_seconds', 0, 'invalid_fields'),
                ('Run', 'runtime_seconds', 101, 'implausible_factor'),
                ('RateDefinition', 'ideal_cycle_seconds', 3, 'implausible_factor'),
                ('QualityObservation', 'good', 41, 'implausible_factor'),
                ('RateDefinition', 'product_id', 'other-product', 'product_mismatch')):
            with self.subTest(field=field):
                data = fixture('manufacturing')
                data['sources'][name]['rows'][0][field] = value
                self.assert_blocked('manufacturing', data, reason)

    def test_retail_partial_late_and_revised_promises(self):
        for name, field, value, reason in (
                ('DeliverySummary', 'full_quantity', False, 'partial_delivery'),
                ('DeliverySummary', 'delivered_at', '2026-11-03T00:00:00Z', 'after_cutoff'),
                ('Promise', 'original_due_at', '2026-11-03T00:00:00Z', 'open_cohort'),
                ('Promise', 'original_due_at', '2026-11-01T12:00:00+00:00', 'invalid_fields')):
            with self.subTest(field=field):
                data = fixture('retail')
                data['sources'][name]['rows'][0][field] = value
                self.assert_blocked('retail', data, reason)
        data = fixture('retail')
        row = data['sources']['Promise']['rows'][0]
        row['revised_due_at'] = row.pop('original_due_at')
        self.assert_blocked('retail', data, 'invalid_fields')

    def test_answerable_changes_are_computed_not_fixture_lookup(self):
        data = fixture('energy')
        data['sources']['RevenueEntry']['rows'][0]['amount_minor'] = 120000001
        self.assertEqual(assess('energy', data)['values']['difference_minor'], -1)
        data = fixture('financial-services')
        data['sources']['ReportB']['rows'][0]['amount_minor'] = 10000
        self.assertEqual(assess('financial-services', data)['values']['difference_minor'], 0)
        data = fixture('healthcare')
        data['sources']['StaffingCoverage']['rows'][0]['staffed'] = False
        self.assertEqual(assess('healthcare', data)['values']['available_staffed_beds'], 0)
        data = fixture('manufacturing')
        data['sources']['QualityObservation']['rows'][0]['good'] = 0
        self.assertEqual(assess('manufacturing', data)['values']['oee'], '0')
        data = fixture('retail')
        data['sources']['DeliverySummary']['rows'][1]['delivered_at'] = '2026-11-01T12:00:00Z'
        self.assertEqual(assess('retail', data)['values']['ratio'], '1')

    def test_empty_and_malformed_input_fail_closed(self):
        for data in (None, [], {}, {'industry': 'energy', 'scope': [], 'sources': []}):
            self.assertEqual(assess('energy', data)['status'], 'blocked')
        for start, end in [('2026-11-02T00:00:00Z', '2026-11-01T00:00:00Z'),
                           ('2026-11-01', '2026-11-02'),
                           ('2026-11-01T00:00:00Z', '2026-11-01T00:00:00Z')]:
            data = fixture('energy')
            data['scope'].update(window_start=start, window_end=end)
            self.assert_blocked('energy', data, 'invalid_scope')

    def test_receipt_changes_with_input_and_is_order_stable(self):
        data = fixture('energy')
        before = assess('energy', data)
        self.assertEqual(before, assess('energy', dict(reversed(list(data.items())))))
        data['sources']['Bookings']['rows'][0]['amount_minor'] += 1
        after = assess('energy', data)
        self.assertNotEqual(before['input_sha256'], after['input_sha256'])
        self.assertEqual(before['mapping_sha256'], after['mapping_sha256'])

    def test_cli_success_and_incomplete_input_exit_codes(self):
        import tempfile
        result = subprocess.run([sys.executable, str(ROOT/'industry_proof.py'), '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['passed'])
        with tempfile.TemporaryDirectory() as directory:
            from pathlib import Path
            path = Path(directory)/'input.json'
            path.write_text('{}')
            result = subprocess.run([sys.executable, str(ROOT/'industry_proof.py'), '--industry', 'energy', '--input', str(path), '--json'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'blocked')
            path.write_text('{"bad": NaN}')
            result = subprocess.run([sys.executable, str(ROOT/'industry_proof.py'), '--industry', 'energy', '--input', str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
