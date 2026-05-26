# Multi-Asset AI Scanner and Risk-Gated Trading Bot

This repository is the source of truth for a Multi-Asset AI Scanner, ML Probability Engine, Risk-Gated Execution Bot, and Admin GUI.

## Architecture

- `trading-engine/`: Python FastAPI backend and trading engine.
- `base44-app/`: Base44 Admin GUI and control plane only.
- IBKR/TWS or IB Gateway: broker connection layer for future backend integration.
- PostgreSQL: persistent trade, configuration, and log storage.
- Redis: queue, cache, and background job support.
- AWS/VPS: production backend hosting target.

## Safety defaults

- Paper trading is the default execution mode.
- Live trading is disabled by default.
- Manual approval is required by default.
- Every trade must pass the backend risk gate before execution.
- Every rejected trade must include a rejection reason.
- Every order must be logged.

This project must not include code or claims that guarantee, promise, target, or force fixed daily returns.

## Local development

Copy `.env.example` to `.env` for local development and keep `.env` out of version control.

```bash
docker compose up --build
```

Or run the backend directly:

```bash
cd trading-engine
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Current implementation stage

This foundation contains project structure, documentation, safety defaults, and a minimal FastAPI health endpoint. It does not implement live broker execution.

## Disclaimer

This software is for engineering and research purposes. It is not financial advice and does not guarantee returns.
