from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskContext:
    kill_switch_active: bool
    bot_mode: str
    live_trading_enabled: bool
    paper_trading_enabled: bool
    current_daily_pnl: float
    daily_loss_limit: float
    proposed_trade_risk: float
    max_trade_risk: float
    open_positions_count: int
    max_open_positions: int
    day_trades_last_5_business_days: int
    max_day_trades_last_5_business_days: int
    current_margin_usage: float
    max_margin_usage: float
    estimated_slippage_percent: float
    max_slippage_percent: float
    liquidity_score: float
    minimum_liquidity_score: float
    trade_quality_score: float
    minimum_trade_quality_score: float


@dataclass(frozen=True)
class RiskCheckResult:
    check_name: str
    passed: bool
    rejection_reason: str | None = None


@dataclass(frozen=True)
class RiskGateDecision:
    risk_approved: bool
    execution_allowed: bool
    rejection_reasons: list[str]
    checks: list[RiskCheckResult]


from app.risk.drawdown_guard import check_daily_loss_limit
from app.risk.liquidity_guard import check_liquidity_score
from app.risk.margin_guard import check_margin_usage
from app.risk.pdt_guard import check_day_trade_limit
from app.risk.position_sizing import check_max_open_positions, check_max_trade_risk
from app.risk.slippage_guard import check_slippage


def evaluate_trade_risk(context: RiskContext) -> RiskGateDecision:
    checks = [
        _check_kill_switch(context.kill_switch_active),
        _check_bot_mode(context.bot_mode),
        _check_live_trading_enabled(
            context.bot_mode,
            context.live_trading_enabled,
        ),
        _check_paper_trading_enabled(
            context.bot_mode,
            context.paper_trading_enabled,
        ),
        check_daily_loss_limit(context.current_daily_pnl, context.daily_loss_limit),
        check_max_trade_risk(context.proposed_trade_risk, context.max_trade_risk),
        check_max_open_positions(
            context.open_positions_count,
            context.max_open_positions,
        ),
        check_day_trade_limit(
            context.day_trades_last_5_business_days,
            context.max_day_trades_last_5_business_days,
        ),
        check_margin_usage(context.current_margin_usage, context.max_margin_usage),
        check_slippage(
            context.estimated_slippage_percent,
            context.max_slippage_percent,
        ),
        check_liquidity_score(
            context.liquidity_score,
            context.minimum_liquidity_score,
        ),
        _check_trade_quality_score(
            context.trade_quality_score,
            context.minimum_trade_quality_score,
        ),
    ]
    rejection_reasons = [
        check.rejection_reason
        for check in checks
        if not check.passed and check.rejection_reason is not None
    ]
    risk_approved = len(rejection_reasons) == 0
    return RiskGateDecision(
        risk_approved=risk_approved,
        execution_allowed=risk_approved,
        rejection_reasons=rejection_reasons,
        checks=checks,
    )


def _check_kill_switch(kill_switch_active: bool) -> RiskCheckResult:
    passed = not kill_switch_active
    return RiskCheckResult(
        check_name="kill_switch",
        passed=passed,
        rejection_reason=None if passed else "kill_switch_active",
    )


def _check_bot_mode(bot_mode: str) -> RiskCheckResult:
    normalized_mode = bot_mode.lower().strip()
    if normalized_mode == "disabled":
        return RiskCheckResult(
            check_name="bot_mode",
            passed=False,
            rejection_reason="bot_mode_disabled",
        )
    passed = normalized_mode in {"paper", "live"}
    return RiskCheckResult(
        check_name="bot_mode",
        passed=passed,
        rejection_reason=None if passed else "bot_mode_invalid",
    )


def _check_live_trading_enabled(
    bot_mode: str,
    live_trading_enabled: bool,
) -> RiskCheckResult:
    normalized_mode = bot_mode.lower().strip()
    if normalized_mode != "live":
        passed = not live_trading_enabled
        return RiskCheckResult(
            check_name="live_trading_enabled",
            passed=passed,
            rejection_reason=None if passed else "live_trading_enabled_in_non_live_mode",
        )

    if not live_trading_enabled:
        return RiskCheckResult(
            check_name="live_trading_enabled",
            passed=False,
            rejection_reason="live_trading_not_enabled",
        )

    return RiskCheckResult(
        check_name="live_trading_enabled",
        passed=False,
        rejection_reason="live_trading_not_supported",
    )


def _check_paper_trading_enabled(
    bot_mode: str,
    paper_trading_enabled: bool,
) -> RiskCheckResult:
    normalized_mode = bot_mode.lower().strip()
    if normalized_mode != "paper":
        return RiskCheckResult(
            check_name="paper_trading_enabled",
            passed=True,
        )

    return RiskCheckResult(
        check_name="paper_trading_enabled",
        passed=paper_trading_enabled,
        rejection_reason=None if paper_trading_enabled else "paper_trading_disabled",
    )


def _check_trade_quality_score(
    trade_quality_score: float,
    minimum_trade_quality_score: float,
) -> RiskCheckResult:
    passed = trade_quality_score >= minimum_trade_quality_score
    return RiskCheckResult(
        check_name="minimum_trade_quality_score",
        passed=passed,
        rejection_reason=None if passed else "minimum_trade_quality_score_not_met",
    )
