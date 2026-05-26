from typing import Protocol


class VolumeBar(Protocol):
    volume: int


def compute_volume_score(bars: list[VolumeBar]) -> float:
    if len(bars) < 2:
        return 0.0

    full_average = sum(bar.volume for bar in bars) / len(bars)
    if full_average <= 0:
        return 0.0

    recent_window = bars[-5:] if len(bars) >= 5 else bars
    recent_average = sum(bar.volume for bar in recent_window) / len(recent_window)
    relative_volume = recent_average / full_average
    return _clamp((relative_volume - 0.5) / 1.5)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
