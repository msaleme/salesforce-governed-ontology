import copy
import unittest
from demo import MODEL, resolve, reconcile, fixtures


class SemanticControls(unittest.TestCase):
    def test_relationship_references(self):
        ids = [c['id'] for c in MODEL['concepts']]
        self.assertEqual(len(ids), len(set(ids)))
        for r in MODEL['relationships']:
            self.assertIn(r['source'], ids)
            self.assertIn(r['target'], ids)

    def test_ambiguity(self):
        self.assertEqual(resolve('revenue', {'finance:read'})['status'], 'clarification_required')

    def test_definitions_and_operations_distinct(self):
        a = resolve('booked_revenue', {'finance:read'})
        b = resolve('recognized_revenue', {'finance:read'})
        self.assertEqual(a['status'], 'read_plan_only')
        self.assertEqual(b['status'], 'read_plan_only')
        self.assertNotEqual(a['definition'], b['definition'])
        self.assertNotEqual(a['operation'], b['operation'])

    def test_denied_fixture(self):
        for metric in ('revenue', 'recognized_revenue'):
            self.assertEqual(resolve(metric, set())['status'], 'denied')

    def test_unknown_concept(self):
        self.assertEqual(resolve('cash_receipts', {'finance:read'})['status'], 'unsupported_concept')

    def test_expired_definition(self):
        self.assertEqual(resolve('booked_revenue', {'finance:read'}, as_of='2027-01-01')['status'], 'definition_unavailable')

    def test_draft_and_revoked(self):
        for state in ('draft', 'revoked'):
            model = copy.deepcopy(MODEL)
            model['metrics'][0]['status'] = state
            self.assertEqual(resolve('booked_revenue', {'finance:read'}, model=model)['status'], 'definition_unavailable')

    def test_no_approval(self):
        model = copy.deepcopy(MODEL)
        model['metrics'][0]['approval'] = {}
        self.assertEqual(resolve('booked_revenue', {'finance:read'}, model=model)['status'], 'definition_unavailable')

    def test_no_write_or_unknown_operation(self):
        for key, value in [('side_effect', 'write'), ('operation_id', 'arbitrary_url')]:
            model = copy.deepcopy(MODEL)
            model['metrics'][0]['action'][key] = value
            self.assertEqual(resolve('booked_revenue', {'finance:read'}, model=model)['status'], 'unsupported_action')

    def test_explained_bridge(self):
        result = reconcile(*fixtures())
        self.assertEqual(result['status'], 'explained_by_fixture_bridge')
        self.assertEqual(result['difference_minor'], 30000000)
        self.assertIn('fixture:reconciliation:001', result['sources'])

    def test_difference_does_not_prove_cause(self):
        a, b, _ = fixtures()
        result = reconcile(a, b)
        self.assertEqual(result['status'], 'difference_only')
        self.assertNotIn('explanation', result)

    def test_dimension_mismatch(self):
        for dimension in ('currency', 'period', 'operator_id', 'contract_id'):
            a, b, c = fixtures()
            b[dimension] = 'different'
            self.assertEqual(reconcile(a, b, c)['status'], 'incompatible_dimensions')

    def test_invalid_bridge(self):
        a, b, c = fixtures()
        c['amount_minor'] = 1
        self.assertEqual(reconcile(a, b, c)['status'], 'invalid_bridge')

    def test_invalid_amount(self):
        a, b, c = fixtures()
        a['amount_minor'] = float('nan')
        self.assertEqual(reconcile(a, b, c)['status'], 'invalid_amount')

    def test_missing_source(self):
        a, b, c = fixtures()
        del b['source']
        self.assertEqual(reconcile(a, b, c)['status'], 'missing_or_wrong_source')


if __name__ == '__main__':
    unittest.main()
