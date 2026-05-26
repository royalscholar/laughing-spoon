from pathlib import Path

from fastapi.testclient import TestClient

from app.features.fibonacci_features import compute_fibonacci_score
from app.features.price_features import compute_trend_score
from app.features.volatility_features import compute_expected_move_pct, compute_volatility_score
from app.features.volume_features import compute_volume_score
from app.scanner.multi_asset_scanner import (
    ScannerOpportunity,
    generate_mock_ohlcv,
    scan_symbols,
)
from app.scanner.opportunity_ranker import rank_opportunities
from app.scanner.universe_loader import (
    UniverseSymbol,
    load_default_universe,
    load_symbols_from_file,
)
from main import app


def test_universe_loader_ignores_comments_blanks_duplicates_and_uppercases(
    tmp_path: Path,
) -> None:
    universe_file = tmp_path / "symbols.txt"
    universe_file.write_text(
        "\n# comment\naapl\nMSFT\nmsft\n  spy  \n",
        encoding="utf-8",
    )

    assert load_symbols_from_file(universe_file) == ["AAPL", "MSFT", "SPY"]


def test_default_universe_loads_stocks_and_etfs_from_data(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "universe_stocks.txt").write_text("AAPL\nMSFT\n", encoding="utf-8")
    (data_dir / "universe_etfs.txt").write_text("SPY\nQQQ\n", encoding="utf-8")

    universe = load_default_universe(tmp_path)

    assert universe == [
        UniverseSymbol(symbol="AAPL", asset_type="stock"),
        UniverseSymbol(symbol="MSFT", asset_type="stock"),
        UniverseSymbol(symbol="SPY", asset_type="etf"),
        UniverseSymbol(symbol="QQQ", asset_type="etf"),
    ]


def test_mock_ohlcv_generation_is_deterministic() -> None:
    first = generate_mock_ohlcv("AAPL", "stock")
    second = generate_mock_ohlcv("AAPL", "stock")

    assert first == second
    assert len(first) == 30


def test_feature_scores_are_normalized() -> None:
    bars = generate_mock_ohlcv("AAPL", "stock")

    assert 0.0 <= compute_trend_score(bars) <= 1.0
    assert 0.0 <= compute_volume_score(bars) <= 1.0
    assert 0.0 <= compute_volatility_score(bars) <= 1.0
    assert 0.0 <= compute_fibonacci_score(bars) <= 1.0
    assert compute_expected_move_pct(bars) >= 0.0


def test_scanner_returns_ranked_opportunities_with_statuses() -> None:
    opportunities = scan_symbols(
        [
            UniverseSymbol(symbol="AAPL", asset_type="stock"),
            UniverseSymbol(symbol="SPY", asset_type="etf"),
        ]
    )

    assert len(opportunities) == 2
    assert [opportunity.rank for opportunity in opportunities] == [1, 2]
    for opportunity in opportunities:
        assert 0.0 <= opportunity.trade_quality_score <= 1.0
        assert opportunity.expected_move_pct >= 0.0
        assert opportunity.status in {"reject", "watchlist", "manual_approval"}


def test_rejected_opportunities_include_rejection_reason() -> None:
    opportunities = scan_symbols([UniverseSymbol(symbol="ZZZ", asset_type="stock")])

    for opportunity in opportunities:
        if opportunity.status == "reject":
            assert opportunity.rejection_reason == "trade_quality_below_threshold"


def test_ranker_sorts_deterministically() -> None:
    opportunities = [
        _opportunity("BBB", "watchlist", 0.55),
        _opportunity("AAA", "manual_approval", 0.70),
        _opportunity("CCC", "reject", 0.20),
        _opportunity("DDD", "manual_approval", 0.90),
    ]

    ranked = rank_opportunities(opportunities)

    assert [opportunity.symbol for opportunity in ranked] == ["DDD", "AAA", "BBB", "CCC"]
    assert [opportunity.rank for opportunity in ranked] == [1, 2, 3, 4]


def test_scanner_results_api_returns_scanner_v1_fields() -> None:
    client = TestClient(app)

    response = client.get("/api/scanner/results")

    assert response.status_code == 200
    results = response.json()["results"]
    assert results
    first_result = results[0]
    assert first_result["signal"] == "mock_scanner_v1"
    assert "trend_score" in first_result
    assert "volume_score" in first_result
    assert "fibonacci_score" in first_result
    assert "expected_move_pct" in first_result
    assert "trade_quality_score" in first_result
    assert first_result["status"] in {"reject", "watchlist", "manual_approval"}


def _opportunity(
    symbol: str,
    status: str,
    trade_quality_score: float,
) -> ScannerOpportunity:
    return ScannerOpportunity(
        symbol=symbol,
        asset_type="stock",
        trend_score=trade_quality_score,
        volume_score=trade_quality_score,
        volatility_score=trade_quality_score,
        fibonacci_score=trade_quality_score,
        expected_move_pct=1.0,
        trade_quality_score=trade_quality_score,
        status=status,
        rejection_reason="trade_quality_below_threshold" if status == "reject" else None,
    )
