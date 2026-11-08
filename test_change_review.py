"""Change governance checks using independently constructed mutations."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from change_review import fingerprint, review_changes
from demo import MODEL


class ChangeReview(unittest.TestCase):
    def setUp(self):
        self.before = copy.deepcopy(MODEL)
        self.after = copy.deepcopy(MODEL)

    def review(self):
        return review_changes(self.before, self.after)

    def bump(self):
        self.after['version'] = '0.2.0'
        self.after['metrics'][0]['version'] = '0.2.0'

    def test_unchanged_and_no_mutation(self):
        self.assertEqual(self.review()['status'], 'unchanged')
        self.assertEqual(self.before, MODEL)
        self.assertEqual(self.after, MODEL)

    def test_same_version_definition_drift(self):
        self.after['metrics'][0]['definition'] = 'A materially different accounting basis'
        result = self.review()
        self.assertEqual(result['status'], 'version_policy_violation')
        self.assertEqual(len(result['violations']), 2)

    def test_bumping_registry_does_not_hide_metric_drift(self):
        self.after['version'] = '0.2.0'
        self.after['metrics'][0]['valid_to'] = '2027-12-31'
        self.assertEqual(len(self.review()['violations']), 1)

    def test_version_change_is_not_approval(self):
        self.bump()
        self.after['metrics'][0]['definition'] = 'Changed definition'
        result = self.review()
        self.assertEqual(result['status'], 'review_required')
        self.assertEqual(result['changes'][1]['kind'], 'contract_review_required')

    def test_lifecycle_revocation_requires_review(self):
        self.bump()
        self.after['metrics'][0]['status'] = 'revoked'
        self.assertEqual(self.review()['status'], 'review_required')
        self.assertIn('status', self.review()['changes'][1]['fields'])

    def test_label_is_descriptive_but_still_versioned(self):
        self.after['metrics'][0]['label'] = 'Clearer label'
        self.assertEqual(self.review()['status'], 'version_policy_violation')
        self.bump()
        self.assertEqual(self.review()['changes'][1]['kind'], 'descriptive')

    def test_reordering_collections_is_not_semantic_drift(self):
        for collection in ('concepts', 'metrics', 'relationships'):
            self.after[collection].reverse()
        self.assertEqual(self.review()['status'], 'unchanged')
        self.assertNotEqual(fingerprint(self.before), fingerprint(self.after))

    def test_removed_metric_and_relationship(self):
        self.after['version'] = '0.2.0'
        self.after['metrics'].pop()
        self.after['relationships'].pop()
        result = self.review()
        self.assertEqual(result['status'], 'review_required')
        self.assertEqual(sum(c['kind'] == 'removed' for c in result['changes']), 2)

    def test_added_concept(self):
        self.after['version'] = '0.2.0'
        self.after['concepts'].append({'id': 'Facility', 'definition': 'Synthetic facility'})
        self.assertEqual(self.review()['changes'][1]['kind'], 'added')

    def test_unknown_extensions_and_null_presence_are_not_ignored(self):
        for collection in ('concepts', 'metrics', 'relationships'):
            with self.subTest(collection=collection):
                self.after = copy.deepcopy(MODEL)
                self.after[collection][0]['extension'] = None
                result = self.review()
                self.assertEqual(result['status'], 'version_policy_violation')
                self.assertEqual(result['changes'][0]['kind'], 'contract_review_required')

    def test_json_types_not_collapsed_by_python_equality(self):
        self.before['metrics'][0]['extension'] = {'value': True}
        self.after['metrics'][0]['extension'] = {'value': 1}
        self.assertEqual(self.review()['status'], 'version_policy_violation')

    def test_invalid_binding_never_produces_valid_review(self):
        self.after['metrics'][0]['action']['operation_id'] = 'write_anything'
        self.assertEqual(self.review()['status'], 'invalid_registry')

    def test_invalid_baseline_and_candidate(self):
        for bad in (None, [], {'metrics': []}):
            self.assertEqual(review_changes(bad, MODEL)['status'], 'invalid_registry')
            self.assertEqual(review_changes(MODEL, bad)['status'], 'invalid_registry')

    def test_nonfinite_extension_rejected(self):
        self.after['extension'] = float('nan')
        self.assertEqual(self.review()['status'], 'invalid_registry')

    def test_fingerprint_stable_under_mapping_order(self):
        self.assertEqual(fingerprint(MODEL), fingerprint(dict(reversed(list(MODEL.items())))))

    def test_cli_exit_codes_and_json_from_other_directory(self):
        script = str(Path(__file__).with_name('change_review.py'))
        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / 'before.json'
            candidate = Path(directory) / 'after.json'
            baseline.write_text(json.dumps(MODEL))
            for value, code, status in ((json.dumps(MODEL), 0, 'unchanged'),
                                        ('{', 1, 'invalid_input'),
                                        ('{"version": "1", "version": "2"}', 1, 'invalid_input')):
                candidate.write_text(value)
                run = subprocess.run([sys.executable, script, str(baseline), str(candidate)],
                                     cwd=directory, capture_output=True, text=True)
                self.assertEqual(run.returncode, code, run.stderr)
                self.assertEqual(json.loads(run.stdout)['status'], status)
            self.after['metrics'][0]['definition'] = 'Changed'
            candidate.write_text(json.dumps(self.after))
            run = subprocess.run([sys.executable, script, str(baseline), str(candidate)],
                                 cwd=directory, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertEqual(json.loads(run.stdout)['status'], 'version_policy_violation')
