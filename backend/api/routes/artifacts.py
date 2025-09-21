# backend/api/routes/artifacts.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
import json, os

router = APIRouter(prefix="/artifacts", tags=["artifacts"])

@router.get("/get")
def get_artifact(path: str = Query(..., description="Path returned by /analytics/run (e.g., artifacts/analysis/10/20240101_000000/risk_prediction.json)")):
    path = path.lstrip("/\\")
    if not os.path.exists(path):
        raise HTTPException(404, f"file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(data)
