import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class SourceIdentityTests(unittest.TestCase):
    def test_same_post_across_routes(self):
        urls = [
            'https://www.instagram.com/p/Deuo1C7TfMW/',
            'https://www.instagram.com/reel/Deuo1C7TfMW/?igsh=example',
            'https://instagram.com/reels/Deuo1C7TfMW/#caption',
            'https://www.instagram.com/porsukgames/reel/Deuo1C7TfMW/',
        ]
        self.assertEqual({v.post_id_from_url(x) for x in urls}, {'Deuo1C7TfMW'})

    def test_rejects_non_post_and_lookalike_urls(self):
        for url in ['https://instagram.com/', 'https://instagram.com/author/',
                    'https://instagram.com.evil.example/reel/id/',
                    'https://instagram.com@evil.example/reel/id/',
                    'https://user@instagram.com/reel/id/',
                    'http://instagram.com/reel/id/',
                    'https://instagram.com:222/reel/id/']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                v.post_id_from_url(url)


class RepositoryInvariantTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '.git'))

    def tearDown(self):
        self.tmp.cleanup()

    def mutate_json(self, filename, fn):
        path = self.root / filename
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data, ensure_ascii=False))

    def assert_issue(self, prefix):
        self.assertTrue(any(prefix in x for x in v.validate(self.root)), v.validate(self.root))

    def test_valid_repository(self):
        self.assertEqual(v.validate(self.root), [])

    def test_duplicate_source_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'].append(d['posts'][0].copy()))
        self.assert_issue('Duplicate source IDs')

    def test_duplicate_mechanism_owner_fails(self):
        self.mutate_json('catalog.json', lambda d: d['skills'][1]['mechanisms'].append(d['skills'][0]['mechanisms'][0]))
        self.assert_issue('Duplicate mechanism owner')

    def test_url_id_mismatch_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(url='https://www.instagram.com/p/OtherID/'))
        self.assert_issue('URL/source ID mismatch')

    def test_missing_reverse_reference_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(skill_ids=[]))
        self.assert_issue('Missing reverse source link')
        self.assert_issue('Unassigned included source')

    def test_broken_local_reference_fails(self):
        with (self.root / 'README.md').open('a') as f:
            f.write('\n[missing](skills/not-a-skill/SKILL.md)\n')
        self.assert_issue('Broken/outside link')

    def test_unknown_alias_target_fails(self):
        self.mutate_json('catalog.json', lambda d: d['mechanism_aliases'].update(freeze='unknown-new-owner'))
        self.assert_issue('Unknown alias target')

    def test_unsubstantiated_execution_claim_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(code_executed=True))
        self.assert_issue('Execution claimed without evidence')

    def test_unsubstantiated_audio_claim_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(audio_verified=True))
        self.assert_issue('Audio verification claimed without evidence')

    def test_excluded_material_cannot_be_skill_evidence(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(status='excluded'))
        self.assert_issue('Excluded source used by skill')

    def test_stale_derived_index_fails(self):
        with (self.root / 'sources/INDEX.md').open('a') as f:
            f.write('stale content\n')
        self.assert_issue('Source index is stale')

    def test_private_marker_fails(self):
        with (self.root / 'README.md').open('a') as f:
            f.write('\n-----BEGIN OPENSSH PRIVATE KEY-----\n')
        self.assert_issue('Private implementation marker')


if __name__ == '__main__':
    unittest.main()
