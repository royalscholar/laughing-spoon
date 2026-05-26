from app.schemas.health import HealthResponse
from app.execution.ibkr_client import check_ibkr_connected
from app.services import state


def get_health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        bot_mode=state.bot_state.bot_mode,
        live_trading_enabled=state.bot_state.live_trading_enabled,
        paper_trading_enabled=state.bot_state.paper_trading_enabled,
        manual_approval_required=state.bot_state.manual_approval_required,
        kill_switch_active=state.bot_state.kill_switch_active,
        ibkr_connected=check_ibkr_connected(),
    )
