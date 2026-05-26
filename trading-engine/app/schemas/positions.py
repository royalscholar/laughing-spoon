from pydantic import BaseModel


class Position(BaseModel):
    symbol: str
    asset_type: str
    quantity: float
    average_price: float
    market_value: float
    unrealized_pnl: float
    environment: str


class PositionsResponse(BaseModel):
    positions: list[Position]
