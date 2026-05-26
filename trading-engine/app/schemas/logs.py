from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    timestamp: datetime
    event_type: str
    message: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class LogsResponse(BaseModel):
    logs: list[LogEntry]
