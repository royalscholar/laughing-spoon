# Base44 Admin GUI

This directory is reserved for the Base44 Admin GUI and control plane.

Base44 may display scanner results, model probabilities, risk decisions, approval queues, settings, and logs. Base44 must call the external Python FastAPI backend for every trading-related action.

Base44 must not:

- connect directly to IBKR/TWS or IB Gateway,
- store broker credentials,
- place live broker orders,
- run the Python scanner,
- train ML models,
- run long-lived trading loops,
- bypass backend risk checks.

The Python backend is the final authority for scanning, risk checks, execution decisions, paper orders, future broker adapters, trade journaling, and audit logs.
