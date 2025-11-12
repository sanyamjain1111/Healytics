
from fastapi import APIRouter, Depends, Body
from ..routes.auth import get_current_user
from ..routes.analytics import _assert_owned
router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/download/{analysis_id}")
async def download_report(analysis_id: str):
    # Placeholder for export manager integration
    return {"status": "available", "analysis_id": analysis_id}
