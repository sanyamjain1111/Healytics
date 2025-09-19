
from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional, List
from ...ml_library.model_factory import DynamicModelFactory
from ...services.model_training_service import train_model_api
from ...paths import ARTIFACT_DIR, REPORT_DIR
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/models", tags=["Models"])

@router.get("", response_model=List[str])
async def list_models():
    return list(DynamicModelFactory.MODEL_REGISTRY.keys())

@router.post("/train")
async def train_model(payload: Dict[str, Any] = Body(...)):
    name = payload.get("model_name")
    estimator = payload.get("estimator", "random_forest")
    target = payload.get("target")
    if not name:
        raise HTTPException(status_code=400, detail="model_name is required")
    res = await train_model_api(name, estimator=estimator, target=target)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.get("/{model_name}/artifacts")
async def get_artifacts(model_name: str):
    safe = "".join([c if c.isalnum() or c in ("-","_") else "_" for c in model_name])
    mdir = ARTIFACT_DIR / safe
    if not mdir.exists():
        raise HTTPException(status_code=404, detail="No artifacts yet for this model" )
    files = [str((mdir / f).resolve()) for f in os.listdir(mdir)]
    return {"files": files}

@router.get("/{model_name}/report/{fmt}")
async def get_report(model_name: str, fmt: str = "pdf"):
    safe = "".join([c if c.isalnum() or c in ("-","_") else "_" for c in model_name])
    rdir = REPORT_DIR / safe
    path = (rdir/"report.pdf") if fmt == "pdf" else (rdir/"report.html")
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(str(path))
