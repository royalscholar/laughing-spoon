# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python-based algorithmic trading bot platform for backtesting and live trading across multiple asset classes (US stocks, forex, crypto, futures). It uses two broker APIs:

- **Interactive Brokers (IBKR)** — via `ib_insync`, connecting to TWS on `127.0.0.1:7497` (paper) or `:7496` (live)
- **Alpaca Markets** — via `alpaca-py`, requires API keys in a gitignored `alpaca_keys.py`

### Dependencies

All Python dependencies are installed globally via pip. There is no `requirements.txt` in the repo. The required packages are:

```
backtrader yfinance pandas ib_insync alpaca-py openpyxl matplotlib pyflakes
```

### Running scripts

**Backtesting (no external services needed):**
- `python3 06_backtest.py` — Single-asset RSI backtest using yfinance data (EURUSD)
- `python3 07_backtest_multi_assets.py` — Multi-asset SMA crossover backtest (EURUSD, AAPL, BTC-USD)

These are the only scripts that can run without external broker connections.

**IBKR scripts** (`01_connect.py` through `10_live_multi_asset_bot.py`, `ib_ma_*.py`): Require Interactive Brokers TWS or IB Gateway running locally on port 7497. Cannot run in Cloud Agent environments without TWS.

**Alpaca scripts** (`alpaca_connect.py`, `alpaca_data.py`, `bt_run.py`, etc.): Require a `alpaca_keys.py` file with `API_KEY`, `API_SECRET`, and `BASE_URL` variables. This file is gitignored.

### Linting

No linter is configured in the project. Use `python3 -m pyflakes <file>` for basic checks. Existing code has minor unused-import warnings which are expected.

### Known issues

- `strategies/BTCMA.py` is a code snippet/stub, not a working module (it references `Strategies.BTCMA` which doesn't exist).
- `strategies/init__.py` (note the double underscore typo) imports from `macross`, `rsi`, and `breakout` which don't match the actual filenames (`macross_bt.py`, `RsiStrategy.py`, `BreakoutStrategy.py`).
- `bt_run.py` imports from `Strategies.MaCrossStrategy` (capitalized `S`), but the directory is `strategies` (lowercase). This is case-sensitive on Linux.
- Several `ib_ma_*.py` scripts import `from strategies.macross import Strategy`, but no `strategies/macross.py` file exists.
