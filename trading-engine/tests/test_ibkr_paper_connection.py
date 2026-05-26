import socket

import pytest
from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.execution.bracket_orders import build_bracket_order_intent
from app.execution.fill_monitor import get_fill_monitor_status
from app.execution.ibkr_client import (
    get_ibkr_config,
    test_ibkr_connection as check_ibkr_connection_status,
)
from app.execution.order_builder import build_paper_order_request
from main import app


def test_ibkr_defaults_are_paper_safe() -> None:
    settings = Settings()

    assert settings.live_trading_enabled is False
    assert settings.paper_trading_enabled is True
    assert settings.ib_host == "127.0.0.1"
    assert settings.ib_port == 7497
    assert settings.ib_client_id == 1


def test_get_ibkr_config_returns_requested_env_defaults() -> None:
    config = get_ibkr_config(Settings(ib_host="localhost", ib_port=4002, ib_client_id=9))

    assert config.host == "localhost"
    assert config.port == 4002
    assert config.client_id == 9
    assert config.paper_only is True


def test_ibkr_connection_status_does_not_raise_when_unavailable() -> None:
    status = check_ibkr_connection_status(timeout_seconds=0.001)

    assert status.attempted is True
    assert status.paper_only is True
    assert status.port == 7497
    assert isinstance(status.connected, bool)
    assert status.message


def test_ibkr_connection_status_reports_connected_when_socket_opens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeSocket:
        def __enter__(self) -> "FakeSocket":
            return self

        def __exit__(self, *args: object) -> None:
            return None

    monkeypatch.setattr(socket, "create_connection", lambda *args, **kwargs: FakeSocket())

    status = check_ibkr_connection_status(timeout_seconds=0.001)

    assert status.connected is True
    assert status.paper_only is True


def test_paper_order_builder_requires_risk_approval() -> None:
    with pytest.raises(ValueError, match="risk_approved_required"):
        build_paper_order_request(
            symbol="AAPL",
            action="BUY",
            quantity=1,
            order_type="MARKET",
            risk_approved=False,
            execution_allowed=True,
        )


def test_paper_order_builder_requires_execution_allowed() -> None:
    with pytest.raises(ValueError, match="execution_allowed_required"):
        build_paper_order_request(
            symbol="AAPL",
            action="BUY",
            quantity=1,
            order_type="MARKET",
            risk_approved=True,
            execution_allowed=False,
        )


def test_paper_order_builder_creates_local_intent_only() -> None:
    order = build_paper_order_request(
        symbol="aapl",
        action="buy",
        quantity=3,
        order_type="limit",
        limit_price=195.25,
        risk_approved=True,
        execution_allowed=True,
    )

    assert order.symbol == "AAPL"
    assert order.action == "BUY"
    assert order.order_type == "LIMIT"
    assert order.paper_only is True


def test_bracket_order_intent_builds_paper_only_when_risk_approved() -> None:
    bracket = build_bracket_order_intent(
        symbol="AAPL",
        action="BUY",
        quantity=2,
        entry_limit_price=195.0,
        take_profit_price=205.0,
        stop_loss_price=190.0,
        risk_approved=True,
        execution_allowed=True,
    )

    assert bracket.paper_only is True
    assert bracket.parent.paper_only is True
    assert bracket.take_profit.action == "SELL"
    assert bracket.stop_loss.order_type == "STOP"


def test_bracket_order_intent_requires_valid_prices() -> None:
    with pytest.raises(ValueError, match="take_profit_must_exceed_entry_for_buy"):
        build_bracket_order_intent(
            symbol="AAPL",
            action="BUY",
            quantity=2,
            entry_limit_price=195.0,
            take_profit_price=194.0,
            stop_loss_price=190.0,
            risk_approved=True,
            execution_allowed=True,
        )


def test_fill_monitor_is_inactive_placeholder() -> None:
    status = get_fill_monitor_status()

    assert status.active is False
    assert status.paper_only is True
    assert "inactive" in status.message


def test_health_includes_ibkr_connected_field(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.services.health_service.check_ibkr_connected", lambda: False)
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["ibkr_connected"] is False
