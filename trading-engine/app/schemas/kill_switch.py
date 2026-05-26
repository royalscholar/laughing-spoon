from pydantic import BaseModel


class KillSwitchRequest(BaseModel):
    active: bool
    reason: str | None = None


class KillSwitchResponse(BaseModel):
    kill_switch_active: bool
    trading_enabled: bool
    message: str
