from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_mode: str = "paper"
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = True
    manual_approval_required: bool = True
    kill_switch_active: bool = False
    ib_host: str = "127.0.0.1"
    ib_port: int = 7497
    ib_client_id: int = 1


@lru_cache
def get_settings() -> Settings:
    return Settings()
