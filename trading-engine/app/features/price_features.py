from typing import Protocol


class PriceBar(Protocol):
    close: float


def compute_trend_score(bars: list[PriceBar]) -> float:
    if len(bars) < 2 or bars[0].close <= 0:
        return 0.0

    pct_change = (bars[-1].close - bars[0].close) / bars[0].close
    return _clamp((pct_change + 0.05) / 0.20)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
