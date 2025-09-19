from __future__ import annotations
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import numpy as np
from ..services.datasets_service import registry, load_dataframe

router = APIRouter(prefix="/patients", tags=["patients"])

ID_HINTS = ("patient", "mrn", "name", "id", "identifier")

@router.get("/search")
def search_patients(
    dataset_id: str = Query(...),
    q: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=500)
) -> Dict[str, Any]:
    ds = registry.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = load_dataframe(registry.path_for(dataset_id))

    # Pick candidate columns
    cand_cols: List[str] = []
    for c in df.columns:
        lc = c.lower()
        if any(h in lc for h in ID_HINTS):
            cand_cols.append(c)
    if not cand_cols:
        # fall back to all object columns
        cand_cols = [c for c in df.columns if df[c].dtype == "object"]

    if not cand_cols:
        return {"columns": [], "rows": []}

    q_lower = q.lower()
    mask = False
    for c in cand_cols:
        ser = df[c].astype(str).str.lower()
        mask = (mask | ser.str.contains(q_lower, na=False))
    sub = df.loc[mask].head(limit)
    return {"columns": list(sub.columns), "rows": sub.astype(object).where(pd.notna(sub), None).values.tolist()}