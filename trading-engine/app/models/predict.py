from dataclasses import dataclass
from typing import Mapping

from app.models.registry import get_active_model, get_active_model_version


REQUIRED_FEATURES = (
    "trend_score",
    "volume_score",
    "volatility_score",
    "fibonacci_score",
    "trade_quality_score",
    "expected_move_pct",
)


@dataclass(frozen=True)
class PredictionResult:
    ml_probability: float
    expected_move_pct: float
    expected_drawdown_pct: float
    confidence_score: float
    model_version: str


def predict_opportunity(features: Mapping[str, float]) -> PredictionResult:
    normalized_features = _normalize_features(features)
    model = get_active_model()
    probability_row = model.predict_proba([normalized_features])[0]
    ml_probability = _clamp(probability_row[1])
    expected_move_pct = max(0.0, _feature_value(features, "expected_move_pct"))
    volatility_score = normalized_features["volatility_score"]
    expected_drawdown_pct = round(max(0.5, (1.0 - volatility_score) * 2.0), 4)
    confidence_score = _compute_confidence_score(features)

    return PredictionResult(
        ml_probability=round(ml_probability, 4),
        expected_move_pct=round(expected_move_pct, 4),
        expected_drawdown_pct=expected_drawdown_pct,
        confidence_score=confidence_score,
        model_version=get_active_model_version(),
    )


def _normalize_features(features: Mapping[str, float]) -> dict[str, float]:
    return {
        "trend_score": _clamp(_feature_value(features, "trend_score")),
        "volume_score": _clamp(_feature_value(features, "volume_score")),
        "volatility_score": _clamp(_feature_value(features, "volatility_score")),
        "fibonacci_score": _clamp(_feature_value(features, "fibonacci_score")),
        "trade_quality_score": _clamp(_feature_value(features, "trade_quality_score")),
        "expected_move_pct": max(0.0, _feature_value(features, "expected_move_pct")),
    }


def _compute_confidence_score(features: Mapping[str, float]) -> float:
    present_features = sum(1 for key in REQUIRED_FEATURES if key in features)
    return round(present_features / len(REQUIRED_FEATURES), 4)


def _feature_value(features: Mapping[str, float], key: str) -> float:
    try:
        return float(features.get(key, 0.0))
    except (TypeError, ValueError):
        return 0.0


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
