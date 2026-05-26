from app.schemas.scanner import ScannerResult
from app.scanner.multi_asset_scanner import ScannerOpportunity, scan_universe


def get_scanner_results() -> list[ScannerResult]:
    return [
        _to_scanner_result(opportunity)
        for opportunity in scan_universe()
    ]


def _to_scanner_result(opportunity: ScannerOpportunity) -> ScannerResult:
    return ScannerResult(
        symbol=opportunity.symbol,
        asset_type=opportunity.asset_type,
        signal="mock_scanner_v1",
        probability=opportunity.trade_quality_score,
        rank=opportunity.rank or 1,
        trend_score=opportunity.trend_score,
        volume_score=opportunity.volume_score,
        liquidity_score=opportunity.volume_score,
        volatility_score=opportunity.volatility_score,
        fibonacci_score=opportunity.fibonacci_score,
        expected_move_pct=opportunity.expected_move_pct,
        trade_quality_score=opportunity.trade_quality_score,
        status=opportunity.status,
        rejection_reason=opportunity.rejection_reason,
        risk_reward_ratio=max(1.0, round(1.0 + opportunity.expected_move_pct, 4)),
    )
