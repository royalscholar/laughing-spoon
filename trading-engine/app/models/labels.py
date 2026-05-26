from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class LabelConfig:
    profit_target_pct: float = 2.0
    max_drawdown_pct: float = 1.0
    holding_period_bars: int = 10


def build_placeholder_label(
    features: Mapping[str, float],
    config: LabelConfig | None = None,
) -> int:
    label_config = config or LabelConfig()
    trade_quality_score = _feature_value(features, "trade_quality_score")
    expected_move_pct = _feature_value(features, "expected_move_pct")
    volatility_score = _feature_value(features, "volatility_score")

    favorable_setup = (
        trade_quality_score >= 0.65
        and expected_move_pct >= label_config.profit_target_pct
        and volatility_score <= 0.85
    )
    return 1 if favorable_setup else 0


def _feature_value(features: Mapping[str, float], key: str) -> float:
    try:
        return float(features.get(key, 0.0))
    except (TypeError, ValueError):
        return 0.0
