from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class UniverseSymbol:
    symbol: str
    asset_type: str


def load_symbols_from_file(path: Path) -> list[str]:
    if not path.exists():
        return []

    symbols: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        symbol = line.strip().upper()
        if not symbol or symbol.startswith("#") or symbol in seen:
            continue
        seen.add(symbol)
        symbols.append(symbol)
    return symbols


def load_default_universe(repo_root: Path | None = None) -> list[UniverseSymbol]:
    root = repo_root or Path(__file__).resolve().parents[3]
    data_dir = root / "data"

    universe: list[UniverseSymbol] = []
    seen: set[tuple[str, str]] = set()
    for asset_type, filename in (
        ("stock", "universe_stocks.txt"),
        ("etf", "universe_etfs.txt"),
    ):
        for symbol in load_symbols_from_file(data_dir / filename):
            key = (symbol, asset_type)
            if key in seen:
                continue
            seen.add(key)
            universe.append(UniverseSymbol(symbol=symbol, asset_type=asset_type))

    return universe
