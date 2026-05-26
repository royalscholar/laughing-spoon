from fastapi.testclient import TestClient

from main import app


def test_scanner_results_return_mock_data() -> None:
    client = TestClient(app)

    response = client.get("/api/scanner/results")

    assert response.status_code == 200
    payload = response.json()
    assert payload["results"]
    assert payload["results"][0]["signal"] == "mock_scanner_v1"


def test_trade_candidates_return_mock_data() -> None:
    client = TestClient(app)

    response = client.get("/api/trades/candidates")

    assert response.status_code == 200
    payload = response.json()
    assert payload["candidates"]
    assert payload["candidates"][0]["status"] == "pending_review"


def test_approve_trade_calls_risk_gate_and_only_approves_paper() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/trades/approve",
        json={"candidate_id": "mock-aapl-breakout", "approved_by": "admin"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "approved_for_paper"
    assert payload["risk_decision"]["risk_approved"] is True
    assert payload["risk_decision"]["execution_allowed"] is True
    assert "No live broker order was placed" in payload["message"]


def test_approve_trade_fails_when_kill_switch_is_active() -> None:
    client = TestClient(app)

    kill_switch_response = client.post(
        "/api/kill-switch",
        json={"active": True, "reason": "test safety stop"},
    )
    assert kill_switch_response.status_code == 200
    assert kill_switch_response.json()["trading_enabled"] is False

    response = client.post(
        "/api/trades/approve",
        json={"candidate_id": "mock-aapl-breakout", "approved_by": "admin"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "rejected_by_risk_gate"
    assert payload["risk_decision"]["risk_approved"] is False
    assert "kill_switch_active" in payload["risk_decision"]["rejection_reasons"]


def test_reject_trade_requires_rejection_reason() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/trades/reject",
        json={"candidate_id": "mock-aapl-breakout", "rejected_by": "admin"},
    )

    assert response.status_code == 422


def test_bot_mode_cannot_enable_live_trading() -> None:
    client = TestClient(app)

    response = client.post("/api/bot/mode", json={"mode": "live"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["bot_mode"] == "paper"
    assert payload["live_trading_enabled"] is False
    assert "not implemented" in payload["message"]


def test_risk_settings_can_update_placeholder_threshold() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/risk/settings",
        json={
            "max_daily_loss": 250.0,
            "max_position_size": 500.0,
            "max_symbol_exposure": 1000.0,
            "min_probability": 0.8,
            "max_spread_percent": 0.5,
            "require_manual_approval": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["settings"]["min_probability"] == 0.8

    approval_response = client.post(
        "/api/trades/approve",
        json={"candidate_id": "mock-aapl-breakout", "approved_by": "admin"},
    )
    payload = approval_response.json()
    assert payload["status"] == "rejected_by_risk_gate"
    assert (
        "minimum_trade_quality_score_not_met"
        in payload["risk_decision"]["rejection_reasons"]
    )


def test_tradingview_webhook_logs_without_execution() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/webhooks/tradingview",
        json={
            "symbol": "AAPL",
            "signal": "buy",
            "price": 195.25,
            "timeframe": "5m",
            "strategy": "mock_alert",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "accepted": True,
        "message": "Webhook accepted for logging only. No trade was executed.",
        "candidate_created": False,
    }

    logs_response = client.get("/api/logs")
    assert logs_response.status_code == 200
    assert logs_response.json()["logs"][0]["event_type"] == "tradingview_webhook_received"


def test_positions_return_paper_positions_only() -> None:
    client = TestClient(app)

    response = client.get("/api/positions")

    assert response.status_code == 200
    assert response.json()["positions"][0]["environment"] == "paper"
