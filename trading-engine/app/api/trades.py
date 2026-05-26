from fastapi import APIRouter

from app.schemas.trades import (
    ApproveTradeRequest,
    RejectTradeRequest,
    TradeCandidatesResponse,
    TradeDecisionResponse,
)
from app.services import trade_service


router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/candidates", response_model=TradeCandidatesResponse)
def get_trade_candidates() -> TradeCandidatesResponse:
    return TradeCandidatesResponse(candidates=trade_service.get_trade_candidates())


@router.post("/approve", response_model=TradeDecisionResponse)
def approve_trade(request: ApproveTradeRequest) -> TradeDecisionResponse:
    return trade_service.approve_trade(request)


@router.post("/reject", response_model=TradeDecisionResponse)
def reject_trade(request: RejectTradeRequest) -> TradeDecisionResponse:
    return trade_service.reject_trade(request)
