"""Negative controls for JSON-shaped inputs at public fixture boundaries."""
import copy
import unittest
from demo import MODEL, fixtures, reconcile, resolve


class PlannerBoundary(unittest.TestCase):
    def test_malformed_scope_containers_and_members(self):
        for scopes in ('finance:read', {'finance:read': True}, None, 1, [None], [[]], ['']):
            with self.subTest(scopes=scopes):
                self.assertEqual(resolve('recognized_revenue', scopes), {'status': 'invalid_request'})

    def test_malformed_request_identity_and_date(self):
        for metric in (None, [], {}, 1, ''):
            self.assertEqual(resolve(metric, ['finance:read']), {'status': 'invalid_request'})
        for date in (None, [], {}, 2026, '20260101', '2026-02-30'):
            self.assertEqual(resolve('recognized_revenue', ['finance:read'], as_of=date), {'status': 'invalid_request'})

    def test_missing_fields_never_return_plan_or_exception(self):
        for field in MODEL['metrics'][0]:
            model = copy.deepcopy(MODEL)
            del model['metrics'][0][field]
            self.assertNotEqual(resolve('booked_revenue', ['finance:read'], model=model)['status'], 'read_plan_only', field)

    def test_nested_malformed_values_never_return_plan(self):
        for field in MODEL['metrics'][0]:
            for value in (None, [], {}, 12, True):
                model = copy.deepcopy(MODEL)
                model['metrics'][0][field] = value
                with self.subTest(field=field, value=value):
                    result = resolve('booked_revenue', ['finance:read'], model=model)
                    self.assertEqual(set(result), {'status'})
                    self.assertNotEqual(result['status'], 'read_plan_only')

    def test_invalid_unselected_record_blocks_whole_registry(self):
        model = copy.deepcopy(MODEL)
        model['metrics'][0]['grain'] = []
        for metric in ('recognized_revenue', 'revenue', 'unknown'):
            self.assertEqual(resolve(metric, ['finance:read'], model=model), {'status': 'invalid_registry'})

    def test_duplicate_and_invalid_top_level(self):
        for model in ([], 1, 'text', {}, {'metrics': [None]}):
            self.assertEqual(resolve('recognized_revenue', ['finance:read'], model=model), {'status': 'invalid_registry'})
        model = copy.deepcopy(MODEL)
        model['metrics'].append(copy.deepcopy(model['metrics'][1]))
        self.assertEqual(resolve('recognized_revenue', ['finance:read'], model=model), {'status': 'invalid_registry'})

    def test_denied_request_does_not_disclose_registry_errors(self):
        self.assertEqual(resolve('revenue', [], model={})['status'], 'denied')

    def test_clarification_excludes_unavailable_definitions(self):
        model = copy.deepcopy(MODEL)
        model['metrics'][0]['status'] = 'revoked'
        before = copy.deepcopy(model)
        self.assertEqual(resolve('revenue', ['finance:read'], model=model),
                         {'status': 'clarification_required', 'choices': ['recognized_revenue']})
        self.assertEqual(model, before)
        self.assertEqual(resolve('revenue', ['finance:read'], as_of='2027-01-01'), {'status': 'definition_unavailable'})

    def test_reconciliation_non_object_inputs_and_false_evidence(self):
        a, b, c = fixtures()
        for value in (None, [], 'text', 4):
            self.assertEqual(reconcile(value, b), {'status': 'invalid_input'})
            self.assertEqual(reconcile(a, value), {'status': 'invalid_input'})
        for value in ([], 'text', 4):
            self.assertEqual(reconcile(a, b, value), {'status': 'invalid_bridge'})
        for field in ('source', 'reason'):
            for value in (True, ['invented'], {'text': 'invented'}, ' '):
                bridge = dict(c, **{field: value})
                self.assertEqual(reconcile(a, b, bridge), {'status': 'invalid_bridge'})
