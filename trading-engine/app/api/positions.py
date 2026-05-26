from fastapi import APIRouter

from app.schemas.positions import PositionsResponse
from app.services import position_service


router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("", response_model=PositionsResponse)
def get_positions() -> PositionsResponse:
    return PositionsResponse(positions=position_service.get_positions())
