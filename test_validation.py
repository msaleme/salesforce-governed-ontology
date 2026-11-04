"""Mutation-based checks for malformed registries and semantic binding drift."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from demo import MODEL, resolve
from explore import SCENARIOS, run_scenario
from validation import validate_model

ROOT = Path(__file__).resolve().parent


class RegistryValidation(unittest.TestCase):
    def test_valid_registry_is_not_mutated(self):
        model = copy.deepcopy(MODEL)
        self.assertEqual(validate_model(model), [])
        self.assertEqual(model, MODEL)

    def test_non_object_and_malformed_collections(self):
        for value in (None, [], 'text', 4):
            self.assertTrue(validate_model(value))
        for field in ('concepts', 'relationships', 'metrics'):
            for value in (None, {}, [], [None], ['text']):
                model = copy.deepcopy(MODEL)
                model[field] = value
                self.assertTrue(validate_model(model))

    def test_duplicate_identities(self):
        for collection in ('concepts', 'metrics', 'relationships'):
            model = copy.deepcopy(MODEL)
            model[collection].append(copy.deepcopy(model[collection][0]))
            self.assertTrue(any('duplicate' in e for e in validate_model(model)))

    def test_dangling_relationship(self):
        model = copy.deepcopy(MODEL)
        model['relationships'][0]['target'] = 'NotAConcept'
        self.assertTrue(any('unknown concept' in e for e in validate_model(model)))

    def test_invalid_dates_and_reversed_interval(self):
        for value in ('2026-02-30', '20260101', None, 2026):
            model = copy.deepcopy(MODEL)
            model['metrics'][0]['valid_from'] = value
            self.assertTrue(validate_model(model))
        model['metrics'][0].update(valid_from='2027-01-01', valid_to='2026-01-01')
        self.assertTrue(any('must not exceed' in e for e in validate_model(model)))

    def test_required_metric_fields(self):
        for field in MODEL['metrics'][0]:
            with self.subTest(field=field):
                model = copy.deepcopy(MODEL)
                del model['metrics'][0][field]
                self.assertTrue(validate_model(model))

    def test_binding_swaps_rejected_by_validator_and_resolver(self):
        for index in (0, 1):
            for field in ('source_binding', 'operation_id'):
                model = copy.deepcopy(MODEL)
                a, b = model['metrics'][index], model['metrics'][1 - index]
                if field == 'operation_id':
                    a['action'][field] = b['action'][field]
                else:
                    a[field] = b[field]
                self.assertTrue(validate_model(model))
                self.assertEqual(resolve(a['id'], {'finance:read'}, model=model)['status'], 'binding_mismatch')

    def test_lineage_and_approval_are_required(self):
        for field, value in (('lineage', []), ('lineage', [None]), ('approval', {}), ('approval', None)):
            model = copy.deepcopy(MODEL)
            model['metrics'][0][field] = value
            self.assertTrue(validate_model(model))

    def test_validity_boundaries_inclusive(self):
        for boundary in ('2026-01-01', '2026-12-31'):
            self.assertEqual(resolve('recognized_revenue', {'finance:read'}, as_of=boundary)['status'], 'read_plan_only')
        self.assertEqual(resolve('recognized_revenue', {'finance:read'}, as_of='2025-12-31')['status'], 'definition_unavailable')


class GuidedExperience(unittest.TestCase):
    def test_scenarios_match_contract_without_mutating_model(self):
        before = copy.deepcopy(MODEL)
        for name, (_, _, expected) in SCENARIOS.items():
            self.assertEqual(run_scenario(name)['result']['status'], expected)
        self.assertEqual(before, MODEL)

    def test_cli_runs_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            for args in (['tour', '--json'], ['validate'], ['scenario', 'explained']):
                result = subprocess.run([sys.executable, str(ROOT / 'explore.py'), *args],
                                        cwd=directory, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                json.loads(result.stdout)

    def test_invalid_registry_and_unknown_scenario_exit_nonzero(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            for contents in ('{', '[]', '{"metrics": []}'):
                path.write_text(contents)
                result = subprocess.run([sys.executable, str(ROOT / 'explore.py'), 'validate', str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertFalse(json.loads(result.stdout)['valid'])
        result = subprocess.run([sys.executable, str(ROOT / 'explore.py'), 'scenario', 'unknown'], capture_output=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
