import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from evaluate import ROOT, evaluate, report, result_mismatches
from unittest.mock import patch


class DecisionEvaluation(unittest.TestCase):
    def test_contract_includes_positive_and_negative_controls(self):
        result = report()
        self.assertEqual(result['total'], 12)
        self.assertEqual(result['passed'], 12)
        states = {row['actual_status'] for row in result['cases']}
        self.assertIn('read_plan_only', states)
        self.assertIn('denied', states)
        self.assertIn('explained_by_fixture_bridge', states)
        self.assertIn('difference_only', states)
        self.assertFalse(result['vendor_comparison'])

    def test_wrong_expectation_is_not_marked_passed(self):
        cases = [{'case': 'denied', 'expected_status': 'read_plan_only', 'expected_result': {'status': 'read_plan_only'}}]
        before = copy.deepcopy(cases)
        self.assertEqual(evaluate(cases)['passed'], 0)
        self.assertEqual(cases, before)
        with self.assertRaises(ValueError):
            evaluate([{'case': 'invented', 'expected_status': 'denied', 'expected_result': {'status': 'denied'}}])

    def test_checked_in_receipt_matches_and_cli_is_portable(self):
        expected = json.loads((ROOT / 'examples/decision-results.json').read_text())
        self.assertEqual(report(), expected)
        with tempfile.TemporaryDirectory() as directory:
            output = subprocess.check_output([sys.executable, str(ROOT / 'evaluate.py')], cwd=directory, text=True)
        self.assertEqual(json.loads(output), expected)


    def test_same_status_wrong_payload_is_detected(self):
        cases = json.loads((ROOT / 'examples/decision-cases.json').read_text())
        mutations = [
            ('approved-read', 'source', 'fixture:crm:contract_bookings'),
            ('approved-read', 'operation', 'read_contract_bookings'),
            ('difference-only', 'difference_minor', 300000),
            ('difference-only', 'explanation', 'Invented causal explanation'),
            ('explained', 'sources', []),
            ('ambiguity', 'choices', ['recognized_revenue']),
            ('denied', 'definition', 'Unexpected semantic disclosure'),
        ]
        for name, field, value in mutations:
            with self.subTest(case=name, field=field):
                case = next(c for c in cases if c['case'] == name)
                broken = dict(case['expected_result'], **{field: value})
                with patch('evaluate.run_scenario', return_value={'result': broken}):
                    result = evaluate([case])
                self.assertEqual(result['passed'], 0)
                self.assertEqual(result['cases'][0]['mismatch_fields'], [field])

    def test_missing_field_and_numeric_types_are_not_equivalent(self):
        self.assertEqual(result_mismatches({'amount': 1}, {'amount': True}), ['amount'])
        self.assertEqual(result_mismatches({'amount': 1}, {'amount': 1.0}), ['amount'])
        self.assertEqual(result_mismatches({'sources': ['a']}, {}), ['sources'])
        self.assertEqual(result_mismatches({'a': 1, 'b': 2}, {'b': 2, 'a': 1}), [])

    def test_conflicting_status_expectations_are_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([{'case': 'denied', 'expected_status': 'denied',
                       'expected_result': {'status': 'read_plan_only'}}])
