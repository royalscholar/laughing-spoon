from dataclasses import dataclass
import socket

from app.core.settings import Settings, get_settings


@dataclass(frozen=True)
class IbkrConnectionConfig:
    host: str
    port: int
    client_id: int
    paper_only: bool = True


@dataclass(frozen=True)
class IbkrConnectionStatus:
    attempted: bool
    connected: bool
    paper_only: bool
    host: str
    port: int
    client_id: int
    message: str


def get_ibkr_config(settings: Settings | None = None) -> IbkrConnectionConfig:
    active_settings = settings or get_settings()
    return IbkrConnectionConfig(
        host=active_settings.ib_host,
        port=active_settings.ib_port,
        client_id=active_settings.ib_client_id,
        paper_only=True,
    )


def test_ibkr_connection(timeout_seconds: float = 0.2) -> IbkrConnectionStatus:
    config = get_ibkr_config()
    try:
        with socket.create_connection(
            (config.host, config.port),
            timeout=timeout_seconds,
        ):
            return IbkrConnectionStatus(
                attempted=True,
                connected=True,
                paper_only=config.paper_only,
                host=config.host,
                port=config.port,
                client_id=config.client_id,
                message="Connected to configured IBKR paper endpoint.",
            )
    except OSError as exc:
        return IbkrConnectionStatus(
            attempted=True,
            connected=False,
            paper_only=config.paper_only,
            host=config.host,
            port=config.port,
            client_id=config.client_id,
            message=f"IBKR paper endpoint unavailable: {exc.__class__.__name__}",
        )


def check_ibkr_connected(timeout_seconds: float = 0.05) -> bool:
    return test_ibkr_connection(timeout_seconds=timeout_seconds).connected
