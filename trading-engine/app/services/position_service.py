from app.schemas.positions import Position


def get_positions() -> list[Position]:
    return [
        Position(
            symbol="AAPL",
            asset_type="stock",
            quantity=5,
            average_price=195.10,
            market_value=975.50,
            unrealized_pnl=0.0,
            environment="paper",
        )
    ]
