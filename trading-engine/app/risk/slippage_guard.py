from app.risk.trade_gate import RiskCheckResult


def check_slippage(
    estimated_slippage_percent: float,
    max_slippage_percent: float,
) -> RiskCheckResult:
    passed = estimated_slippage_percent <= max_slippage_percent
    return RiskCheckResult(
        check_name="max_slippage",
        passed=passed,
        rejection_reason=None if passed else "max_slippage_exceeded",
    )
