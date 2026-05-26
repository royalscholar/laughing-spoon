from fastapi import APIRouter

from app.schemas.bot import BotModeRequest, BotModeResponse
from app.schemas.kill_switch import KillSwitchRequest, KillSwitchResponse
from app.services import bot_service


router = APIRouter(tags=["bot"])


@router.post("/bot/mode", response_model=BotModeResponse)
def set_bot_mode(request: BotModeRequest) -> BotModeResponse:
    return bot_service.set_bot_mode(request.mode)


@router.post("/kill-switch", response_model=KillSwitchResponse)
def set_kill_switch(request: KillSwitchRequest) -> KillSwitchResponse:
    return bot_service.set_kill_switch(request.active, request.reason)
