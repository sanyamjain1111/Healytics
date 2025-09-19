# app/routers/analytics.py
from __future__ import annotations
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import os
import json
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from ..services.datasets_service import registry, load_dataframe
from ..services.analysis_service import histograms_for_columns, duckdb_query

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from pathlib import Path
import joblib

# -------- json export helper --------
try:
    from utils.json_export import write_json as _write_json
except Exception:
    def _write_json(path: str, payload: Dict[str, Any]) -> None:
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)

# -------- DB engine --------
try:
    from ..database import engine as _app_engine  # type: ignore
except Exception:
    _app_engine = None

router = APIRouter(prefix="/analytics", tags=["analytics"])

def _get_engine() -> Engine:
    if _app_engine is not None:
        return _app_engine
    url = "postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
    if not url:
        raise RuntimeError("DATABASE_URL not set and no app engine found")
    return create_engine(url, future=True)

def _ensure_analysis_tables(engine: Engine) -> None:
    DDL = """
    CREATE TABLE IF NOT EXISTS analyses (
      id BIGSERIAL PRIMARY KEY,
      dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
      strategy_id INT,
      kind TEXT,
      artifact_path TEXT,
      summary JSONB,
      created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    with engine.begin() as con:
        for stmt in filter(None, DDL.split(";")):
            st = stmt.strip()
            if st:
                con.execute(text(st + ";"))

def _load_df(dataset_id: int) -> pd.DataFrame:
    """
    Prefer Postgres; if that fails (e.g., ingestion didn't write rows yet),
    try to resolve the dataset NAME from DB and then load the file with the same name
    from the registry.
    """
    errors = []
    
    # 1) DB read
    try:
        eng = _get_engine()
        with eng.begin() as con:
            df = pd.read_sql(
                text("SELECT * FROM patient_records WHERE dataset_id=:d"),
                con, params={"d": int(dataset_id)}
            )
        if df.empty:
            errors.append("No patient records found in database for dataset_id")
        else:
            if "id" in df.columns:
                df = df.drop(columns=["id"])
            print(f"Successfully loaded {len(df)} rows from database")
            return df
    except Exception as e:
        errors.append(f"Database read failed: {str(e)}")

    # 2) fallback: find dataset name, then match registry by name
    try:
        eng = _get_engine()
        with eng.begin() as con:
            row = con.execute(
                text("SELECT name FROM datasets WHERE id=:d"),
                {"d": int(dataset_id)}
            ).mappings().first()
        
        if not row:
            errors.append(f"Dataset ID {dataset_id} not found in datasets table")
        elif not row.get("name"):
            errors.append(f"Dataset ID {dataset_id} has no name in datasets table")
        else:
            ds_name = str(row["name"]).strip().lower()
            print(f"Found dataset name: '{ds_name}'")
            
            # search registry by name
            try:
                registry_entries = registry.list()
                print(f"Registry has {len(registry_entries)} entries")
                
                for entry in registry_entries:
                    nm = str(entry.get("name", "")).strip().lower()
                    print(f"Checking registry entry: '{nm}' vs '{ds_name}'")
                    if nm == ds_name:
                        df = load_dataframe(registry.path_for(entry["id"]))
                        print(f"Successfully loaded {len(df)} rows from registry")
                        return df
                
                errors.append(f"Dataset name '{ds_name}' not found in registry")
            except Exception as e:
                errors.append(f"Registry search failed: {str(e)}")
    except Exception as e:
        errors.append(f"Dataset name lookup failed: {str(e)}")

    # 3) last resort: old behavior (id match)
    try:
        ds = registry.get(str(dataset_id))
        if ds:
            df = load_dataframe(registry.path_for(str(dataset_id)))
            print(f"Successfully loaded {len(df)} rows from registry by ID")
            return df
        else:
            errors.append(f"Dataset ID {dataset_id} not found in registry")
    except Exception as e:
        errors.append(f"Registry ID lookup failed: {str(e)}")

    # If we get here, all methods failed
    error_details = "; ".join(errors)
    print(f"All dataset loading methods failed: {error_details}")
    raise HTTPException(
        status_code=404, 
        detail=f"Dataset not found. Attempted methods: {error_details}"
    )

# ---------------- Existing endpoints ----------------

@router.get("/histograms")
def histograms(
    dataset_id: int = Query(...),
    columns: Optional[str] = Query(None),
    bins: int = Query(20, ge=5, le=200)
) -> Dict[str, Any]:
    df = _load_df(dataset_id)
    cols = None
    if columns:
        cols = [c.strip() for c in columns.split(",") if c.strip() in df.columns]
    hists = histograms_for_columns(df, columns=cols, bins=bins)

    decorated = []
    for h in hists:
        col = h.get("column", "value")
        decorated.append({
            **h,
            "title": f"Distribution of {col}",
            "xLabel": col,
            "yLabel": "Count"
        })
    return {"histograms": decorated}

@router.post("/ad-hoc")
def ad_hoc_sql(body: Dict[str, Any]) -> Dict[str, Any]:
    dataset_id = body.get("dataset_id")
    sql = body.get("sql")
    if not dataset_id or not sql:
        raise HTTPException(status_code=400, detail="dataset_id and sql required")
    df = _load_df(int(dataset_id))
    cols, rows = duckdb_query(df, sql)
    return {"columns": cols, "rows": rows}

# ---------------- Ad-hoc random + predict ----------------

class AdhocPredictRequest(BaseModel):
    dataset_id: int
    patient_id: Optional[str] = None
    patient: Optional[Dict[str, Any]] = None
    strategy_id: Optional[int] = None

@router.get("/adhoc/random")
def adhoc_random(dataset_id: int = Query(...)) -> Dict[str, Any]:
    df = _load_df(dataset_id)
    if df.empty:
        raise HTTPException(status_code=404, detail="No records in dataset")
    row = df.sample(1, random_state=np.random.randint(0, 1_000_000)).iloc[0].to_dict()
    return {"patient": row}

def _artifact_path(model_name: str) -> Optional[str]:
    for p in (
        f"artifacts/models/{model_name}.joblib",
        f"artifacts/{model_name}.joblib",
        f"training_data/models/{model_name}.joblib",
    ):
        if os.path.exists(p):
            return p
    return None

def _predict_with_model(model_name: str, X: pd.DataFrame, threshold: float = 0.5) -> Dict[str, Any]:
    pth = _artifact_path(model_name)
    if pth:
        try:
            model = joblib.load(pth)
            if hasattr(model, "predict_proba"):
                prob = float(model.predict_proba(X)[:, 1][0])
                pred = int(prob >= threshold)
                return {"score": prob, "pred": pred, "threshold": threshold, "source": "model"}
            elif hasattr(model, "predict"):
                val = float(model.predict(X)[0])
                return {"prediction": val, "source": "model"}
        except Exception:
            pass
    # heuristic fallback
    row = X.iloc[0].to_dict()
    risk = 0.0
    if "age" in row and pd.notna(row["age"]):
        risk += min(float(row["age"]) / 100.0, 0.5)
    if "systolic_bp" in row and pd.notna(row["systolic_bp"]) and row["systolic_bp"] > 150:
        risk += 0.2
    if "glucose" in row and pd.notna(row["glucose"]) and row["glucose"] > 180:
        risk += 0.2
    risk = max(0.0, min(1.0, risk))
    return {"score": risk, "pred": int(risk >= threshold), "threshold": threshold, "source": "heuristic"}

def _load_latest_strategy(engine: Engine, dataset_id: int) -> Optional[Dict[str, Any]]:
    with engine.begin() as con:
        row = con.execute(
            text("SELECT id, parsed FROM strategies WHERE dataset_id=:d ORDER BY id DESC LIMIT 1"),
            {"d": int(dataset_id)}
        ).mappings().first()
        if row:
            parsed = row["parsed"] if isinstance(row["parsed"], dict) else json.loads(row["parsed"])
            return {"id": int(row["id"]), "parsed": parsed}
    return None

@router.post("/adhoc/predict")
def adhoc_predict(req: AdhocPredictRequest) -> Dict[str, Any]:
    df = _load_df(req.dataset_id)
    if req.patient is not None:
        x = pd.DataFrame([req.patient])
    elif req.patient_id is not None and "patient_id" in df.columns:
        sub = df[df["patient_id"].astype(str) == str(req.patient_id)]
        if sub.empty:
            raise HTTPException(status_code=404, detail="patient_id not found in dataset")
        x = sub.iloc[[0]]
    else:
        x = df.sample(1, random_state=np.random.randint(0, 1_000_000))

    eng = _get_engine()
    _ensure_analysis_tables(eng)

    strategy = None
    if req.strategy_id:
        with eng.begin() as con:
            row = con.execute(
                text("SELECT id, parsed FROM strategies WHERE id=:s AND dataset_id=:d"),
                {"s": int(req.strategy_id), "d": int(req.dataset_id)}
            ).mappings().first()
            if row:
                parsed = row["parsed"] if isinstance(row["parsed"], dict) else json.loads(row["parsed"])
                strategy = {"id": int(row["id"]), "parsed": parsed}
    if strategy is None:
        strategy = _load_latest_strategy(eng, req.dataset_id)

    selected = []
    thresholds = {}
    if strategy and isinstance(strategy.get("parsed"), dict):
        parsed = strategy["parsed"]
        selected = list(parsed.get("selected_models", []))
        thresholds = dict(parsed.get("thresholds", {}))
    if not selected:
        selected = ["MortalityRiskModel", "SepsisEarlyWarning", "LengthOfStayRegressor"]

    preds: Dict[str, Any] = {}
    for m in selected:
        th = float(thresholds.get(m, 0.5))
        preds[m] = _predict_with_model(m, x, threshold=th)

    pid = str(x.iloc[0].get("patient_id", "adhoc"))
    return {"patient_id": pid, "predictions": preds, "strategy_id": (strategy or {}).get("id")}

# ---------------- Full analysis run ----------------

class AnalysisRunRequest(BaseModel):
    dataset_id: int
    strategy_id: Optional[int] = None

@router.post("/run")
def run_analysis(req: AnalysisRunRequest) -> Dict[str, Any]:
    print(f"Running analysis for dataset {req.dataset_id} with strategy {req.strategy_id}")
    df = _load_df(req.dataset_id)
    if df.empty:
        raise HTTPException(status_code=400, detail="Dataset has no rows")

    eng = _get_engine()
    _ensure_analysis_tables(eng)

    strategy = None
    if req.strategy_id:
        with eng.begin() as con:
            row = con.execute(
                text("SELECT id, parsed FROM strategies WHERE id=:s AND dataset_id=:d"),
                {"s": int(req.strategy_id), "d": int(req.dataset_id)}
            ).mappings().first()
            if row:
                parsed = row["parsed"] if isinstance(row["parsed"], dict) else json.loads(row["parsed"])
                strategy = {"id": int(row["id"]), "parsed": parsed}
    if strategy is None:
        strategy = _load_latest_strategy(eng, req.dataset_id)

    selected = []
    thresholds = {}
    if strategy and isinstance(strategy.get("parsed"), dict):
        parsed = strategy["parsed"]
        selected = list(parsed.get("selected_models", []))
        thresholds = dict(parsed.get("thresholds", {}))
    if not selected:
        selected = ["MortalityRiskModel", "SepsisEarlyWarning", "LengthOfStayRegressor"]

    ts = time.strftime("%Y%m%d_%H%M%S")
    base_dir = f"artifacts/analysis/{req.dataset_id}/{ts}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)

    # Risk JSON
    risk_rows: List[Dict[str, Any]] = []
    for idx, row in df.iterrows():
        x = pd.DataFrame([row.to_dict()])
        entry = {"patient_id": str(row.get("patient_id", idx))}
        for m in selected:
            th = float(thresholds.get(m, 0.5))
            entry[m] = _predict_with_model(m, x, threshold=th)
        risk_rows.append(entry)

    risk_summary = {
        "dataset_id": req.dataset_id,
        "strategy_id": (strategy or {}).get("id"),
        "selected_models": selected,
        "counts": {
            m: {
                "positives": int(sum(int(e.get(m, {}).get("pred", 0)) for e in risk_rows)),
                "total": int(len(risk_rows))
            } for m in selected
        }
    }
    risk_payload = {"summary": risk_summary, "patients": risk_rows}
    risk_path = f"{base_dir}/risk_prediction.json"
    _write_json(risk_path, risk_payload)

    # Anomaly JSON
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    ana_rows: List[Dict[str, Any]] = []
    if num_cols:
        X = df[num_cols].fillna(df[num_cols].median())
        iso = IsolationForest(n_estimators=200, random_state=42, contamination="auto")
        scores = iso.fit_predict(X)       # -1 anomaly, 1 normal
        decision = iso.decision_function(X)  # higher = more normal
        for i, (s, d) in enumerate(zip(scores, decision)):
            ana_rows.append({
                "patient_id": str(df.iloc[i].get("patient_id", i)),
                "anomaly_flag": int(s == -1),
                "anomaly_score": float(-d)
            })
    anomaly_summary = {
        "dataset_id": req.dataset_id,
        "n_anomalies": int(sum(r["anomaly_flag"] for r in ana_rows)),
        "total": int(len(ana_rows))
    }
    anomaly_payload = {"summary": anomaly_summary, "patients": ana_rows}
    anomaly_path = f"{base_dir}/anomaly_detection.json"
    _write_json(anomaly_path, anomaly_payload)

    with _get_engine().begin() as con:
        con.execute(
            text("INSERT INTO analyses (dataset_id, strategy_id, kind, artifact_path, summary) VALUES (:d,:s,'risk',:p,:sum)"),
            {"d": int(req.dataset_id), "s": (strategy or {}).get("id"), "p": risk_path, "sum": json.dumps(risk_summary)}
        )
        con.execute(
            text("INSERT INTO analyses (dataset_id, strategy_id, kind, artifact_path, summary) VALUES (:d,:s,'anomaly',:p,:sum)"),
            {"d": int(req.dataset_id), "s": (strategy or {}).get("id"), "p": anomaly_path, "sum": json.dumps(anomaly_summary)}
        )

    return {"risk_json": risk_path, "anomaly_json": anomaly_path, "summary": {"risk": risk_summary, "anomaly": anomaly_summary}}
