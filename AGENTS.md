# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This is a Python algorithmic trading bot platform for backtesting and live trading across multiple asset classes (stocks, forex, crypto, futures). It uses **Backtrader** for backtesting and connects to **Interactive Brokers (IBKR)** and **Alpaca Markets** for live trading.

### Running scripts

- **Backtesting (no external services needed):** `python3 06_backtest.py` and `python3 07_backtest_multi_assets.py` use `yfinance` for data and can run without any API keys or broker connections.
- **Live trading scripts (01–05, 08–10, ib_ma_*):** Require a running IBKR TWS/Gateway on `127.0.0.1:7497` (paper trading). These cannot run in Cloud Agent VMs.
- **Alpaca scripts (`alpaca_connect.py`, `alpaca_data.py`, `bt_run.py`, etc.):** Require Alpaca API keys. `alpaca_connect.py` imports from `alpaca_keys.py` (gitignored). `alpaca_data.py` has hardcoded keys that may be expired.

### Linting

Run flake8: `flake8 --max-line-length=120 --exclude=.git,__pycache__,.venv,venv,ibenv .`

The codebase uses `from ib_insync import *` extensively, which generates F403/F405 warnings. These are expected and not errors.

### Known import caveats

- `bt_run.py` imports `from Strategies.MaCrossStrategy import MaCrossStrategy` (capital-S `Strategies`), but the actual directory is `strategies` (lowercase). This works on case-insensitive filesystems (macOS/Windows) but **fails on Linux**. Avoid running `bt_run.py` directly without fixing the import path.
- `strategies/init__.py` (double underscore, not `__init__.py`) imports from `.macross`, `.rsi`, `.breakout` — but the actual files are `macross_bt.py`, `RsiStrategy.py`, `BreakoutStrategy.py`. This file is not the real package init; the actual `__init__.py` is intentionally empty.

### Dependencies

No `requirements.txt` exists in the repo. Install manually:
```
pip install backtrader yfinance pandas numpy ib_insync alpaca-py openpyxl flake8
```

### Secrets / API keys

- **Alpaca:** Create `alpaca_keys.py` in the repo root (gitignored) exporting `API_KEY`, `API_SECRET`, `BASE_URL`.
- **IBKR:** Requires TWS/Gateway running locally — not feasible in Cloud Agent VMs.
