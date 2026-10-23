"""Tests for library-authored reference semantics, not game-engine behavior."""
import importlib.util
import itertools
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'shuffle_bag_reference', ROOT / 'skills/gameplay-bag-randomizer/scripts/shuffle_bag.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ShuffleBag = module.ShuffleBag


class BagReferenceTests(unittest.TestCase):
    def test_every_complete_bag_is_a_permutation(self):
        types = tuple('IJLOSTZ')
        for seed in range(20):
            bag = ShuffleBag(types, seed)
            for _ in range(50):
                self.assertCountEqual([bag.draw() for _ in types], types)

    def test_observed_seven_type_gaps_respect_intervening_bound(self):
        for seed in range(20):
            bag = ShuffleBag('IJLOSTZ', seed)
            positions = {}
            for index in range(700):
                item = bag.draw()
                if item in positions:
                    self.assertLessEqual(index - positions[item] - 1, 12)
                positions[item] = index

    def test_exhaustive_small_bag_bound_is_tight(self):
        n = 4
        maximum = 0
        for left in itertools.permutations(range(n)):
            for right in itertools.permutations(range(n)):
                for target in range(n):
                    gap = n - 1 - left.index(target) + right.index(target)
                    maximum = max(maximum, gap)
                    self.assertLessEqual(gap, 2 * (n - 1))
        self.assertEqual(maximum, 6)

    def test_preview_does_not_consume_current_or_future_bags(self):
        bag = ShuffleBag('ABC', 7)
        bag.draw()
        preview = bag.peek(20)
        self.assertEqual(preview, bag.peek(20))
        self.assertEqual(preview, [bag.draw() for _ in range(20)])

    def test_seed_reproducible_in_this_implementation(self):
        a, b = ShuffleBag('ABC', 42), ShuffleBag('ABC', 42)
        self.assertEqual([a.draw() for _ in range(30)], [b.draw() for _ in range(30)])

    def test_single_type_empty_duplicate_and_preview_edges(self):
        bag = ShuffleBag(['A'], 0)
        self.assertEqual([bag.draw() for _ in range(10)], ['A'] * 10)
        self.assertEqual(bag.peek(0), [])
        for types in ([], ['A', 'A'], [''], [1]):
            with self.subTest(types=types), self.assertRaises(ValueError):
                ShuffleBag(types)
        for count in (-1, 1.2, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                bag.peek(count)


if __name__ == '__main__':
    unittest.main()
