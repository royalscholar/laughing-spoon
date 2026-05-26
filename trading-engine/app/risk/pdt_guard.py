from app.risk.trade_gate import RiskCheckResult


def check_day_trade_limit(
    day_trades_last_5_business_days: int,
    max_day_trades_last_5_business_days: int,
) -> RiskCheckResult:
    passed = day_trades_last_5_business_days < max_day_trades_last_5_business_days
    return RiskCheckResult(
        check_name="pdt_day_trade_limit",
        passed=passed,
        rejection_reason=None if passed else "pdt_day_trade_limit_exceeded",
    )
