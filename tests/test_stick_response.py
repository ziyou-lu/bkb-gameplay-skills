"""Synthetic math checks for a library candidate, not hardware or engine tests."""
import importlib.util
import inspect
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'radial_candidate', ROOT / 'skills/gameplay-stick-response/scripts/radial_response.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
response = module.radial_response


class StaticRadialCandidateTests(unittest.TestCase):
    def test_zero_and_deadzone_are_neutral(self):
        for d in (0.0, 0.04, 0.2):
            for x, y in ((0, 0), (d, 0), (0, -d), (d / 2, d / 2)):
                self.assertEqual(response(x, y, deadzone=d, exponent=2.0), (0.0, 0.0))

    def test_just_outside_deadzone_starts_continuously(self):
        d, epsilon = 0.12, 1e-8
        out = response(d + epsilon, 0, deadzone=d, exponent=1.0)[0]
        self.assertAlmostEqual(out, epsilon / (1 - d), places=14)
        self.assertGreater(out, 0)
        self.assertLess(out, 2 * epsilon)

    def test_endpoints_and_full_deflection_remain_full(self):
        for d in (0.0, 0.04, 0.2):
            for exponent in (1.0, 1.4, 3.0):
                for angle in (0, math.pi / 4, math.pi / 2, math.pi, -math.pi / 3):
                    x, y = math.cos(angle), math.sin(angle)
                    ox, oy = response(x, y, deadzone=d, exponent=exponent)
                    self.assertAlmostEqual(math.hypot(ox, oy), 1.0)
                    self.assertAlmostEqual(ox, x)
                    self.assertAlmostEqual(oy, y)

    def test_internal_deflections_below_same_deadzone_linear_baseline(self):
        for amount in (0.15, 0.3, 0.5, 0.8, 0.99):
            linear = response(amount, 0, deadzone=0.1, exponent=1.0)[0]
            curved = response(amount, 0, deadzone=0.1, exponent=2.2)[0]
            self.assertGreater(curved, 0.0)
            self.assertLess(curved, linear)

    def test_sweep_monotone_and_bounded(self):
        for exponent in (1.0, 1.3, 4.0):
            values = [response(i / 1000, 0, deadzone=0.08,
                               exponent=exponent)[0] for i in range(1001)]
            self.assertEqual(values, sorted(values))
            self.assertTrue(all(0 <= v <= 1 for v in values))

    def test_rotational_covariance_and_direction(self):
        for magnitude in (0.0, 0.05, 0.2, 0.7, 1.0):
            expected = response(magnitude, 0, deadzone=0.07, exponent=1.8)[0]
            for degree in range(-180, 181, 15):
                angle = math.radians(degree)
                direction = math.cos(angle), math.sin(angle)
                out = response(magnitude * direction[0], magnitude * direction[1],
                               deadzone=0.07, exponent=1.8)
                self.assertAlmostEqual(out[0], expected * direction[0])
                self.assertAlmostEqual(out[1], expected * direction[1])

    def test_diagonal_outside_circle_saturates_without_overshoot(self):
        for x, y in ((1, 1), (-1, 1), (-1, -1), (1, -1), (0.8, 0.9)):
            ox, oy = response(x, y, deadzone=0.05, exponent=2.0)
            self.assertAlmostEqual(math.hypot(ox, oy), 1.0)
            self.assertAlmostEqual(ox * y - oy * x, 0.0)
            self.assertGreater(ox * x + oy * y, 0.0)

    def test_sign_symmetry_and_immediate_reverse(self):
        for x, y in ((0.3, 0.4), (0.8, -0.4), (1, 0)):
            a = response(x, y, deadzone=0.1, exponent=2.0)
            b = response(-x, -y, deadzone=0.1, exponent=2.0)
            self.assertEqual(b, tuple(-v for v in a))
            self.assertEqual(response(0, 0, deadzone=0.1, exponent=2.0), (0, 0))

    def test_same_sample_independent_of_prior_samples_and_repetition(self):
        kwargs = {'deadzone': 0.06, 'exponent': 2.4}
        expected = response(0.4, 0.2, **kwargs)
        for prior in ((1, 1), (-1, -1), (0, 0), (0.1, 0.0)):
            response(*prior, **kwargs)
            for _ in range(20):
                self.assertEqual(response(0.4, 0.2, **kwargs), expected)
        self.assertEqual(list(inspect.signature(response).parameters),
                         ['x', 'y', 'deadzone', 'exponent'])

    def test_already_processed_upstream_uses_zero_additional_deadzone(self):
        self.assertEqual(response(0.3, 0, deadzone=0, exponent=2), (0.09, 0.0))
        self.assertNotEqual(response(0.3, 0, deadzone=0.1, exponent=2), (0.09, 0.0))

    def test_invalid_configuration_rejected_not_silently_clamped(self):
        for d, exponent in ((-0.1, 2), (1, 2), (2, 2), (0.1, 0), (0.1, 0.99)):
            with self.subTest(d=d, exponent=exponent), self.assertRaises(ValueError):
                response(0.5, 0, deadzone=d, exponent=exponent)

    def test_nonfinite_or_non_numeric_values_rejected(self):
        for field in ('x', 'y', 'deadzone', 'exponent'):
            for bad in (math.nan, math.inf, -math.inf, True, '0.3', None, 10**1000):
                kwargs = dict(x=0.3, y=0.4, deadzone=0.1, exponent=2)
                kwargs[field] = bad
                with self.subTest(field=field, bad=bad), self.assertRaises(ValueError):
                    response(**kwargs)

    def test_out_of_contract_calibrated_axes_rejected(self):
        for x, y in ((1.01, 0), (0, -1.01), (1e100, 1)):
            with self.assertRaises(ValueError):
                response(x, y, deadzone=0.1, exponent=2)


if __name__ == '__main__':
    unittest.main()
