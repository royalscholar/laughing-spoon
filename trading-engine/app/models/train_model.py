from dataclasses import dataclass, field
from typing import Mapping, Sequence


@dataclass(frozen=True)
class TrainingResult:
    model_version: str
    trained: bool
    sample_count: int
    feature_names: list[str]
    metrics: dict[str, float]


@dataclass
class PlaceholderProbabilityModel:
    model_version: str = "placeholder-v1"
    feature_names: list[str] = field(default_factory=list)
    trained: bool = False

    def fit(
        self,
        X: Sequence[Mapping[str, float]],
        y: Sequence[int],
    ) -> "PlaceholderProbabilityModel":
        if len(X) != len(y):
            raise ValueError("Feature rows and labels must have the same length.")

        self.feature_names = _feature_names_from_rows(X)
        self.trained = True
        return self

    def predict_proba(
        self,
        X: Sequence[Mapping[str, float]],
    ) -> list[list[float]]:
        return [
            _probability_row(row)
            for row in X
        ]


def train_placeholder_model(
    rows: Sequence[Mapping[str, float]],
    labels: Sequence[int],
    model_version: str = "placeholder-v1",
) -> TrainingResult:
    model = PlaceholderProbabilityModel(model_version=model_version)
    model.fit(rows, labels)
    positive_count = sum(1 for label in labels if int(label) == 1)
    sample_count = len(labels)
    positive_rate = positive_count / sample_count if sample_count else 0.0
    return TrainingResult(
        model_version=model_version,
        trained=model.trained,
        sample_count=sample_count,
        feature_names=model.feature_names,
        metrics={"placeholder_positive_rate": round(positive_rate, 4)},
    )


def _probability_row(row: Mapping[str, float]) -> list[float]:
    trade_quality_score = _clamp(_feature_value(row, "trade_quality_score"))
    trend_score = _clamp(_feature_value(row, "trend_score"))
    volume_score = _clamp(_feature_value(row, "volume_score"))
    fibonacci_score = _clamp(_feature_value(row, "fibonacci_score"))
    volatility_score = _clamp(_feature_value(row, "volatility_score"))

    probability = _clamp(
        (0.35 * trade_quality_score)
        + (0.20 * trend_score)
        + (0.15 * volume_score)
        + (0.15 * fibonacci_score)
        + (0.15 * volatility_score)
    )
    return [round(1.0 - probability, 4), round(probability, 4)]


def _feature_names_from_rows(rows: Sequence[Mapping[str, float]]) -> list[str]:
    feature_names: set[str] = set()
    for row in rows:
        feature_names.update(row.keys())
    return sorted(feature_names)


def _feature_value(row: Mapping[str, float], key: str) -> float:
    try:
        return float(row.get(key, 0.0))
    except (TypeError, ValueError):
        return 0.0


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
