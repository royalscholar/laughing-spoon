from fastapi import APIRouter

from app.schemas.logs import LogsResponse
from app.services import log_service


router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("", response_model=LogsResponse)
def get_logs() -> LogsResponse:
    return LogsResponse(logs=log_service.get_logs())
