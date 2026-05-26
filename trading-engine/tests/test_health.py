from fastapi.testclient import TestClient

from main import app


def test_health_reports_safe_defaults() -> None:
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "bot_mode": "paper",
        "live_trading_enabled": False,
        "paper_trading_enabled": True,
        "manual_approval_required": True,
        "kill_switch_active": False,
    }
