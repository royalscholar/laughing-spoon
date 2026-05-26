from app.risk.trade_gate import RiskCheckResult


def check_max_trade_risk(
    proposed_trade_risk: float,
    max_trade_risk: float,
) -> RiskCheckResult:
    passed = proposed_trade_risk <= max_trade_risk
    return RiskCheckResult(
        check_name="max_trade_risk",
        passed=passed,
        rejection_reason=None if passed else "max_trade_risk_exceeded",
    )


def check_max_open_positions(
    open_positions_count: int,
    max_open_positions: int,
) -> RiskCheckResult:
    passed = open_positions_count < max_open_positions
    return RiskCheckResult(
        check_name="max_open_positions",
        passed=passed,
        rejection_reason=None if passed else "max_open_positions_exceeded",
    )
