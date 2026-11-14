"""Negative controls for reproduction receipts and captured demo."""
import subprocess
import unittest
from unittest.mock import patch
from scripts.reproduce import passed, run, transcript


class ReproductionTests(unittest.TestCase):
    def test_empty_or_partial_success_is_not_pass(self):
        self.assertFalse(passed([]))
        self.assertFalse(passed([{'exit_code': 0}, {'exit_code': 1}]))
        self.assertTrue(passed([{'exit_code': 0}]))

    def test_failed_demo_cannot_be_presented_as_success(self):
        with patch('scripts.reproduce.run', return_value={'exit_code': 1}):
            with self.assertRaises(RuntimeError):
                transcript()

    def test_command_failure_retains_diagnostics(self):
        with patch('scripts.reproduce.subprocess.run', return_value=subprocess.CompletedProcess([], 7, '', 'failed')):
            result = run(['python3', 'missing.py'])
        self.assertEqual(result['exit_code'], 7)
        self.assertEqual(result['stderr'], 'failed')

    def test_timeout_does_not_emit_success(self):
        with patch('scripts.reproduce.subprocess.run', side_effect=subprocess.TimeoutExpired([], 120)):
            with self.assertRaises(subprocess.TimeoutExpired):
                run(['python3', 'hung.py'])
