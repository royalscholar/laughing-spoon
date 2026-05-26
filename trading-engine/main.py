from fastapi import FastAPI

from app.api import bot, health, logs, positions, risk, scanner, trades, webhooks
from app.schemas.health import HealthResponse
from app.services import health_service


app = FastAPI(
    title="Trading Engine",
    description="Paper-first FastAPI backend for the risk-gated trading bot.",
    version="0.1.0",
)

app.include_router(health.router, prefix="/api")
app.include_router(scanner.router, prefix="/api")
app.include_router(trades.router, prefix="/api")
app.include_router(bot.router, prefix="/api")
app.include_router(risk.router, prefix="/api")
app.include_router(positions.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return health_service.get_health()
