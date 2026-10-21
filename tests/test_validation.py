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


class TaskRouteTests(unittest.TestCase):
    def setUp(self):
        # Synthetic IDs keep these contract tests independent of the live skill
        # inventory, its size, and the current classification decisions.
        self.catalog = {
            'skills': [
                {'id': 'skill-first', 'mechanisms': ['first-mechanism']},
                {'id': 'skill-second', 'mechanisms': ['second-mechanism']},
            ],
            'task_routes': [
                {
                    'id': 'first-task',
                    'request_examples': ['请把第一类交互做成可复用的完整流程。'],
                    'primary_skill': 'skill-first',
                    'mechanisms': ['first-mechanism'],
                    'evidence_status': 'workflow',
                    'boundary': '只覆盖第一类交互；未运行引擎代码。',
                    'distinct_from': ['second-task'],
                },
                {
                    'id': 'second-task',
                    'request_examples': ['我需要第二类交互的独立工作流。'],
                    'primary_skill': 'skill-second',
                    'mechanisms': ['second-mechanism'],
                    'evidence_status': 'workflow',
                    'boundary': '第二类交互有独立触发条件，不包含第一类交互。',
                    'distinct_from': [],
                },
                {
                    'id': 'first-evidence',
                    'request_examples': ['现有第一类交互案例能证明什么？'],
                    'primary_skill': 'skill-first',
                    'mechanisms': [],
                    'evidence_status': 'evidence_only',
                    'boundary': '只提供已有案例证据，不声称完整实现能力。',
                    'distinct_from': [],
                },
            ],
        }

    def assert_issue(self, prefix):
        issues = v.validate_task_routes(self.catalog)
        self.assertTrue(any(prefix in issue for issue in issues), issues)

    def test_valid_routes_and_shared_targets_without_declared_distinction(self):
        self.assertEqual(v.validate_task_routes(self.catalog), [])

    def test_routes_must_be_present_and_nonempty(self):
        for routes in (None, [], {}, 'first-task'):
            with self.subTest(routes=routes):
                self.catalog['task_routes'] = routes
                self.assert_issue('task_routes must be a non-empty array')
        del self.catalog['task_routes']
        self.assert_issue('task_routes must be a non-empty array')

    def test_route_must_be_an_object(self):
        self.catalog['task_routes'].append('not-an-object')
        self.assert_issue('Invalid task route object')

    def test_unknown_primary_skill_fails(self):
        self.catalog['task_routes'][0]['primary_skill'] = 'missing-skill'
        self.assert_issue('Unknown task route primary_skill')

    def test_workflow_requires_nonempty_mechanisms(self):
        self.catalog['task_routes'][0]['mechanisms'] = []
        self.assert_issue('Workflow task route needs owned mechanisms')

    def test_workflow_missing_mechanism_owner_fails(self):
        self.catalog['skills'][0]['mechanisms'] = []
        self.assert_issue('Task route mechanism not uniquely owned by primary_skill')

    def test_workflow_wrong_mechanism_owner_fails(self):
        self.catalog['task_routes'][0]['mechanisms'] = ['second-mechanism']
        self.assert_issue('Task route mechanism not uniquely owned by primary_skill')

    def test_workflow_multiple_mechanism_owners_fail(self):
        self.catalog['skills'][1]['mechanisms'].append('first-mechanism')
        self.assert_issue('Task route mechanism not uniquely owned by primary_skill')

    def test_independent_routes_cannot_be_merged_even_if_ownership_is_updated(self):
        self.catalog['skills'][0]['mechanisms'].append('second-mechanism')
        self.catalog['skills'][1]['mechanisms'] = []
        self.catalog['task_routes'][1]['primary_skill'] = 'skill-first'
        # Ownership is still unique after the merge; the explicit task boundary
        # must catch the regression independently of the mechanism check.
        self.assertEqual(v.validate_task_routes(self.catalog), [
            'Distinct task routes share primary_skill: first-task -> second-task',
            'Skill has no discovery route: skill-second'])

    def test_skill_without_discovery_route_fails(self):
        self.catalog['skills'].append({'id': 'unrouted-skill', 'mechanisms': ['unused-mechanism']})
        self.assert_issue('Skill has no discovery route')

    def test_evidence_only_cannot_claim_workflow_mechanisms(self):
        self.catalog['task_routes'][2]['mechanisms'] = ['first-mechanism']
        self.assert_issue('Evidence-only task route cannot claim mechanisms')

    def test_duplicate_route_ids_fail(self):
        self.catalog['task_routes'].append(self.catalog['task_routes'][0].copy())
        self.assert_issue('Duplicate task route ID')

    def test_unknown_distinct_route_fails(self):
        self.catalog['task_routes'][0]['distinct_from'] = ['missing-route']
        self.assert_issue('Unknown distinct task route')

    def test_duplicate_distinct_route_fails(self):
        self.catalog['task_routes'][0]['distinct_from'] = ['second-task', 'second-task']
        self.assert_issue('Duplicate task route distinct_from')

    def test_self_distinction_fails(self):
        self.catalog['task_routes'][0]['distinct_from'] = ['first-task']
        self.assert_issue('Task route cannot be distinct from itself')

    def test_invalid_route_ids_fail(self):
        for value in ('', ' ', 'Not a route', [], None):
            with self.subTest(value=value):
                self.catalog['task_routes'][0]['id'] = value
                self.assert_issue('Invalid task route ID')

    def test_empty_or_invalid_examples_fail(self):
        for value in ([], [''], ['  '], ['示例', None], '示例', None):
            with self.subTest(value=value):
                self.catalog['task_routes'][0]['request_examples'] = value
                self.assert_issue('Empty/invalid task route request_examples')

    def test_empty_or_invalid_boundary_fails(self):
        for value in ('', '  ', [], None):
            with self.subTest(value=value):
                self.catalog['task_routes'][0]['boundary'] = value
                self.assert_issue('Empty/invalid task route boundary')

    def test_invalid_evidence_status_fails(self):
        for value in ('', 'executed', [], None):
            with self.subTest(value=value):
                self.catalog['task_routes'][0]['evidence_status'] = value
                self.assert_issue('Invalid task route evidence_status')

    def test_invalid_mechanism_list_fails(self):
        for value in ('first-mechanism', [''], [None], None):
            with self.subTest(value=value):
                self.catalog['task_routes'][0]['mechanisms'] = value
                self.assert_issue('Invalid task route mechanisms')

    def test_duplicate_mechanism_claims_fail(self):
        self.catalog['task_routes'][0]['mechanisms'] *= 2
        self.assert_issue('Duplicate task route mechanism')

    def test_invalid_distinct_list_fails(self):
        for value in ('second-task', [''], [None], None):
            with self.subTest(value=value):
                self.catalog['task_routes'][0]['distinct_from'] = value
                self.assert_issue('Invalid task route distinct_from')


class ReviewedWorkflowBoundaryTests(unittest.TestCase):
    """Protect reviewed real-task boundaries, beyond synthetic schema tests."""

    @classmethod
    def setUpClass(cls):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        cls.routes = {route['id']: route for route in catalog['task_routes']}

    def assert_independent_workflows(self, route_ids):
        routes = [self.routes[rid] for rid in route_ids]
        self.assertTrue(all(r['evidence_status'] == 'workflow' for r in routes))
        self.assertEqual(len({r['primary_skill'] for r in routes}), len(routes))
        for left in routes:
            for right in routes:
                if left is not right:
                    self.assertIn(right['id'], left['distinct_from'])

    def test_jump_command_eligibility_and_spatial_correction_are_distinct(self):
        self.assert_independent_workflows(
            ['jump-input-buffer', 'jump-forgiveness', 'ceiling-corner-correction'])

    def test_damage_amount_space_and_time_are_distinct(self):
        self.assert_independent_workflows(
            ['low-health-damage-reduction', 'hurtbox-tolerance', 'post-hit-protection'])
        for rid in ('low-health-damage-reduction', 'post-hit-protection'):
            self.assertIn('health-damage-ui', self.routes[rid]['distinct_from'])
            self.assertIn('hit-recovery', self.routes[rid]['distinct_from'])

    def test_legacy_evidence_routes_remain_limited_under_current_owner(self):
        for old, current in [('jump-buffer-evidence', 'jump-input-buffer'),
                             ('mercy-frames-evidence', 'post-hit-protection')]:
            with self.subTest(old=old):
                self.assertEqual(self.routes[old]['evidence_status'], 'evidence_only')
                self.assertEqual(self.routes[old]['mechanisms'], [])
                self.assertEqual(self.routes[old]['primary_skill'],
                                 self.routes[current]['primary_skill'])

    def test_pointer_curve_mapping_is_not_self_steering_or_command_buffering(self):
        route = self.routes['pointer-curvature-steering']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('steering-assistance', 'jump-input-buffer', 'attack-direction',
                      'camera-feedback', 'movement-feedback', 'locomotion-contacts'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])

    def test_deformable_support_is_not_visual_scale_or_contact_coverage(self):
        route = self.routes['deformable-support']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('motion-deformation', 'contact-response',
                      'locomotion-contacts', 'surface-aftermath'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])

    def test_occlusion_reveal_moves_out_of_target_discoverability(self):
        reveal = self.routes['occlusion-reveal']
        discovery = self.routes['world-readability']
        self.assertNotEqual(reveal['primary_skill'], discovery['primary_skill'])
        self.assertIn('world-readability', reveal['distinct_from'])
        self.assertIn('occlusion-reveal', discovery['distinct_from'])
        self.assertIn('occluded-character-indicator', reveal['mechanisms'])
        self.assertNotIn('occluded-character-indicator', discovery['mechanisms'])
        self.assertEqual(discovery['mechanisms'], ['target-discoverability'])


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

    def test_task_routes_are_required_by_repository_validation(self):
        self.mutate_json('catalog.json', lambda d: d.pop('task_routes', None))
        self.assert_issue('task_routes must be a non-empty array')

    def test_duplicate_source_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'].append(d['posts'][0].copy()))
        self.assert_issue('Duplicate source IDs')

    def test_duplicate_mechanism_owner_fails(self):
        self.mutate_json('catalog.json', lambda d: d['skills'][1]['mechanisms'].append(d['skills'][0]['mechanisms'][0]))
        self.assert_issue('Duplicate mechanism owner')

    def test_url_id_mismatch_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(url='https://www.instagram.com/p/OtherID/'))
        self.assert_issue('URL/source ID mismatch')

    def test_visible_editor_setting_is_not_code_execution(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(parameters=[{
            'name': 'editor_example', 'value': 30.0, 'unit': 'unspecified',
            'provenance': 'visible_editor_setting',
        }]))
        posts = json.loads((self.root / 'sources/posts.json').read_text())['posts']
        (self.root / 'sources/INDEX.md').write_text(v.render_source_index(posts))
        self.assertFalse(posts[0]['code_executed'])
        self.assertEqual(v.validate(self.root), [])

    def test_unknown_parameter_provenance_fails(self):
        self.mutate_json('sources/posts.json', lambda d: d['posts'][0].update(parameters=[{
            'name': 'unverified', 'value': 30.0, 'unit': 'unspecified',
            'provenance': 'assumed_verified',
        }]))
        self.assert_issue('Invalid example parameter')

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
