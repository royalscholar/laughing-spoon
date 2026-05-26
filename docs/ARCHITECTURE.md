# Architecture

This project is a Multi-Asset AI Scanner, ML Probability Engine, Risk-Gated Execution Bot, and Admin GUI.

## Component boundaries

### Cursor/GitHub

Cursor and GitHub are used for code development, source control, review, and deployment preparation.

### trading-engine/

The Python FastAPI backend is the trading engine. It owns:

- market scanning,
- feature generation,
- ML probability scoring,
- Greeks computation,
- Fibonacci risk logic,
- PDT and margin guards,
- risk gate decisions,
- paper execution,
- future IBKR/TWS adapter boundaries,
- trade journal records,
- audit logs.

### base44-app/

Base44 is only the Admin GUI and control plane. It may display data and send admin requests to the backend. It must not directly execute trades, connect to IBKR/TWS, or store broker credentials.

### IBKR/TWS or IB Gateway

IBKR/TWS or IB Gateway is the broker connection layer for future backend integration. Broker connectivity belongs behind backend execution adapters, not in route handlers or frontend code.

### PostgreSQL

PostgreSQL stores persistent trade, configuration, journal, and audit log data.

### Redis

Redis supports queues, cache, and background job coordination.

### AWS/VPS

Production hosting should run the backend and supporting services on AWS or a VPS with secrets supplied by the hosting environment.

## Default operating mode

- Paper trading enabled.
- Live trading disabled.
- Manual approval required.
- Risk gate mandatory before execution.
