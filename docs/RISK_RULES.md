# Risk Rules

The backend risk gate is mandatory for every trade candidate.

## Required safety defaults

- Paper trading is the default mode.
- Live trading is disabled by default.
- Manual approval is required by default.
- Kill switch support must fail closed.

## Required checks before execution

Every trade must pass:

- bot mode check,
- live trading enabled check,
- paper/live environment check,
- PDT guard,
- daily loss guard,
- margin guard,
- position size guard,
- liquidity guard,
- slippage guard,
- spread guard,
- manual approval check when required.

## Rejections

Every rejected trade must include a structured rejection reason. The bot must scan, rank, and reject weak opportunities rather than forcing trades.

## Orders

Every order must be logged. Execution is allowed only when:

- `risk_approved == true`
- `execution_allowed == true`
- `kill_switch_active == false`

## Return claims

The project must not include code or documentation that guarantees, promises, targets, or forces fixed daily returns.
