# Deployment

This project is currently scaffolded for safe local development and future AWS/VPS deployment.

## Local development

Use Docker Compose for local PostgreSQL, Redis, and the FastAPI backend:

```bash
docker compose up --build
```

The compose configuration starts the backend with:

- `BOT_MODE=paper`
- `LIVE_TRADING_ENABLED=false`
- `MANUAL_APPROVAL_REQUIRED=true`
- `KILL_SWITCH_ACTIVE=false`

## Environment variables

Use `.env.example` as a template. Copy it to `.env` locally when needed.

Never commit:

- `.env`
- broker credentials
- API keys
- account numbers
- access tokens

## Production direction

AWS or VPS hosting should provide:

- FastAPI backend process,
- PostgreSQL,
- Redis,
- secure environment variable injection,
- logs and monitoring,
- network access to the broker gateway only when live trading has been explicitly approved.

Live trading must remain disabled until paper trading, risk gates, audit logging, and operational controls are verified.
