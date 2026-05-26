from datetime import UTC, datetime
from typing import Any

from app.schemas.logs import LogEntry


_logs: list[LogEntry] = [
    LogEntry(
        timestamp=datetime.now(UTC),
        event_type="system",
        message="Trading engine started in paper mode with live trading disabled.",
        metadata={"bot_mode": "paper", "live_trading_enabled": False},
    )
]


def add_log(event_type: str, message: str, metadata: dict[str, Any] | None = None) -> LogEntry:
    entry = LogEntry(
        timestamp=datetime.now(UTC),
        event_type=event_type,
        message=message,
        metadata=metadata or {},
    )
    _logs.append(entry)
    return entry


def get_logs() -> list[LogEntry]:
    return list(_logs)


def reset_logs_for_tests() -> None:
    _logs.clear()
