from dataclasses import replace

from app.risk.trade_gate import RiskContext, evaluate_trade_risk


def base_context() -> RiskContext:
    return RiskContext(
        kill_switch_active=False,
        bot_mode="paper",
        live_trading_enabled=False,
        paper_trading_enabled=True,
        current_daily_pnl=0.0,
        daily_loss_limit=500.0,
        proposed_trade_risk=100.0,
        max_trade_risk=250.0,
        open_positions_count=1,
        max_open_positions=5,
        day_trades_last_5_business_days=0,
        max_day_trades_last_5_business_days=3,
        current_margin_usage=0.2,
        max_margin_usage=0.5,
        estimated_slippage_percent=0.1,
        max_slippage_percent=0.5,
        liquidity_score=0.9,
        minimum_liquidity_score=0.6,
        trade_quality_score=0.75,
        minimum_trade_quality_score=0.65,
    )


def rejection_reasons_for(context: RiskContext) -> list[str]:
    return evaluate_trade_risk(context).rejection_reasons


def test_risk_gate_approves_when_all_checks_pass() -> None:
    decision = evaluate_trade_risk(base_context())

    assert decision.risk_approved is True
    assert decision.execution_allowed is True
    assert decision.rejection_reasons == []
    assert all(check.passed for check in decision.checks)


def test_risk_gate_rejects_kill_switch() -> None:
    reasons = rejection_reasons_for(replace(base_context(), kill_switch_active=True))

    assert "kill_switch_active" in reasons


def test_risk_gate_rejects_disabled_bot_mode() -> None:
    reasons = rejection_reasons_for(replace(base_context(), bot_mode="disabled"))

    assert "bot_mode_disabled" in reasons


def test_risk_gate_rejects_live_mode_when_live_trading_not_enabled() -> None:
    reasons = rejection_reasons_for(replace(base_context(), bot_mode="live"))

    assert "live_trading_not_enabled" in reasons


def test_risk_gate_rejects_live_mode_even_when_enabled_until_supported() -> None:
    reasons = rejection_reasons_for(
        replace(base_context(), bot_mode="live", live_trading_enabled=True)
    )

    assert "live_trading_not_supported" in reasons


def test_risk_gate_rejects_unexpected_live_enablement_in_paper_mode() -> None:
    reasons = rejection_reasons_for(replace(base_context(), live_trading_enabled=True))

    assert "live_trading_enabled_in_non_live_mode" in reasons


def test_risk_gate_rejects_paper_trading_disabled() -> None:
    reasons = rejection_reasons_for(replace(base_context(), paper_trading_enabled=False))

    assert "paper_trading_disabled" in reasons


def test_risk_gate_rejects_daily_loss_limit_exceeded() -> None:
    reasons = rejection_reasons_for(replace(base_context(), current_daily_pnl=-501.0))

    assert "daily_loss_limit_exceeded" in reasons


def test_risk_gate_rejects_max_trade_risk_exceeded() -> None:
    reasons = rejection_reasons_for(replace(base_context(), proposed_trade_risk=251.0))

    assert "max_trade_risk_exceeded" in reasons


def test_risk_gate_rejects_max_open_positions_exceeded() -> None:
    reasons = rejection_reasons_for(replace(base_context(), open_positions_count=5))

    assert "max_open_positions_exceeded" in reasons


def test_risk_gate_rejects_pdt_day_trade_limit_exceeded() -> None:
    reasons = rejection_reasons_for(
        replace(base_context(), day_trades_last_5_business_days=3)
    )

    assert "pdt_day_trade_limit_exceeded" in reasons


def test_risk_gate_rejects_max_margin_usage_exceeded() -> None:
    reasons = rejection_reasons_for(replace(base_context(), current_margin_usage=0.51))

    assert "max_margin_usage_exceeded" in reasons


def test_risk_gate_rejects_max_slippage_exceeded() -> None:
    reasons = rejection_reasons_for(
        replace(base_context(), estimated_slippage_percent=0.51)
    )

    assert "max_slippage_exceeded" in reasons


def test_risk_gate_rejects_minimum_liquidity_score_not_met() -> None:
    reasons = rejection_reasons_for(replace(base_context(), liquidity_score=0.59))

    assert "minimum_liquidity_score_not_met" in reasons


def test_risk_gate_rejects_minimum_trade_quality_score_not_met() -> None:
    reasons = rejection_reasons_for(replace(base_context(), trade_quality_score=0.64))

    assert "minimum_trade_quality_score_not_met" in reasons
