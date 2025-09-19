# app/routers/adhoc.py
from __future__ import annotations
import os, json
from typing import Optional, Dict, Any, List
import pandas as pd
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text, create_engine
from sqlalchemy.engine import Engine

# engine & SessionLocal from your current project
try:
    from ..database import engine as _app_engine, SessionLocal as _SessionLocal  # type: ignore
except Exception:
    _app_engine, _SessionLocal = None, None

from joblib import load as _load

router = APIRouter(prefix="/adhoc", tags=["ad-hoc"])

def _get_engine() -> Engine:
    if _app_engine is not None:
        return _app_engine
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set and no app engine found")
    return create_engine(url, future=True)

def get_db():
    if _SessionLocal is None:
        # Provide a dummy generator to keep Depends happy
        def _dummy():
            yield None
        return _dummy()
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PatientPredictionRequest(BaseModel):
    dataset_id: int = Field(..., ge=1)
    strategy_id: int = Field(..., ge=1)
    patient_id: Optional[str] = None

def _read_strategy(dataset_id: int, strategy_id: int) -> Dict[str, Any]:
    eng = _get_engine()
    with eng.begin() as con:
        row = con.execute(
            text("SELECT parsed FROM strategies WHERE id = :sid AND dataset_id = :d"),
            {"sid": strategy_id, "d": dataset_id},
        ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Strategy not found for this dataset")
    parsed = row.get("parsed")
    if isinstance(parsed, str):
        try:
            parsed = json.loads(parsed)
        except Exception:
            parsed = {}
    return parsed or {}

def _extract_models_and_thresholds(strategy_json: Dict[str, Any]) -> Dict[str, Any]:
    models: List[str] = []
    thresholds: Dict[str, float] = strategy_json.get("thresholds", {}) or {}
    if "models" in strategy_json and isinstance(strategy_json["models"], list):
        models = [m for m in strategy_json["models"] if isinstance(m, str)]
    else:
        mep = (strategy_json.get("model_execution_plan") or {}).get("primary_models") or []
        for item in mep:
            if isinstance(item, dict) and item.get("model_name"):
                models.append(item["model_name"])
    # also support parsed form we store: selected_models
    if not models and isinstance(strategy_json.get("selected_models"), list):
        models = [str(m) for m in strategy_json["selected_models"]]
    return {"models": models, "thresholds": thresholds}

def _fetch_patient(dataset_id: int, patient_id: Optional[str] = None) -> pd.DataFrame:
    eng = _get_engine()
    if patient_id:
        sql = text("""SELECT * FROM patient_records WHERE dataset_id = :d AND patient_id = :pid LIMIT 1""")
        params = {"d": dataset_id, "pid": patient_id}
    else:
        sql = text("""SELECT * FROM patient_records WHERE dataset_id = :d ORDER BY random() LIMIT 1""")
        params = {"d": dataset_id}
    df = pd.read_sql(sql, con=eng, params=params)
    if df.empty:
        raise HTTPException(status_code=404, detail="Patient not found for dataset")
    return df

def _infer_single_model(model, Xrow: pd.DataFrame, thr: float) -> Dict[str, Any]:
    try:
        if hasattr(model, "predict_proba"):
            prob = float(model.predict_proba(Xrow)[:, 1][0])
            return {"kind": "classification", "score": prob, "pred": int(prob >= thr), "threshold": thr}
        pred = float(model.predict(Xrow)[0])
        return {"kind": "regression", "prediction": pred}
    except Exception as e:
        return {"error": f"inference error: {e.__class__.__name__}: {e}"}

@router.get("/random")
def get_random_patient(dataset_id: int = Query(..., ge=1)) -> Dict[str, Any]:
    df = _fetch_patient(dataset_id)
    return {"patient": df.to_dict(orient="records")[0]}

@router.get("/patient/{patient_id}")
def get_patient(patient_id: str, dataset_id: int = Query(..., ge=1)) -> Dict[str, Any]:
    df = _fetch_patient(dataset_id, patient_id)
    return {"patient": df.to_dict(orient="records")[0]}

@router.post("/predict")
def predict_for_patient(req: PatientPredictionRequest, _db = Depends(get_db)) -> Dict[str, Any]:
    strategy_json = _read_strategy(req.dataset_id, req.strategy_id)
    extracted = _extract_models_and_thresholds(strategy_json)
    models = extracted["models"]
    thresholds = extracted["thresholds"]

    if not models:
        raise HTTPException(
            status_code=400,
            detail="No models listed in strategy. Generate/select a strategy before running ad-hoc predictions."
        )

    df = _fetch_patient(req.dataset_id, req.patient_id)
    patient_record = df.to_dict(orient="records")[0]
    feature_df = df.drop(columns=[c for c in ("id", "dataset_id") if c in df.columns], errors="ignore")

    results: Dict[str, Any] = {}
    artifacts_dir = os.getenv("ARTIFACTS_DIR", os.path.join("artifacts", "models"))

    for m in models:
        path = os.path.join(artifacts_dir, f"{m}.joblib")
        if not os.path.exists(path):
            results[m] = {"error": "Model file not found. Train/models export required.", "path": path}
            continue
        try:
            model = _load(path)
            thr = float(thresholds.get(m, 0.5))
            results[m] = _infer_single_model(model, feature_df, thr)
        except Exception as e:
            results[m] = {"error": f"load/predict error: {e.__class__.__name__}: {e}"}

    return {
        "dataset_id": req.dataset_id,
        "strategy_id": req.strategy_id,
        "patient": patient_record,
        "predictions": results,
        "strategy_echo": {"models": models, "thresholds": thresholds}
    }

@router.get("/predict/random")
def predict_for_random(dataset_id: int = Query(..., ge=1), strategy_id: int = Query(..., ge=1)):
    req = PatientPredictionRequest(dataset_id=dataset_id, strategy_id=strategy_id, patient_id=None)
    return predict_for_patient(req)
