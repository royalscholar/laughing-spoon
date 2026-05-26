from typing import Protocol


class FibonacciBar(Protocol):
    high: float
    low: float
    close: float


def compute_fibonacci_score(bars: list[FibonacciBar]) -> float:
    if not bars:
        return 0.0

    swing_high = max(bar.high for bar in bars)
    swing_low = min(bar.low for bar in bars)
    latest_close = bars[-1].close
    swing_range = swing_high - swing_low

    if swing_range <= 0:
        return 0.0

    retracement_levels = [
        swing_high - (swing_range * ratio)
        for ratio in (0.382, 0.5, 0.618)
    ]
    nearest_distance = min(abs(latest_close - level) for level in retracement_levels)
    normalized_distance = nearest_distance / swing_range
    return _clamp(1.0 - (normalized_distance / 0.15))


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
