from dataclasses import dataclass

from app.execution.order_builder import PaperOrderRequest, build_paper_order_request


@dataclass(frozen=True)
class BracketOrderIntent:
    parent: PaperOrderRequest
    take_profit: PaperOrderRequest
    stop_loss: PaperOrderRequest
    paper_only: bool = True


def build_bracket_order_intent(
    symbol: str,
    action: str,
    quantity: int,
    entry_limit_price: float,
    take_profit_price: float,
    stop_loss_price: float,
    risk_approved: bool,
    execution_allowed: bool,
) -> BracketOrderIntent:
    normalized_action = action.upper().strip()
    exit_action = "SELL" if normalized_action == "BUY" else "BUY"

    _validate_bracket_prices(
        normalized_action,
        entry_limit_price,
        take_profit_price,
        stop_loss_price,
    )

    return BracketOrderIntent(
        parent=build_paper_order_request(
            symbol=symbol,
            action=normalized_action,
            quantity=quantity,
            order_type="LIMIT",
            limit_price=entry_limit_price,
            stop_price=None,
            risk_approved=risk_approved,
            execution_allowed=execution_allowed,
        ),
        take_profit=build_paper_order_request(
            symbol=symbol,
            action=exit_action,
            quantity=quantity,
            order_type="LIMIT",
            limit_price=take_profit_price,
            stop_price=None,
            risk_approved=risk_approved,
            execution_allowed=execution_allowed,
        ),
        stop_loss=build_paper_order_request(
            symbol=symbol,
            action=exit_action,
            quantity=quantity,
            order_type="STOP",
            limit_price=None,
            stop_price=stop_loss_price,
            risk_approved=risk_approved,
            execution_allowed=execution_allowed,
        ),
        paper_only=True,
    )


def _validate_bracket_prices(
    action: str,
    entry_limit_price: float,
    take_profit_price: float,
    stop_loss_price: float,
) -> None:
    if entry_limit_price <= 0 or take_profit_price <= 0 or stop_loss_price <= 0:
        raise ValueError("prices_must_be_positive")

    if action == "BUY":
        if take_profit_price <= entry_limit_price:
            raise ValueError("take_profit_must_exceed_entry_for_buy")
        if stop_loss_price >= entry_limit_price:
            raise ValueError("stop_loss_must_be_below_entry_for_buy")
        return

    if action == "SELL":
        if take_profit_price >= entry_limit_price:
            raise ValueError("take_profit_must_be_below_entry_for_sell")
        if stop_loss_price <= entry_limit_price:
            raise ValueError("stop_loss_must_exceed_entry_for_sell")
        return

    raise ValueError("unsupported_order_action")
