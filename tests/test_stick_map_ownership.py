"""Protect reviewed task boundaries and source assignments, not runtime behavior."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StickMapOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / 'catalog.json').read_text())
        cls.skills = {s['id']: s for s in cls.catalog['skills']}
        cls.routes = {r['id']: r for r in cls.catalog['task_routes']}
        cls.posts = {p['id']: p for p in json.loads((ROOT / 'sources/posts.json').read_text())['posts']}

    def test_static_response_has_one_owner_and_independent_adjacent_routes(self):
        route = self.routes['stick-response']
        self.assertEqual(route['primary_skill'], 'gameplay-stick-response')
        self.assertEqual(route['mechanisms'], ['static-stick-response'])
        owners = [s['id'] for s in self.catalog['skills']
                  if 'static-stick-response' in s['mechanisms']]
        self.assertEqual(owners, ['gameplay-stick-response'])
        for other in ('gamepad-pitch-limits', 'pointer-curvature-steering',
                      'steering-assistance', 'movement-look-decoupling'):
            self.assertNotEqual(route['primary_skill'], self.routes[other]['primary_skill'])
            self.assertIn(other, route['distinct_from'])
            self.assertIn('stick-response', self.routes[other]['distinct_from'])
        self.assertEqual(self.posts['DYJmBg9CEAN']['skill_ids'], ['gameplay-stick-response'])
        self.assertIn('DYJmBg9CEAN', self.skills['gameplay-stick-response']['source_ids'])

    def test_isolation_enriches_selected_room_owner_without_owning_secret_or_backdrop(self):
        owner = 'gameplay-room-map-navigation'
        self.assertEqual(self.posts['DXRACBAAjXA']['skill_ids'], [owner])
        self.assertIn('DXRACBAAjXA', self.skills[owner]['source_ids'])
        self.assertIn('Dd_BhoziQ01', self.skills[owner]['source_ids'])
        for mechanism in ('room-map-navigation', 'selected-room-map-isolation'):
            self.assertEqual([s['id'] for s in self.catalog['skills']
                              if mechanism in s['mechanisms']], [owner])
            self.assertIn(mechanism, self.routes['room-map-navigation']['mechanisms'])
        for other in ('paused-map-backdrop', 'room-secret-markers', 'contextual-ui'):
            self.assertNotEqual(owner, self.routes[other]['primary_skill'])
            self.assertIn(other, self.routes['room-map-navigation']['distinct_from'])
            self.assertIn('room-map-navigation', self.routes[other]['distinct_from'])

    def test_source_execution_flags_not_upgraded_by_library_reference_tests(self):
        for source in ('DYJmBg9CEAN', 'DXRACBAAjXA'):
            self.assertFalse(self.posts[source]['code_executed'])
            self.assertFalse(self.posts[source]['audio_verified'])


if __name__ == '__main__':
    unittest.main()
