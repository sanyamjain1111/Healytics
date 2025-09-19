
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def intelligent_upload(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV")
    dataset_id = str(uuid.uuid4())
    # In production persist df to object store/DB; here we just echo
    return {"dataset_id": dataset_id, "rows": len(df), "columns": len(df.columns), "message": "uploaded"}
