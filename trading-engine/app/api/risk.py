from fastapi import APIRouter

from app.schemas.risk import RiskSettingsRequest, RiskSettingsResponse
from app.services import risk_service


router = APIRouter(prefix="/risk", tags=["risk"])


@router.post("/settings", response_model=RiskSettingsResponse)
def update_risk_settings(request: RiskSettingsRequest) -> RiskSettingsResponse:
    return RiskSettingsResponse(settings=risk_service.update_risk_settings(request))
