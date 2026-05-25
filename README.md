# Algo Bot Trading Framework

This repository contains the original IBKR / multi-asset algorithmic trading framework.

## Current Baseline

- IBKR connection scripts
- Moving-average strategy scripts
- Multi-asset live bot scripts
- Backtesting scripts
- Data folder for ticker universe
- Strategy folder for strategy modules

## Next Build Phase

The next build phase will restructure the bot into a cleaner framework with:

- Broker adapter layer
- Market data layer
- Scanner engine
- Strategy engine
- Risk management engine
- Execution manager
- Backtesting and walk-forward validation
- ML signal engine
- Monitoring and alerting layer

# Algo Bot Trading Framework

This repository contains the original IBKR / multi-asset algorithmic trading bot framework and the new clean-build branch for scanner, risk, execution, and machine-learning expansion.

## Branches

- main: original uploaded bot baseline
- clean-build-ml-scanner: reorganized clean build for new development

## Clean Build Structure

- app/broker: broker connection and IBKR client logic
- app/data: ticker universe and market data loaders
- app/strategies: trading strategies
- app/scanner: scanner engine and filters
- app/risk: stop-loss, position sizing, and risk limits
- app/execution: order routing and execution manager
- app/ml: future machine-learning signal engine
- app/monitoring: alerts, logs, and performance tracking
- tests: backtests and test scripts
- docs: build notes and roadmap

## Immediate Roadmap

1. Verify original scripts still run.
2. Clean and modularize IBKR connection logic.
3. Add scanner engine.
4. Add risk controls.
5. Add backtesting and walk-forward validation.
6. Add ML signal model only after the base framework is stable.