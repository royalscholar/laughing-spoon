from app.schemas.scanner import ScannerResult


def get_scanner_results() -> list[ScannerResult]:
    return [
        ScannerResult(
            symbol="AAPL",
            asset_type="stock",
            signal="mock_breakout",
            probability=0.72,
            rank=1,
            liquidity_score=0.94,
            volatility_score=0.48,
            risk_reward_ratio=2.2,
        ),
        ScannerResult(
            symbol="SPY",
            asset_type="etf",
            signal="mock_mean_reversion",
            probability=0.61,
            rank=2,
            liquidity_score=0.98,
            volatility_score=0.35,
            risk_reward_ratio=1.9,
        ),
    ]
