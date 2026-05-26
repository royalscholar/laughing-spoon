from app.risk.trade_gate import RiskContext, evaluate_trade_risk
from app.schemas.risk import RiskCheck, RiskDecision, RiskSettingsRequest
from app.schemas.trades import TradeCandidate
from app.services import state


def update_risk_settings(settings: RiskSettingsRequest) -> RiskSettingsRequest:
    state.risk_settings = settings
    return state.risk_settings


def evaluate_trade_candidate(candidate: TradeCandidate) -> RiskDecision:
    decision = evaluate_trade_risk(_build_risk_context(candidate))
    return RiskDecision(
        risk_approved=decision.risk_approved,
        execution_allowed=decision.execution_allowed,
        rejection_reasons=decision.rejection_reasons,
        checks=[
            RiskCheck(
                name=check.check_name,
                status="pass" if check.passed else "fail",
                reason=check.rejection_reason,
            )
            for check in decision.checks
        ],
    )


def _build_risk_context(candidate: TradeCandidate) -> RiskContext:
    proposed_trade_risk = abs(candidate.proposed_entry - candidate.proposed_stop)
    return RiskContext(
        kill_switch_active=state.bot_state.kill_switch_active,
        bot_mode=state.bot_state.bot_mode,
        live_trading_enabled=state.bot_state.live_trading_enabled,
        paper_trading_enabled=state.bot_state.paper_trading_enabled,
        current_daily_pnl=0.0,
        daily_loss_limit=state.risk_settings.max_daily_loss,
        proposed_trade_risk=proposed_trade_risk,
        max_trade_risk=state.risk_settings.max_trade_risk,
        open_positions_count=1,
        max_open_positions=state.risk_settings.max_open_positions,
        day_trades_last_5_business_days=0,
        max_day_trades_last_5_business_days=(
            state.risk_settings.max_day_trades_last_5_business_days
        ),
        current_margin_usage=0.0,
        max_margin_usage=state.risk_settings.max_margin_usage,
        estimated_slippage_percent=0.1,
        max_slippage_percent=state.risk_settings.max_slippage_percent,
        liquidity_score=_mock_liquidity_score(candidate),
        minimum_liquidity_score=state.risk_settings.minimum_liquidity_score,
        trade_quality_score=candidate.probability,
        minimum_trade_quality_score=state.risk_settings.min_probability,
    )


def _mock_liquidity_score(candidate: TradeCandidate) -> float:
    liquidity_by_asset_type = {
        "stock": 0.9,
        "etf": 0.95,
        "option": 0.7,
        "otc": 0.4,
    }
    return liquidity_by_asset_type.get(candidate.asset_type, 0.6)
