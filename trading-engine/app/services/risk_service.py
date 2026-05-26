from app.schemas.risk import RiskCheck, RiskDecision, RiskSettingsRequest
from app.schemas.trades import TradeCandidate
from app.services import state


def update_risk_settings(settings: RiskSettingsRequest) -> RiskSettingsRequest:
    state.risk_settings = settings
    return state.risk_settings


def evaluate_trade_candidate(candidate: TradeCandidate) -> RiskDecision:
    checks: list[RiskCheck] = []
    rejection_reasons: list[str] = []

    def add_check(name: str, passed: bool, reason: str | None = None) -> None:
        checks.append(
            RiskCheck(
                name=name,
                status="pass" if passed else "fail",
                reason=reason,
            )
        )
        if not passed and reason:
            rejection_reasons.append(reason)

    add_check(
        "kill_switch",
        not state.bot_state.kill_switch_active,
        "kill_switch_active" if state.bot_state.kill_switch_active else None,
    )
    add_check(
        "paper_trading_enabled",
        state.bot_state.paper_trading_enabled,
        "paper_trading_disabled" if not state.bot_state.paper_trading_enabled else None,
    )
    add_check(
        "live_trading_disabled",
        not state.bot_state.live_trading_enabled,
        "live_trading_not_allowed_in_skeleton" if state.bot_state.live_trading_enabled else None,
    )
    add_check(
        "minimum_probability",
        candidate.probability >= state.risk_settings.min_probability,
        "probability_below_threshold"
        if candidate.probability < state.risk_settings.min_probability
        else None,
    )
    add_check(
        "manual_approval",
        True,
        "manual_approval_required" if state.bot_state.manual_approval_required else None,
    )

    risk_approved = not rejection_reasons
    return RiskDecision(
        risk_approved=risk_approved,
        execution_allowed=risk_approved and not state.bot_state.kill_switch_active,
        rejection_reasons=rejection_reasons,
        checks=checks,
    )
