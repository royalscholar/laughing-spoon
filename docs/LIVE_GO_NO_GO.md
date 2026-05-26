# Live Trading Go/No-Go Checklist

Live trading is disabled by default and is not implemented in this foundation.

Before live trading is considered, verify:

- paper trading works end to end,
- every trade candidate passes through the risk gate,
- rejected trades include rejection reasons,
- paper orders are logged,
- audit logs are durable,
- manual approval behavior works,
- kill switch behavior fails closed,
- PDT guard works,
- daily loss guard works,
- margin guard works,
- position size guard works,
- liquidity, slippage, and spread guards work,
- broker credentials are never stored in code, frontend, or repository files,
- Base44 remains a control plane only,
- IBKR/TWS connectivity exists only behind backend adapter boundaries,
- tests cover the paper/live mode split and risk gate behavior.

No live order execution should be added until this checklist has been reviewed and explicitly approved.
