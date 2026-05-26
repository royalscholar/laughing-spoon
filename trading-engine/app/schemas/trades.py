from pydantic import BaseModel, Field

from app.schemas.risk import RiskDecision


class TradeCandidate(BaseModel):
    candidate_id: str
    symbol: str
    asset_type: str
    side: str
    strategy: str
    probability: float = Field(ge=0.0, le=1.0)
    proposed_entry: float = Field(gt=0.0)
    proposed_stop: float = Field(gt=0.0)
    proposed_target: float = Field(gt=0.0)
    status: str


class TradeCandidatesResponse(BaseModel):
    candidates: list[TradeCandidate]


class ApproveTradeRequest(BaseModel):
    candidate_id: str
    approved_by: str
    notes: str | None = None


class RejectTradeRequest(BaseModel):
    candidate_id: str
    rejected_by: str
    rejection_reason: str = Field(min_length=1)
    notes: str | None = None


class TradeDecisionResponse(BaseModel):
    candidate_id: str
    status: str
    message: str
    risk_decision: RiskDecision | None = None
    rejection_reason: str | None = None
