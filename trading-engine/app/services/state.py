from dataclasses import dataclass

from app.core.settings import get_settings
from app.schemas.risk import RiskSettingsRequest
from app.schemas.trades import TradeCandidate


@dataclass
class BotState:
    bot_mode: str
    live_trading_enabled: bool
    paper_trading_enabled: bool
    manual_approval_required: bool
    kill_switch_active: bool


def _initial_bot_state() -> BotState:
    settings = get_settings()
    return BotState(
        bot_mode=settings.bot_mode,
        live_trading_enabled=settings.live_trading_enabled,
        paper_trading_enabled=settings.paper_trading_enabled,
        manual_approval_required=settings.manual_approval_required,
        kill_switch_active=settings.kill_switch_active,
    )


bot_state = _initial_bot_state()

risk_settings = RiskSettingsRequest()

mock_trade_candidates: list[TradeCandidate] = [
    TradeCandidate(
        candidate_id="mock-aapl-breakout",
        symbol="AAPL",
        asset_type="stock",
        side="buy",
        strategy="mock_breakout",
        probability=0.72,
        proposed_entry=195.10,
        proposed_stop=191.50,
        proposed_target=203.00,
        status="pending_review",
    ),
    TradeCandidate(
        candidate_id="mock-spy-mean-reversion",
        symbol="SPY",
        asset_type="etf",
        side="buy",
        strategy="mock_mean_reversion",
        probability=0.61,
        proposed_entry=530.25,
        proposed_stop=526.00,
        proposed_target=538.50,
        status="pending_review",
    ),
]


def reset_state_for_tests() -> None:
    bot_state.bot_mode = "paper"
    bot_state.live_trading_enabled = False
    bot_state.paper_trading_enabled = True
    bot_state.manual_approval_required = True
    bot_state.kill_switch_active = False

    global risk_settings
    risk_settings = RiskSettingsRequest()

    for candidate in mock_trade_candidates:
        candidate.status = "pending_review"
