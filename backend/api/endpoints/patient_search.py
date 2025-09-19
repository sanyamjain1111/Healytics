
from fastapi import APIRouter, HTTPException, Query
import pandas as pd

router = APIRouter(prefix="/patient-search", tags=["Patient Search"])

@router.get("/{patient_id}")
async def search_patient_by_id(patient_id: str, include_history: bool = Query(True)):
    try:
        patients = pd.read_csv("/mnt/data/medical-intellianalytics-pro/data/patients.csv", dtype={"patient_id": str})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"patients.csv missing: {e}")
    row = patients[patients["patient_id"] == patient_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Patient not found")
    profile = row.iloc[0].to_dict()
    history = []
    if include_history:
        try:
            outcomes = pd.read_csv("/mnt/data/medical-intellianalytics-pro/data/outcomes.csv", dtype={"patient_id": str})
            history = outcomes[outcomes["patient_id"] == patient_id].to_dict(orient="records")
        except Exception:
            history = []
    return {"patient_profile": profile, "historical_analyses": history, "current_status": {"note": "demo"}}
