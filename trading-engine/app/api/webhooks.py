from fastapi import APIRouter

from app.schemas.webhooks import TradingViewWebhookRequest, WebhookResponse
from app.services import webhook_service


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/tradingview", response_model=WebhookResponse)
def tradingview_webhook(request: TradingViewWebhookRequest) -> WebhookResponse:
    return webhook_service.handle_tradingview_webhook(request)
