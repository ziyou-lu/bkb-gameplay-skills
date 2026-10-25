"""Library-authored radial candidate, not source code or an engine controller.

No defaults are supplied: deadzone/exponent are project choices. The caller owns
calibration, device arbitration, already-applied processor detection and failure
recovery. See references/sources.md before adopting this illustrative function.
"""
import math


def radial_response(x, y, *, deadzone, exponent):
    """Map one calibrated 2-D sample; no history, timing, units or side effects."""
    values = (x, y, deadzone, exponent)
    try:
        finite = all(not isinstance(v, bool) and isinstance(v, (int, float))
                     and math.isfinite(v) for v in values)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError('Sample and configuration must be finite real numbers')
    if not 0 <= deadzone < 1 or exponent < 1:
        raise ValueError('Require 0 <= deadzone < 1 and exponent >= 1')
    # Calibrated axes, not arbitrary unbounded or untrusted raw device values.
    if abs(x) > 1 or abs(y) > 1:
        raise ValueError('Calibrated axes must lie in [-1, 1]')
    length = math.hypot(x, y)
    radius = min(length, 1.0)
    if radius <= deadzone:
        return (0.0, 0.0)
    amount = ((radius - deadzone) / (1.0 - deadzone)) ** exponent
    return (x / length * amount, y / length * amount)
