import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from evaluate import ROOT, evaluate, report


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
        cases = [{'case': 'denied', 'expected_status': 'read_plan_only'}]
        before = copy.deepcopy(cases)
        self.assertEqual(evaluate(cases)['passed'], 0)
        self.assertEqual(cases, before)
        with self.assertRaises(ValueError):
            evaluate([{'case': 'invented', 'expected_status': 'denied'}])

    def test_checked_in_receipt_matches_and_cli_is_portable(self):
        expected = json.loads((ROOT / 'examples/decision-results.json').read_text())
        self.assertEqual(report(), expected)
        with tempfile.TemporaryDirectory() as directory:
            output = subprocess.check_output([sys.executable, str(ROOT / 'evaluate.py')], cwd=directory, text=True)
        self.assertEqual(json.loads(output), expected)
