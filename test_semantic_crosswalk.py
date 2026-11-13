"""Documentation drift checks, not live federation/interoperability tests."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent


class SemanticCrosswalkTests(unittest.TestCase):
    def test_crosswalk_tracks_registry_without_promoting_bindings(self):
        registry_bytes = (ROOT / 'ontology.json').read_bytes()
        registry = json.loads(registry_bytes)
        crosswalk = json.loads((ROOT / 'docs/semantic-federation/CROSSWALK.json').read_text())
        self.assertEqual(crosswalk['ontology_sha256'], hashlib.sha256(registry_bytes).hexdigest())
        self.assertEqual(crosswalk['status'], 'design_only_not_runtime_config')
        metric = next(m for m in registry['metrics'] if m['id'] == 'recognized_revenue')
        self.assertEqual(crosswalk['example_local_metric'], metric)
        platforms = crosswalk['platforms']
        self.assertEqual(len(platforms), 6)
        self.assertEqual({p['platform'] for p in platforms},
                         {'salesforce', 'snowflake', 'databricks', 'dbt', 'looker', 'power_bi'})
        for platform in platforms:
            with self.subTest(platform=platform['platform']):
                self.assertEqual(platform['status'], 'design_only')
                self.assertIs(platform['native_binding_verified'], False)
                self.assertEqual(set(platform['metric_fields']), set(metric))
                self.assertEqual(set(platform['metric_fields']['action']), set(metric['action']))
                self.assertTrue(platform['semantic_loss_to_review'].strip())
                self.assertTrue(platform['mulesoft_route'].strip())
                self.assertTrue(platform['source_url'].startswith('https://'))


if __name__ == '__main__':
    unittest.main()
