from pydantic import BaseModel, Field


class ScannerResult(BaseModel):
    symbol: str
    asset_type: str
    signal: str
    probability: float = Field(ge=0.0, le=1.0)
    rank: int = Field(ge=1)
    trend_score: float = Field(ge=0.0, le=1.0)
    volume_score: float = Field(ge=0.0, le=1.0)
    liquidity_score: float = Field(ge=0.0, le=1.0)
    volatility_score: float = Field(ge=0.0, le=1.0)
    fibonacci_score: float = Field(ge=0.0, le=1.0)
    expected_move_pct: float = Field(ge=0.0)
    trade_quality_score: float = Field(ge=0.0, le=1.0)
    status: str
    rejection_reason: str | None = None
    risk_reward_ratio: float = Field(gt=0.0)


class ScannerResultsResponse(BaseModel):
    results: list[ScannerResult]
