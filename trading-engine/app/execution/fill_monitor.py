from dataclasses import dataclass


@dataclass(frozen=True)
class FillMonitorStatus:
    active: bool
    paper_only: bool
    message: str


def get_fill_monitor_status() -> FillMonitorStatus:
    return FillMonitorStatus(
        active=False,
        paper_only=True,
        message="Fill monitor placeholder is inactive; no broker polling is running.",
    )
