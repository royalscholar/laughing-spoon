from dataclasses import dataclass


@dataclass(frozen=True)
class PaperOrderRequest:
    symbol: str
    action: str
    quantity: int
    order_type: str
    limit_price: float | None
    stop_price: float | None
    risk_approved: bool
    execution_allowed: bool
    paper_only: bool = True


def build_paper_order_request(
    symbol: str,
    action: str,
    quantity: int,
    order_type: str,
    risk_approved: bool,
    execution_allowed: bool,
    limit_price: float | None = None,
    stop_price: float | None = None,
) -> PaperOrderRequest:
    normalized_action = action.upper().strip()
    normalized_order_type = order_type.upper().strip()
    normalized_symbol = symbol.upper().strip()

    if not risk_approved:
        raise ValueError("risk_approved_required")
    if not execution_allowed:
        raise ValueError("execution_allowed_required")
    if normalized_action not in {"BUY", "SELL"}:
        raise ValueError("unsupported_order_action")
    if normalized_order_type not in {"MARKET", "LIMIT", "STOP"}:
        raise ValueError("unsupported_order_type")
    if quantity <= 0:
        raise ValueError("quantity_must_be_positive")
    if normalized_order_type == "LIMIT" and limit_price is None:
        raise ValueError("limit_price_required")
    if normalized_order_type == "STOP" and stop_price is None:
        raise ValueError("stop_price_required")

    return PaperOrderRequest(
        symbol=normalized_symbol,
        action=normalized_action,
        quantity=quantity,
        order_type=normalized_order_type,
        limit_price=limit_price,
        stop_price=stop_price,
        risk_approved=risk_approved,
        execution_allowed=execution_allowed,
        paper_only=True,
    )
