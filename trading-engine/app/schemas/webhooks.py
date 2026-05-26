from typing import Any

from pydantic import BaseModel


class TradingViewWebhookRequest(BaseModel):
    symbol: str
    signal: str
    price: float | None = None
    timeframe: str | None = None
    strategy: str | None = None
    payload: dict[str, Any] = {}


class WebhookResponse(BaseModel):
    accepted: bool
    message: str
    candidate_created: bool
