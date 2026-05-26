from pydantic import BaseModel, Field


class RiskCheck(BaseModel):
    name: str
    status: str
    reason: str | None = None


class RiskDecision(BaseModel):
    risk_approved: bool
    execution_allowed: bool
    rejection_reasons: list[str]
    checks: list[RiskCheck]


class RiskSettingsRequest(BaseModel):
    max_daily_loss: float = Field(default=500.0, gt=0.0)
    max_position_size: float = Field(default=1000.0, gt=0.0)
    max_symbol_exposure: float = Field(default=2500.0, gt=0.0)
    min_probability: float = Field(default=0.65, ge=0.0, le=1.0)
    max_spread_percent: float = Field(default=1.0, gt=0.0)
    require_manual_approval: bool = True


class RiskSettingsResponse(BaseModel):
    settings: RiskSettingsRequest
