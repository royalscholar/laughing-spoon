from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    bot_mode: str
    live_trading_enabled: bool
    paper_trading_enabled: bool
    manual_approval_required: bool
    kill_switch_active: bool
    ibkr_connected: bool
