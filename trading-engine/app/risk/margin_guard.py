from app.risk.trade_gate import RiskCheckResult


def check_margin_usage(
    current_margin_usage: float,
    max_margin_usage: float,
) -> RiskCheckResult:
    passed = current_margin_usage <= max_margin_usage
    return RiskCheckResult(
        check_name="max_margin_usage",
        passed=passed,
        rejection_reason=None if passed else "max_margin_usage_exceeded",
    )
