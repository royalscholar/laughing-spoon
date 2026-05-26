from pathlib import Path

import pytest

from app.models.labels import LabelConfig, build_placeholder_label
from app.models.predict import PredictionResult, predict_opportunity
from app.models.registry import DEFAULT_MODEL_VERSION, get_active_model, get_active_model_version
from app.models.train_model import PlaceholderProbabilityModel, train_placeholder_model


def sample_features() -> dict[str, float]:
    return {
        "trend_score": 0.7,
        "volume_score": 0.6,
        "volatility_score": 0.5,
        "fibonacci_score": 0.8,
        "trade_quality_score": 0.75,
        "expected_move_pct": 2.4,
    }


def test_predict_opportunity_returns_required_fields() -> None:
    prediction = predict_opportunity(sample_features())

    assert isinstance(prediction, PredictionResult)
    assert 0.0 <= prediction.ml_probability <= 1.0
    assert prediction.expected_move_pct == 2.4
    assert prediction.expected_drawdown_pct >= 0.0
    assert 0.0 <= prediction.confidence_score <= 1.0
    assert prediction.model_version == DEFAULT_MODEL_VERSION


def test_predict_opportunity_clamps_probability_inputs() -> None:
    prediction = predict_opportunity(
        {
            "trend_score": 10.0,
            "volume_score": -5.0,
            "volatility_score": 2.0,
            "fibonacci_score": 1.5,
            "trade_quality_score": 99.0,
            "expected_move_pct": 3.0,
        }
    )

    assert 0.0 <= prediction.ml_probability <= 1.0
    assert 0.0 <= prediction.confidence_score <= 1.0


def test_predict_opportunity_is_deterministic_for_same_input() -> None:
    first = predict_opportunity(sample_features())
    second = predict_opportunity(sample_features())

    assert first == second


def test_predict_opportunity_handles_missing_features_safely() -> None:
    prediction = predict_opportunity({"trend_score": 0.6})

    assert 0.0 <= prediction.ml_probability <= 1.0
    assert prediction.expected_move_pct == 0.0
    assert prediction.confidence_score == pytest.approx(0.1667)
    assert prediction.model_version == DEFAULT_MODEL_VERSION


def test_registry_returns_placeholder_model_and_version() -> None:
    model = get_active_model()

    assert get_active_model_version() == DEFAULT_MODEL_VERSION
    assert isinstance(model, PlaceholderProbabilityModel)
    assert hasattr(model, "fit")
    assert hasattr(model, "predict_proba")


def test_placeholder_model_fit_and_predict_proba_are_sklearn_compatible() -> None:
    model = PlaceholderProbabilityModel()
    result = model.fit([sample_features()], [1])
    probabilities = model.predict_proba([sample_features()])

    assert result is model
    assert model.trained is True
    assert probabilities == [[0.3125, 0.6875]]


def test_placeholder_model_rejects_mismatched_training_lengths() -> None:
    model = PlaceholderProbabilityModel()

    with pytest.raises(ValueError):
        model.fit([sample_features()], [])


def test_train_placeholder_model_returns_metadata_without_artifacts(
    tmp_path: Path,
) -> None:
    before_files = set(tmp_path.iterdir())

    result = train_placeholder_model([sample_features()], [1])

    assert result.model_version == DEFAULT_MODEL_VERSION
    assert result.trained is True
    assert result.sample_count == 1
    assert "trend_score" in result.feature_names
    assert result.metrics == {"placeholder_positive_rate": 1.0}
    assert set(tmp_path.iterdir()) == before_files


def test_label_builder_returns_deterministic_binary_labels() -> None:
    favorable = build_placeholder_label(
        sample_features(),
        LabelConfig(profit_target_pct=2.0, max_drawdown_pct=1.0, holding_period_bars=10),
    )
    weak = build_placeholder_label(
        {"trade_quality_score": 0.2, "expected_move_pct": 0.5, "volatility_score": 0.3}
    )

    assert favorable == 1
    assert weak == 0
    assert build_placeholder_label(sample_features()) == favorable
