import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import reliability
from standards_export import export, recovered_concepts, SKOS

ROOT = Path(__file__).parents[1]


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads((ROOT / 'examples/reliability-cases.json').read_text())[0]

    def test_reviewed_cases(self):
        result = reliability.evaluate_cases()
        self.assertEqual(len(result['cases']), 8)
        self.assertTrue(result['passed'], result)

    def test_wrong_same_status_payload_fails(self):
        wrong = dict(self.case['expected'], total=10001)
        with patch('reliability.assess', return_value=wrong):
            self.assertFalse(reliability.evaluate_cases()['passed'])

    def test_wrong_scalar_type_fails(self):
        wrong = dict(self.case['expected'], total=10000.0)
        with patch('reliability.assess', return_value=wrong):
            self.assertFalse(reliability.evaluate_cases()['passed'])

    def test_rounding_cannot_turn_miss_into_pass(self):
        obs = dict(self.case['observation'], total=1000001, successful=999000)
        self.assertEqual(reliability.assess(obs, self.case['objective'])['status'], 'objective_missed')

    def test_invalid_input_controls(self):
        for changes in ({'successful':True}, {'total':-1}, {'coverage_complete':1},
                        {'source':''}, {'window_start':'yesterday'},
                        {'window_end':'2026-09-01T00:00:00Z'}):
            with self.subTest(changes=changes):
                result = reliability.assess(dict(self.case['observation'], **changes), self.case['objective'])
                self.assertIn(result['status'], ('invalid_input', 'insufficient_evidence'))
        self.assertEqual(reliability.assess([], {})['status'], 'invalid_input')

    def test_invalid_objectives(self):
        for value in (True, 0, 10001, '9990'):
            self.assertEqual(reliability.assess(self.case['observation'],
                             dict(self.case['objective'], target_basis_points=value))['status'], 'invalid_input')

    def test_no_mutation(self):
        before = copy.deepcopy(self.case)
        reliability.assess(self.case['observation'], self.case['objective'])
        self.assertEqual(self.case, before)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((ROOT / 'ontology.json').read_text())

    def test_projection_round_trip_and_loss(self):
        result = export(self.model)
        self.assertEqual(recovered_concepts(result['document']), sorted(self.model['concepts'], key=lambda c:c['id']))
        self.assertFalse(result['report']['lossless'])
        self.assertFalse(result['report']['executable'])
        self.assertIn('/metrics', result['report']['omitted_source_paths'])
        self.assertIn('/relationships', result['report']['omitted_source_paths'])
        self.assertNotIn('read_recognized_revenue', json.dumps(result['document']))

    def test_unknown_fields_reported(self):
        self.model['odd/key~'] = True
        self.model['future_policy'] = {'must_not_lose_silently': True}
        self.model['concepts'][0]['owner'] = 'fixture'
        report = export(self.model)['report']
        self.assertIn('/odd~1key~0', report['omitted_source_paths'])
        self.assertIn('/future_policy', report['omitted_source_paths'])
        self.assertIn('/concepts/0/owner', report['omitted_source_paths'])

    def test_changed_definition_changes_identity(self):
        first = export(self.model)
        self.model['concepts'][0]['definition'] += ' Updated.'
        second = export(self.model)
        self.assertNotEqual(first['report']['source_sha256'], second['report']['source_sha256'])
        self.assertNotEqual(first['document'][0]['@id'], second['document'][0]['@id'])

    def test_no_false_semantic_equivalence(self):
        result = json.dumps(export(self.model)['document'])
        for term in ('broader', 'sameAs', 'exactMatch', 'subClassOf'):
            self.assertNotIn(term, result)

    def test_invalid_registry_rejected(self):
        self.model['concepts'].append(self.model['concepts'][0])
        with self.assertRaises(ValueError):
            export(self.model)

    def test_export_fixture_parity(self):
        expected = json.loads((ROOT / 'examples/skos-export.json').read_text())
        self.assertEqual(export(self.model), expected)

    def test_unicode_and_quotes_survive_projection(self):
        self.model['concepts'][0]['definition'] = 'A "quoted" café\nwith a newline.'
        doc = json.loads(json.dumps(export(self.model)['document']))
        self.assertEqual(recovered_concepts(doc), sorted(self.model['concepts'], key=lambda c:c['id']))


if __name__ == '__main__':
    unittest.main()
