from typing import Protocol


class VolatilityBar(Protocol):
    high: float
    low: float
    close: float


def compute_volatility_score(bars: list[VolatilityBar]) -> float:
    expected_move_pct = compute_expected_move_pct(bars)
    if expected_move_pct <= 0.0:
        return 0.0

    # Scanner v1 favors moderate movement: too little is stale, too much is noisy.
    target_move_pct = 2.0
    distance_from_target = abs(expected_move_pct - target_move_pct)
    return _clamp(1.0 - (distance_from_target / target_move_pct))


def compute_expected_move_pct(bars: list[VolatilityBar]) -> float:
    if not bars:
        return 0.0

    range_percentages = [
        ((bar.high - bar.low) / bar.close) * 100.0
        for bar in bars
        if bar.close > 0 and bar.high >= bar.low
    ]
    if not range_percentages:
        return 0.0

    recent_window = range_percentages[-5:] if len(range_percentages) >= 5 else range_percentages
    return sum(recent_window) / len(recent_window)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
