from dataclasses import replace

from app.scanner.multi_asset_scanner import ScannerOpportunity


STATUS_PRIORITY = {
    "manual_approval": 0,
    "watchlist": 1,
    "reject": 2,
}


def rank_opportunities(
    opportunities: list[ScannerOpportunity],
) -> list[ScannerOpportunity]:
    sorted_opportunities = sorted(
        opportunities,
        key=lambda opportunity: (
            STATUS_PRIORITY.get(opportunity.status, 99),
            -opportunity.trade_quality_score,
            opportunity.symbol,
        ),
    )
    return [
        replace(opportunity, rank=index)
        for index, opportunity in enumerate(sorted_opportunities, start=1)
    ]
