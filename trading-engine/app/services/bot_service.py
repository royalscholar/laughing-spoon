from app.schemas.bot import BotModeResponse
from app.schemas.kill_switch import KillSwitchResponse
from app.services import log_service, state


def set_bot_mode(mode: str) -> BotModeResponse:
    requested_mode = mode.lower().strip()

    if requested_mode == "live":
        log_service.add_log(
            "bot_mode_rejected",
            "Live mode request rejected because live trading is not implemented.",
            {"requested_mode": mode},
        )
        return BotModeResponse(
            bot_mode=state.bot_state.bot_mode,
            live_trading_enabled=False,
            paper_trading_enabled=state.bot_state.paper_trading_enabled,
            trading_enabled=not state.bot_state.kill_switch_active,
            message="Live trading is disabled by default and is not implemented in this skeleton.",
        )

    if requested_mode not in {"paper", "disabled"}:
        log_service.add_log(
            "bot_mode_rejected",
            "Unsupported bot mode request rejected.",
            {"requested_mode": mode},
        )
        return BotModeResponse(
            bot_mode=state.bot_state.bot_mode,
            live_trading_enabled=False,
            paper_trading_enabled=state.bot_state.paper_trading_enabled,
            trading_enabled=not state.bot_state.kill_switch_active,
            message="Unsupported bot mode. Allowed modes are paper and disabled.",
        )

    state.bot_state.bot_mode = requested_mode
    state.bot_state.live_trading_enabled = False
    state.bot_state.paper_trading_enabled = requested_mode == "paper"

    log_service.add_log(
        "bot_mode_updated",
        "Bot mode updated.",
        {"bot_mode": state.bot_state.bot_mode},
    )

    return BotModeResponse(
        bot_mode=state.bot_state.bot_mode,
        live_trading_enabled=state.bot_state.live_trading_enabled,
        paper_trading_enabled=state.bot_state.paper_trading_enabled,
        trading_enabled=state.bot_state.paper_trading_enabled
        and not state.bot_state.kill_switch_active,
        message=f"Bot mode set to {state.bot_state.bot_mode}.",
    )


def set_kill_switch(active: bool, reason: str | None = None) -> KillSwitchResponse:
    state.bot_state.kill_switch_active = active
    log_service.add_log(
        "kill_switch_updated",
        "Kill switch updated.",
        {"active": active, "reason": reason},
    )

    return KillSwitchResponse(
        kill_switch_active=state.bot_state.kill_switch_active,
        trading_enabled=not state.bot_state.kill_switch_active
        and state.bot_state.paper_trading_enabled,
        message="Trading disabled by kill switch."
        if state.bot_state.kill_switch_active
        else "Kill switch inactive; paper trading may proceed through the risk gate.",
    )
