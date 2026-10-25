"""Synthetic policy checks only; no renderer, async-session or engine harness."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'map_isolation_candidate',
    ROOT / 'skills/gameplay-room-map-navigation/scripts/isolation_policy.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
visible = module.visible_room_ids


class MapIsolationPolicyTests(unittest.TestCase):
    def test_normal_returns_only_current_base(self):
        self.assertEqual(visible({'A', 'B'}, 'A', isolated=False), {'A', 'B'})

    def test_isolated_contains_only_selected_allowed_room(self):
        self.assertEqual(visible({'A', 'B'}, 'B', isolated=True), {'B'})

    def test_invalid_or_missing_selection_fails_closed(self):
        for selected in ('unknown', None):
            self.assertEqual(visible({'A', 'B'}, selected, isolated=True), set())

    def test_filter_cannot_reveal_disallowed_room(self):
        self.assertEqual(visible({'A'}, 'B', isolated=True), set())
        self.assertEqual(visible(set(), 'A', isolated=True), set())

    def test_a_b_c_selection_uses_current_input_without_history(self):
        base = {'A', 'B', 'C'}
        for selected in ('A', 'B', 'C'):
            self.assertEqual(visible(base, selected, isolated=True), {selected})

    def test_disable_uses_new_base_not_initial_snapshot(self):
        initial = {'A', 'B'}
        self.assertEqual(visible(initial, 'A', isolated=True), {'A'})
        current = {'A', 'C'}  # B loses eligibility; C becomes available.
        self.assertEqual(visible(current, 'A', isolated=False), {'A', 'C'})
        self.assertNotIn('B', visible(current, 'A', isolated=False))

    def test_new_nonselected_rooms_stay_filtered(self):
        self.assertEqual(visible({'A', 'B', 'new'}, 'A', isolated=True), {'A'})

    def test_current_base_removal_immediately_hides_selected(self):
        self.assertEqual(visible({'A', 'B'}, 'A', isolated=True), {'A'})
        self.assertEqual(visible({'B'}, 'A', isolated=True), set())

    def test_repeat_calls_idempotent_and_base_not_mutated(self):
        base = {'A', 'B', 'C'}
        for _ in range(5):
            self.assertEqual(visible(base, 'A', isolated=True), {'A'})
            self.assertEqual(visible(base, 'A', isolated=False), base)
        self.assertEqual(base, {'A', 'B', 'C'})
        self.assertIsInstance(visible(base, 'A', isolated=True), frozenset)

    def test_invalid_contract_values_rejected(self):
        for base, selected, mode in [('A', 'A', True), ({1}, 'A', True),
                                     ({''}, 'A', True), ({'A'}, '', True),
                                     ({'A'}, 2, True), ({'A'}, 'A', 1), (None, 'A', True), ([[]], 'A', True)]:
            with self.subTest(base=base, selected=selected, mode=mode):
                with self.assertRaises(ValueError):
                    visible(base, selected, isolated=mode)


if __name__ == '__main__':
    unittest.main()
