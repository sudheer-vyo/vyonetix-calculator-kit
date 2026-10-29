"""Behavior tests for the reviewed local release compiler."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / 'deploy_and_ping.py'
spec = importlib.util.spec_from_file_location('reviewed_pipeline', PATH)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class PipelineTests(unittest.TestCase):
    def test_build_never_contacts_network(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(p.urllib.request, 'urlopen', side_effect=AssertionError('network forbidden')):
            out = Path(tmp)
            receipt = p.build(out)
            self.assertEqual(receipt['state'], 'local_candidate_not_deployed')
            report = json.loads((out / 'example-report.json').read_text())
            self.assertEqual((report['matched'], report['unresolved'], report['invalid']), (2, 2, 1))
            self.assertEqual(report['rows'][0]['illustrative_months'], 10)
            self.assertEqual(report['rows'][1]['illustrative_months'], 5)
            self.assertIn('market=AU', report['rows'][0]['tool_url'])
            self.assertNotIn('preset=', report['rows'][0]['tool_url'])

    def test_untrusted_formula_and_path_are_not_executed(self):
        with self.assertRaises(ValueError):
            p.generate_tool_html({'formula_key': 'eval', 'formula_js': 'throw 1', 'slug': 'x', 'title': 'x'})
        with self.assertRaises(ValueError):
            p.generate_tool_html({'formula_key': 'thermal_roll_yield', 'slug': '../x', 'title': 'x'})

    def test_render_has_no_false_verified_or_indexed_claims(self):
        doc = p.generate_tool_html({'formula_key': 'thermal_roll_yield', 'slug': 'label-yield', 'title': '<Test>'})
        self.assertIn('&lt;Test&gt;', doc)
        self.assertIn(p.DISCLOSURE, doc)
        self.assertIn('noindex,nofollow', doc)
        self.assertNotIn('${tool[', doc)
        self.assertNotIn('Verified Part', doc)

    def test_indexnow_requires_real_key_before_requests(self):
        with patch.dict(p.os.environ, {'INDEXNOW_API_KEY': ''}), patch.object(p.urllib.request, 'urlopen', side_effect=AssertionError('network forbidden')):
            with self.assertRaises(ValueError):
                p.indexnow([p.BASE + '/tools/'])

    def test_owned_host_only(self):
        for url in ['http://127.0.0.1/', 'https://example.com/', 'file:///secret']:
            with self.assertRaises(ValueError):
                p.get_public(url)


if __name__ == '__main__':
    unittest.main()
