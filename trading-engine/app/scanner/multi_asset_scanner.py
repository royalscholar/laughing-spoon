from dataclasses import dataclass
from pathlib import Path

from app.features.fibonacci_features import compute_fibonacci_score
from app.features.price_features import compute_trend_score
from app.features.volatility_features import (
    compute_expected_move_pct,
    compute_volatility_score,
)
from app.features.volume_features import compute_volume_score
from app.scanner.universe_loader import UniverseSymbol, load_default_universe


@dataclass(frozen=True)
class OhlcvBar:
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class ScannerOpportunity:
    symbol: str
    asset_type: str
    trend_score: float
    volume_score: float
    volatility_score: float
    fibonacci_score: float
    expected_move_pct: float
    trade_quality_score: float
    status: str
    rejection_reason: str | None
    rank: int | None = None


def scan_universe(repo_root: Path | None = None) -> list[ScannerOpportunity]:
    return scan_symbols(load_default_universe(repo_root))


def scan_symbols(universe: list[UniverseSymbol]) -> list[ScannerOpportunity]:
    opportunities = [
        scan_symbol(universe_symbol)
        for universe_symbol in universe
    ]

    from app.scanner.opportunity_ranker import rank_opportunities

    return rank_opportunities(opportunities)


def scan_symbol(universe_symbol: UniverseSymbol) -> ScannerOpportunity:
    bars = generate_mock_ohlcv(universe_symbol.symbol, universe_symbol.asset_type)
    trend_score = compute_trend_score(bars)
    volume_score = compute_volume_score(bars)
    volatility_score = compute_volatility_score(bars)
    fibonacci_score = compute_fibonacci_score(bars)
    expected_move_pct = compute_expected_move_pct(bars)
    expected_move_score = _clamp(expected_move_pct / 4.0)
    trade_quality_score = _round_score(
        (trend_score * 0.30)
        + (volume_score * 0.20)
        + (volatility_score * 0.20)
        + (fibonacci_score * 0.20)
        + (expected_move_score * 0.10)
    )
    status = _status_for_quality(trade_quality_score)
    return ScannerOpportunity(
        symbol=universe_symbol.symbol,
        asset_type=universe_symbol.asset_type,
        trend_score=_round_score(trend_score),
        volume_score=_round_score(volume_score),
        volatility_score=_round_score(volatility_score),
        fibonacci_score=_round_score(fibonacci_score),
        expected_move_pct=round(expected_move_pct, 4),
        trade_quality_score=trade_quality_score,
        status=status,
        rejection_reason="trade_quality_below_threshold"
        if status == "reject"
        else None,
    )


def generate_mock_ohlcv(
    symbol: str,
    asset_type: str,
    bars_count: int = 30,
) -> list[OhlcvBar]:
    symbol_seed = sum((index + 1) * ord(char) for index, char in enumerate(symbol))
    base_price = 50.0 + (symbol_seed % 250)
    slope = ((symbol_seed % 13) - 4) / 100.0
    volatility = 0.006 + ((symbol_seed % 9) / 1000.0)
    base_volume = 500_000 + ((symbol_seed % 20) * 75_000)
    asset_volume_multiplier = 1.4 if asset_type == "etf" else 1.0

    bars: list[OhlcvBar] = []
    previous_close = base_price
    for index in range(bars_count):
        wave = ((index % 5) - 2) * volatility
        open_price = previous_close
        close_price = max(1.0, open_price * (1.0 + slope + wave))
        high_price = max(open_price, close_price) * (1.0 + volatility)
        low_price = min(open_price, close_price) * (1.0 - volatility)
        volume = int(base_volume * asset_volume_multiplier * (1.0 + (index % 7) * 0.03))
        bars.append(
            OhlcvBar(
                open=round(open_price, 4),
                high=round(high_price, 4),
                low=round(low_price, 4),
                close=round(close_price, 4),
                volume=volume,
            )
        )
        previous_close = close_price

    return bars


def _status_for_quality(trade_quality_score: float) -> str:
    if trade_quality_score < 0.45:
        return "reject"
    if trade_quality_score < 0.70:
        return "watchlist"
    return "manual_approval"


def _round_score(score: float) -> float:
    return round(_clamp(score), 4)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
