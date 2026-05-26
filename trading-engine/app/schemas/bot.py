from pydantic import BaseModel


class BotModeRequest(BaseModel):
    mode: str


class BotModeResponse(BaseModel):
    bot_mode: str
    live_trading_enabled: bool
    paper_trading_enabled: bool
    trading_enabled: bool
    message: str
