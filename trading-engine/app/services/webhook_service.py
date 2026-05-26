from app.schemas.webhooks import TradingViewWebhookRequest, WebhookResponse
from app.services import log_service


def handle_tradingview_webhook(request: TradingViewWebhookRequest) -> WebhookResponse:
    log_service.add_log(
        "tradingview_webhook_received",
        "TradingView webhook received and logged without execution.",
        {
            "symbol": request.symbol,
            "signal": request.signal,
            "strategy": request.strategy,
            "timeframe": request.timeframe,
        },
    )
    return WebhookResponse(
        accepted=True,
        message="Webhook accepted for logging only. No trade was executed.",
        candidate_created=False,
    )
