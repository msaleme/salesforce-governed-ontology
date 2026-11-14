"""Schema, user-input and installed CLI contract controls."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import Draft202012Validator
from sgo.byod import evaluate_file, validate_registry
from sgo.cli import main
from sgo.validation import SCHEMA, schema_errors

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/user-metrics.json').read_text())

    def evaluate(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.json'
            path.write_text(json.dumps(data))
            return evaluate_file(path)

    def test_schema_valid_and_both_registries_conform(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.assertEqual(schema_errors(self.data['ontology']), [])
        self.assertEqual(schema_errors(json.loads((ROOT / 'ontology.json').read_text())), [])

    def test_schema_rejects_nested_missing_fields_wrong_types_and_dates(self):
        for field, value in [('action', []), ('grain', ['x','x']), ('valid_from','2026-02-30')]:
            with self.subTest(field=field):
                model = copy.deepcopy(self.data['ontology'])
                model['metrics'][0][field] = value
                self.assertTrue(schema_errors(model))
        del self.data['ontology']['metrics'][0]['action']['operation_id']
        self.assertTrue(schema_errors(self.data['ontology']))

    def test_custom_metric_all_cases_pass_without_mutation(self):
        original = copy.deepcopy(self.data)
        result = self.evaluate(self.data)
        self.assertEqual((result['total'], result['passed']), (4,4))
        self.assertEqual(self.data, original)
        self.assertEqual(result['evidence'], 'user_supplied_unverified')

    def test_full_payload_mismatch_not_hidden_by_same_status(self):
        self.data['cases'][0]['expected_result']['source'] = 'different'
        self.assertEqual(self.evaluate(self.data)['passed'], 3)
        self.data['cases'][0]['expected_result'] = {'status':'read_plan_only'}
        self.assertEqual(self.evaluate(self.data)['passed'], 3)

    def test_custom_graph_and_lifecycle_failures(self):
        for change in ('duplicate', 'edge', 'lineage', 'dates', 'write'):
            model = copy.deepcopy(self.data['ontology'])
            if change == 'duplicate': model['metrics'] *= 2
            if change == 'edge': model['relationships'][0]['source'] = 'Unknown'
            if change == 'lineage': model['metrics'][0]['lineage'] = ['other']
            if change == 'dates': model['metrics'][0]['valid_from'] = '2027-01-01'
            if change == 'write': model['metrics'][0]['action']['side_effect'] = 'write'
            with self.subTest(change=change):
                self.assertTrue(validate_registry(model))

    def test_bad_cases_fail_before_any_plan(self):
        for value in ([], {}, [None], self.data['cases'] + [self.data['cases'][0]]):
            candidate = copy.deepcopy(self.data)
            candidate['cases'] = value
            with patch('sgo.byod.plan') as planner, self.assertRaises(ValueError):
                self.evaluate(candidate)
            planner.assert_not_called()
        for field, value in [('scopes','support:read'), ('as_of','20261114'), ('metric',[]), ('as_of','2026-02-30')]:
            candidate = copy.deepcopy(self.data)
            candidate['cases'][-1]['request'][field] = value
            with patch('sgo.byod.plan') as planner, self.assertRaises(ValueError):
                self.evaluate(candidate)
            planner.assert_not_called()

    def test_bindings_never_execute_or_access_network(self):
        self.data['ontology']['metrics'][0]['source_binding'] = 'https://example.invalid/secret'
        self.data['ontology']['metrics'][0]['lineage'] = ['https://example.invalid/secret']
        self.data['ontology']['metrics'][0]['action']['operation_id'] = '__import__("os").system("false")'
        expected = self.data['cases'][0]['expected_result']
        expected['source'] = 'https://example.invalid/secret'
        expected['operation'] = '__import__("os").system("false")'
        with patch('socket.socket', side_effect=AssertionError('Network access')), patch('os.system', side_effect=AssertionError('Execution')):
            self.assertEqual(self.evaluate(self.data)['passed'], 4)

    def test_cli_exit_codes_and_malformed_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'cases.json'
            for raw in ('{', '{"ontology":{},"ontology":{}}', '{"value":NaN}', 'null'):
                path.write_text(raw)
                with patch('sys.stdout', new_callable=io.StringIO) as output:
                    self.assertEqual(main(['byod',str(path)]), 2)
                    self.assertEqual(json.loads(output.getvalue())['status'], 'invalid_input')
            path.write_text(json.dumps(self.data))
            with patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(main(['byod',str(path)]),0)
            self.data['cases'][0]['expected_result']['version']='wrong'
            path.write_text(json.dumps(self.data))
            with patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(main(['byod',str(path)]),1)
            with patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(main(['byod',str(path.parent/'missing')]),2)

    def test_registry_command_custom_and_invalid(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'registry.json'
            for model, code in [(self.data['ontology'],0), ({},1)]:
                path.write_text(json.dumps(model))
                with patch('sys.stdout',new_callable=io.StringIO):
                    self.assertEqual(main(['validate-registry',str(path)]),code)
