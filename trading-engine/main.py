from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    bot_mode: str
    live_trading_enabled: bool
    manual_approval_required: bool


app = FastAPI(
    title="Trading Engine",
    description="Paper-first FastAPI backend for the risk-gated trading bot.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        bot_mode="paper",
        live_trading_enabled=False,
        manual_approval_required=True,
    )
