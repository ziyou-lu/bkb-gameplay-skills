"""Library-authored algorithm reference, not source-author or engine code.

One copy of each distinct type per shuffled bag. Uses Python's ordinary
pseudorandom generator; no cryptographic, statistical, or cross-runtime promise.
"""
import copy
import random


class ShuffleBag:
    def __init__(self, types, seed=None):
        self.types = tuple(types)
        if not self.types or any(not isinstance(x, str) or not x for x in self.types):
            raise ValueError('types must be nonempty string identifiers')
        if len(set(self.types)) != len(self.types):
            raise ValueError('one distinct identifier per bag entry is required')
        self._rng = random.Random(seed)
        self._bag = []
        self._cursor = 0

    def draw(self):
        if self._cursor == len(self._bag):
            self._bag = list(self.types)
            self._rng.shuffle(self._bag)
            self._cursor = 0
        result = self._bag[self._cursor]
        self._cursor += 1
        return result

    def peek(self, count=1):
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError('preview count must be a nonnegative integer')
        # Reference implementation favors explicit isolation over preview speed.
        clone = copy.deepcopy(self)
        return [clone.draw() for _ in range(count)]
