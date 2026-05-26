from app.risk.trade_gate import RiskCheckResult


def check_liquidity_score(
    liquidity_score: float,
    minimum_liquidity_score: float,
) -> RiskCheckResult:
    passed = liquidity_score >= minimum_liquidity_score
    return RiskCheckResult(
        check_name="minimum_liquidity_score",
        passed=passed,
        rejection_reason=None if passed else "minimum_liquidity_score_not_met",
    )
