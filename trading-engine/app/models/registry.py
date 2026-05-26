from functools import lru_cache

from app.models.train_model import PlaceholderProbabilityModel


DEFAULT_MODEL_VERSION = "placeholder-v1"


def get_active_model_version() -> str:
    return DEFAULT_MODEL_VERSION


@lru_cache
def get_active_model() -> PlaceholderProbabilityModel:
    return PlaceholderProbabilityModel(model_version=get_active_model_version())
