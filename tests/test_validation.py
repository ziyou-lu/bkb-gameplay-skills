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

    def test_bag_selection_does_not_own_reward_display_or_pickup(self):
        route = self.routes['bag-randomizer']
        self.assertEqual(route['mechanisms'], ['shuffle-bag-selection'])
        for other in ('reward-reveal', 'loot-pickup', 'result-counting'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('bag-randomizer', self.routes[other]['distinct_from'])

    def test_sheet_curl_is_not_transform_uv_or_physical_support(self):
        route = self.routes['sheet-curl']
        self.assertEqual(route['mechanisms'], ['sheet-curl-deformation'])
        for other in ('motion-deformation', 'state-driven-surface-motion', 'secondary-motion',
                      'deformable-support', 'cut-surface-rendering', 'surface-aftermath'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('sheet-curl', self.routes[other]['distinct_from'])

    def test_landing_tumble_rules_are_not_cosmetic_landing(self):
        route = self.routes['landing-tumble-recovery']
        self.assertEqual(route['mechanisms'], ['landing-tumble-composition'])
        for other in ('landing-feedback', 'hit-recovery', 'breakables-loot',
                      'loot-pickup', 'launch-pad-feedback', 'contact-response'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('landing-tumble-recovery', self.routes[other]['distinct_from'])

    def test_backdrop_vista_and_ability_mix_have_distinct_owners(self):
        for rid, adjacent in [('paused-map-backdrop', ('room-map-navigation', 'contextual-ui', 'fixed-camera-art-projection')),
                              ('viewpoint-vista-proxies', ('fixed-camera-art-projection', 'impact-physics-activation')),
                              ('ability-audio-mix', ('physics-stage-audio', 'foliage-rustle-response'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_multiray_selection_is_not_reticle_layout_or_feedback(self):
        route = self.routes['multiray-object-selection']
        self.assertEqual(route['mechanisms'], ['multiray-object-selection'])
        for other in ('offset-interaction-reticle', 'contextual-ui', 'world-readability', 'aim-pose'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('multiray-object-selection', self.routes[other]['distinct_from'])

    def test_offset_reticle_is_not_world_marker_or_selection_algorithm(self):
        route = self.routes['offset-interaction-reticle']
        self.assertEqual(route['mechanisms'], ['offset-interaction-reticle'])
        for other in ('multiray-object-selection', 'contextual-ui', 'worldspace-indicators',
                      'world-readability', 'aim-pose'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('offset-interaction-reticle', self.routes[other]['distinct_from'])

    def test_reduced_motion_teleport_is_not_loading_or_movement_permission(self):
        route = self.routes['reduced-motion-teleport']
        self.assertEqual(route['mechanisms'], ['equal-duration-reduced-motion-teleport'])
        for other in ('traversal-transitions', 'scene-transitions', 'dash-feedback', 'speed-camera'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('reduced-motion-teleport', self.routes[other]['distinct_from'])

    def test_pitch_limits_and_room_map_are_not_camera_impulses(self):
        for rid, adjacent in [('gamepad-pitch-limits', ('camera-feedback', 'speed-camera', 'surface-camera-up')),
                              ('room-map-navigation', ('camera-feedback', 'completion-sequences', 'contextual-ui'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_surface_history_is_not_timestamp_expiry_or_surface_mesh(self):
        route = self.routes['surface-history-field']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('timestamped-ground-effects', 'surface-aftermath', 'state-driven-surface-motion'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('surface-history-field', self.routes[other]['distinct_from'])

    def test_rustle_and_roll_momentum_have_distinct_task_owners(self):
        for rid, adjacent in [('foliage-rustle-response', ('physics-stage-audio', 'secondary-motion')),
                              ('dash-roll-momentum', ('dash-feedback', 'landing-feedback', 'traversal-transitions'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_crouch_zone_request_is_not_traversal_release_or_animation(self):
        route = self.routes['crouch-zone-assistance']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('traversal-transitions', 'movement-feedback'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('crouch-zone-assistance', self.routes[other]['distinct_from'])

    def test_ray_depth_and_timestamp_masks_keep_separate_boundaries(self):
        for rid, adjacent in [('raycaster-depth-correction', ('fixed-camera-art-projection', 'camera-feedback')),
                              ('timestamped-ground-effects', ('surface-aftermath', 'state-driven-surface-motion'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_decorative_waterfall_does_not_own_liquid_or_surface_mesh(self):
        route = self.routes['decorative-waterfall']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('surface-aftermath', 'state-driven-surface-motion'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('decorative-waterfall', self.routes[other]['distinct_from'])

    def test_ambient_flipbooks_are_not_combat_bursts_or_target_cues(self):
        route = self.routes['ambient-flipbook-particles']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('impact-visuals', 'world-readability'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('ambient-flipbook-particles', self.routes[other]['distinct_from'])

    def test_art_projection_and_skeletal_shadows_have_distinct_owners(self):
        for rid, adjacent in [('fixed-camera-art-projection', ('state-driven-surface-motion', 'aim-pose')),
                              ('skeletal-planar-shadows', ('worldspace-indicators', 'surface-aftermath'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_bounded_light_aim_is_not_pose_rendering_or_free_look(self):
        route = self.routes['facing-relative-light-aim']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('aim-pose', 'movement-look-decoupling'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('facing-relative-light-aim', self.routes[other]['distinct_from'])

    def test_audio_cutting_and_activation_are_not_generic_harvest_polish(self):
        for rid, adjacent in [('physics-stage-audio', ('prop-toppling-dynamics', 'breakables-loot')),
                              ('precision-branch-cutting', ('breakables-loot', 'prop-appendage-contacts', 'geometric-event-alignment', 'hurtbox-tolerance')),
                              ('impact-physics-activation', ('prop-toppling-dynamics', 'breakables-loot'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_rain_and_dynamic_carry_keep_distinct_task_boundaries(self):
        for rid, adjacent in [('rain-surface-feedback', ('surface-aftermath', 'impact-visuals')),
                              ('dynamic-carry-alignment', ('tool-body-coordination', 'loot-pickup'))]:
            route = self.routes[rid]
            self.assertEqual(route['evidence_status'], 'workflow')
            for other in adjacent:
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_jump_height_and_gravity_are_separate_from_permission(self):
        self.assert_independent_workflows(['variable-jump-height', 'asymmetric-jump-gravity'])
        for rid in ('variable-jump-height', 'asymmetric-jump-gravity'):
            route = self.routes[rid]
            for other in ('jump-forgiveness', 'jump-input-buffer', 'ceiling-corner-correction',
                          'motion-deformation', 'launch-pad-feedback'):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(rid, self.routes[other]['distinct_from'])

    def test_environment_launch_lifecycle_has_its_own_owner(self):
        route = self.routes['launch-pad-feedback']
        self.assertEqual(route['primary_skill'], 'gameplay-launch-pad-feedback')
        self.assertEqual(route['mechanisms'], ['launch-pad-composition'])
        for other in ('motion-deformation', 'landing-feedback', 'stomp-combos',
                      'traversal-transitions', 'jump-forgiveness', 'jump-input-buffer',
                      'dash-feedback', 'mechanical-interactions', 'deformable-support'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('launch-pad-feedback', self.routes[other]['distinct_from'])

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


    def test_predictive_gait_is_not_sprite_facing_or_secondary_follow(self):
        route = self.routes['gait-step-scheduling']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('movement-feedback', 'secondary-motion', 'action-timing',
                      'locomotion-contacts', 'jump-input-buffer'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])

    def test_surface_camera_up_is_not_occlusion_or_transient_feedback(self):
        route = self.routes['surface-camera-up']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('camera-feedback', 'speed-camera', 'occlusion-reveal',
                      'completion-sequences', 'locomotion-contacts'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_gravity_cue_is_not_camera_control_or_target_discovery(self):
        route = self.routes['gravity-orientation-cues']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('surface-camera-up', 'landing-feedback', 'world-readability',
                      'worldspace-indicators', 'impact-visuals', 'gait-step-scheduling'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_movement_look_contract_is_not_visual_facing_or_attack_direction(self):
        route = self.routes['movement-look-decoupling']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('movement-feedback', 'attack-direction', 'aim-pose',
                      'gait-step-scheduling', 'steering-assistance',
                      'pointer-curvature-steering', 'surface-camera-up'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_adhesion_support_is_not_contact_shape_or_visibility_query(self):
        route = self.routes['surface-adhesion']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('locomotion-contacts', 'contact-response',
                      'ceiling-corner-correction', 'occlusion-reveal',
                      'surface-camera-up', 'gait-step-scheduling',
                      'deformable-support', 'traversal-transitions'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_current_ground_reference_is_a_spatial_indicator_not_a_landing_event(self):
        route = self.routes['worldspace-indicators']
        self.assertIn('worldspace-interaction-indicator', route['mechanisms'])
        self.assertIn('ground-position-reference', route['mechanisms'])
        for other in ('gravity-orientation-cues', 'landing-feedback', 'surface-adhesion'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_geometric_event_boundary_is_not_animation_or_result_lifecycle(self):
        route = self.routes['geometric-event-alignment']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('action-timing', 'mechanical-interactions',
                      'breakables-loot', 'contact-response', 'surface-adhesion'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_state_driven_surface_motion_is_not_geometry_or_event_authority(self):
        route = self.routes['state-driven-surface-motion']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('mechanical-interactions', 'motion-deformation',
                      'secondary-motion', 'geometric-event-alignment'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_tool_constraints_are_not_sprite_representation_or_secondary_follow(self):
        route = self.routes['tool-body-coordination']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('aim-pose', 'action-timing', 'gait-step-scheduling',
                      'secondary-motion', 'motion-deformation', 'geometric-event-alignment'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_appendage_contacts_are_not_whole_object_lifecycle_or_support(self):
        route = self.routes['prop-appendage-contacts']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('breakables-loot', 'contact-response', 'deformable-support',
                      'locomotion-contacts', 'secondary-motion'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])

    def test_cut_surface_result_is_not_trigger_or_surface_animation(self):
        route = self.routes['cut-surface-rendering']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('breakables-loot', 'geometric-event-alignment',
                      'surface-aftermath', 'state-driven-surface-motion'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


    def test_precontact_toppling_is_not_contact_or_breakable_lifecycle(self):
        route = self.routes['prop-toppling-dynamics']
        self.assertEqual(route['evidence_status'], 'workflow')
        for other in ('contact-response', 'breakables-loot', 'prop-appendage-contacts',
                      'motion-deformation', 'action-timing'):
            with self.subTest(other=other):
                self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
                self.assertIn(other, route['distinct_from'])
                self.assertIn(route['id'], self.routes[other]['distinct_from'])


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

    def first_skill(self):
        return json.loads((self.root / 'catalog.json').read_text())['skills'][0]

    def test_provenance_not_required_in_execution_prose(self):
        skill = self.first_skill()
        text = (self.root / skill['path']).read_text()
        self.assertTrue(all(pid not in text for pid in skill['source_ids']))
        self.assertEqual(v.validate(self.root), [])

    def test_source_id_leaking_into_execution_is_rejected(self):
        skill = self.first_skill()
        with (self.root / skill['path']).open('a') as f:
            f.write('\n参考 ' + skill['source_ids'][0] + ' 的演示。\n')
        self.assert_issue('Source ID in execution entrypoint')

    def test_platform_link_leaking_into_execution_is_rejected(self):
        skill = self.first_skill()
        with (self.root / skill['path']).open('a') as f:
            f.write('\n[材料](https://www.instagram.com/p/UnregisteredID/)\n')
        self.assert_issue('Source platform link in execution entrypoint')

    def test_missing_evidence_file_is_rejected(self):
        skill = self.first_skill()
        (self.root / skill['evidence_path']).unlink()
        self.assert_issue('Missing evidence reference')

    def test_missing_evidence_source_mapping_is_rejected(self):
        skill = self.first_skill()
        path = self.root / skill['evidence_path']
        path.write_text(path.read_text().replace(skill['source_ids'][0], 'removed-source'))
        self.assert_issue('Source absent from evidence reference')

    def test_evidence_path_cannot_escape_skill_folder(self):
        self.mutate_json('catalog.json', lambda d: d['skills'][0].update(evidence_path='../outside.md'))
        self.assert_issue('Invalid evidence path')

    def test_evidence_link_must_be_discoverable_from_entrypoint(self):
        skill = self.first_skill()
        path = self.root / skill['path']
        path.write_text(path.read_text().replace('(references/sources.md)', '(../gameplay-impact-visuals/SKILL.md)'))
        self.assert_issue('Execution entrypoint does not link evidence reference')

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
