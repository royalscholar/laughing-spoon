from pydantic import BaseModel, Field


class ScannerResult(BaseModel):
    symbol: str
    asset_type: str
    signal: str
    probability: float = Field(ge=0.0, le=1.0)
    rank: int = Field(ge=1)
    liquidity_score: float = Field(ge=0.0, le=1.0)
    volatility_score: float = Field(ge=0.0, le=1.0)
    risk_reward_ratio: float = Field(gt=0.0)


class ScannerResultsResponse(BaseModel):
    results: list[ScannerResult]
