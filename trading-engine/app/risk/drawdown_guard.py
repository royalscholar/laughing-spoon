from app.risk.trade_gate import RiskCheckResult


def check_daily_loss_limit(
    current_daily_pnl: float,
    daily_loss_limit: float,
) -> RiskCheckResult:
    loss_amount = abs(min(current_daily_pnl, 0.0))
    passed = loss_amount <= daily_loss_limit
    return RiskCheckResult(
        check_name="daily_loss_limit",
        passed=passed,
        rejection_reason=None if passed else "daily_loss_limit_exceeded",
    )
