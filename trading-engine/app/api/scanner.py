from fastapi import APIRouter

from app.schemas.scanner import ScannerResultsResponse
from app.services import scanner_service


router = APIRouter(prefix="/scanner", tags=["scanner"])


@router.get("/results", response_model=ScannerResultsResponse)
def get_scanner_results() -> ScannerResultsResponse:
    return ScannerResultsResponse(results=scanner_service.get_scanner_results())
