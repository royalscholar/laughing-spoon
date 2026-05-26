from app.schemas.trades import (
    ApproveTradeRequest,
    RejectTradeRequest,
    TradeCandidate,
    TradeDecisionResponse,
)
from app.services import log_service, risk_service, state


def get_trade_candidates() -> list[TradeCandidate]:
    return list(state.mock_trade_candidates)


def approve_trade(request: ApproveTradeRequest) -> TradeDecisionResponse:
    candidate = _find_candidate(request.candidate_id)

    if candidate is None:
        log_service.add_log(
            "trade_approval_rejected",
            "Trade candidate not found.",
            {"candidate_id": request.candidate_id},
        )
        return TradeDecisionResponse(
            candidate_id=request.candidate_id,
            status="rejected",
            message="Trade candidate not found.",
            rejection_reason="candidate_not_found",
        )

    risk_decision = risk_service.evaluate_trade_candidate(candidate)
    if risk_decision.risk_approved and risk_decision.execution_allowed:
        candidate.status = "approved_for_paper"
        log_service.add_log(
            "trade_approved",
            "Trade approved for paper execution only.",
            {
                "candidate_id": candidate.candidate_id,
                "approved_by": request.approved_by,
                "environment": "paper",
            },
        )
        return TradeDecisionResponse(
            candidate_id=candidate.candidate_id,
            status=candidate.status,
            message="Trade approved for paper execution only. No live broker order was placed.",
            risk_decision=risk_decision,
        )

    candidate.status = "rejected_by_risk_gate"
    log_service.add_log(
        "trade_rejected_by_risk_gate",
        "Trade approval blocked by placeholder risk gate.",
        {
            "candidate_id": candidate.candidate_id,
            "approved_by": request.approved_by,
            "rejection_reasons": risk_decision.rejection_reasons,
        },
    )
    return TradeDecisionResponse(
        candidate_id=candidate.candidate_id,
        status=candidate.status,
        message="Trade blocked by placeholder risk gate. No order was placed.",
        risk_decision=risk_decision,
        rejection_reason=", ".join(risk_decision.rejection_reasons),
    )


def reject_trade(request: RejectTradeRequest) -> TradeDecisionResponse:
    candidate = _find_candidate(request.candidate_id)
    if candidate is not None:
        candidate.status = "rejected_by_user"

    log_service.add_log(
        "trade_rejected",
        "Trade candidate rejected by user.",
        {
            "candidate_id": request.candidate_id,
            "rejected_by": request.rejected_by,
            "rejection_reason": request.rejection_reason,
        },
    )
    return TradeDecisionResponse(
        candidate_id=request.candidate_id,
        status="rejected_by_user",
        message="Trade rejected with recorded reason.",
        rejection_reason=request.rejection_reason,
    )


def _find_candidate(candidate_id: str) -> TradeCandidate | None:
    return next(
        (
            candidate
            for candidate in state.mock_trade_candidates
            if candidate.candidate_id == candidate_id
        ),
        None,
    )
