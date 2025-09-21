from __future__ import annotations
import os
import json
import uuid
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd

# file registry compatibility
from ..services.datasets_service import registry, load_dataframe, ensure_data_dir
from ..services.analysis_service import dataframe_overview, head_sample

# DB plumbing
import os as _os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# ---- strategy helper (singular: strategy.py) ----
try:
    from .strategies import create_and_store_strategy  # async
except Exception:
    from .strategies import create_and_store_strategy  # type: ignore

# optional column normalization
try:
    from ...ai_services.column_mapper import map_columns  # type: ignore
except Exception:
    def map_columns(df: pd.DataFrame) -> pd.DataFrame:
        return df

# try to use your database.py engine if present
try:
    from ...database import engine as _app_engine  # type: ignore
except Exception:
    _app_engine = None

router = APIRouter(prefix="/datasets", tags=["datasets"])
# add with other imports
from sqlalchemy import inspect

def _has_records(engine: Engine, dataset_id: int) -> bool:
    with engine.begin() as con:
        n = con.execute(
            text("SELECT COUNT(*) FROM patient_records WHERE dataset_id=:d"),
            {"d": int(dataset_id)}
        ).scalar_one()
    return int(n) > 0

def _load_registry_df(dataset_id: str | int) -> Optional[pd.DataFrame]:
    try:
        ds = registry.get(str(dataset_id))
        if ds:
            return load_dataframe(registry.path_for(str(dataset_id)))
    except Exception:
        pass
    return None
def _only_scalar_columns(df: pd.DataFrame) -> pd.DataFrame:
    keep = []
    for c in df.columns:
        if c in ("id", "payload"):  # always drop these for summaries
            continue
        try:
            sample = df[c].dropna().head(25).tolist()
            if any(isinstance(v, (dict, list, set)) for v in sample):
                continue
            keep.append(c)
        except Exception:
            # if anything smells weird, skip the column from overview
            continue
    return df[keep]

# ---------- DB helpers ----------
def _get_engine() -> Engine:
    if _app_engine is not None:
        return _app_engine
    url = _os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set and no app engine found")
    return create_engine(url, future=True)

DDL = """
CREATE TABLE IF NOT EXISTS datasets (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  n_rows INT,
  n_cols INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS patient_records (
  id BIGSERIAL PRIMARY KEY,
  dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
  patient_id TEXT,
  age INT,
  sex TEXT,
  bmi DOUBLE PRECISION,
  systolic_bp DOUBLE PRECISION,
  diastolic_bp DOUBLE PRECISION,
  heart_rate DOUBLE PRECISION,
  respiratory_rate DOUBLE PRECISION,
  temperature DOUBLE PRECISION,
  spo2 DOUBLE PRECISION,
  glucose DOUBLE PRECISION,
  hba1c DOUBLE PRECISION,
  creatinine DOUBLE PRECISION,
  egfr DOUBLE PRECISION,
  sodium DOUBLE PRECISION,
  potassium DOUBLE PRECISION,
  wbc DOUBLE PRECISION,
  hemoglobin DOUBLE PRECISION,
  platelet DOUBLE PRECISION,
  smoking_status TEXT,
  diabetes_history BOOLEAN,
  hypertension_history BOOLEAN,
  heart_failure_history BOOLEAN,
  copd_history BOOLEAN,
  stroke_history BOOLEAN,
  medications TEXT,
  encounter_date DATE,
  payload JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pr_dataset ON patient_records(dataset_id);
CREATE INDEX IF NOT EXISTS idx_pr_patient ON patient_records(patient_id);
"""

def _ensure_tables(engine: Engine) -> None:
    with engine.begin() as con:
        for stmt in filter(None, DDL.split(";")):
            st = stmt.strip()
            if st:
                con.execute(text(st + ";"))

def _register_dataset(engine: Engine, name: str, n_rows: int, n_cols: int) -> int:
    q = text("INSERT INTO datasets (name, n_rows, n_cols) VALUES (:name, :r, :c) RETURNING id")
    with engine.begin() as con:
        dsid = con.execute(q, {"name": name, "r": int(n_rows), "c": int(n_cols)}).scalar_one()
    return int(dsid)

def _insert_records(engine: Engine, dataset_id: int, df: pd.DataFrame) -> int:
    """
    Robust bulk insert using psycopg2.extras.execute_values (handles JSONB cleanly).
    Falls back to pandas.to_sql if psycopg2 is not available.
    """
    modeled_cols = {
        "patient_id","age","sex","bmi","systolic_bp","diastolic_bp","heart_rate",
        "respiratory_rate","temperature","spo2","glucose","hba1c","creatinine","egfr",
        "sodium","potassium","wbc","hemoglobin","platelet","smoking_status",
        "diabetes_history","hypertension_history","heart_failure_history",
        "copd_history","stroke_history","medications","encounter_date"
    }

    df = df.copy()

    # normalize booleans
    for bcol in ["diabetes_history","hypertension_history","heart_failure_history","copd_history","stroke_history"]:
        if bcol in df.columns:
            df[bcol] = df[bcol].map(lambda v: bool(v) if pd.notna(v) else None)

    # normalize date
    if "encounter_date" in df.columns:
        df["encounter_date"] = pd.to_datetime(df["encounter_date"], errors="coerce").dt.date

    # add missing modeled cols
    for c in modeled_cols:
        if c not in df.columns:
            df[c] = None

    df["dataset_id"] = dataset_id

    ordered = [
        "dataset_id","patient_id","age","sex","bmi","systolic_bp","diastolic_bp",
        "heart_rate","respiratory_rate","temperature","spo2","glucose","hba1c",
        "creatinine","egfr","sodium","potassium","wbc","hemoglobin","platelet",
        "smoking_status","diabetes_history","hypertension_history","heart_failure_history",
        "copd_history","stroke_history","medications","encounter_date","payload"
    ]

    # build payload = extra columns (drop NaN)
    payloads = []
    extra_cols = [c for c in df.columns if c not in modeled_cols and c not in ("dataset_id","payload")]
    for _, row in df.iterrows():
        extra = {k: row[k] for k in extra_cols}
        payload = {k: (None if pd.isna(v) else v) for k, v in extra.items()}
        payloads.append(payload if payload else None)
    df["payload"] = payloads

    # try psycopg2 fast path
    try:
        from psycopg2.extras import execute_values, Json  # type: ignore

        rows = []
        for tup in df[ordered].itertuples(index=False, name=None):
            # replace dict payload with Json wrapper (or None)
            tup = list(tup)
            tup[-1] = Json(tup[-1]) if tup[-1] is not None else None
            rows.append(tuple(tup))

        sql = """
            INSERT INTO patient_records (
                dataset_id, patient_id, age, sex, bmi, systolic_bp, diastolic_bp,
                heart_rate, respiratory_rate, temperature, spo2, glucose, hba1c,
                creatinine, egfr, sodium, potassium, wbc, hemoglobin, platelet,
                smoking_status, diabetes_history, hypertension_history, heart_failure_history,
                copd_history, stroke_history, medications, encounter_date, payload
            )
            VALUES %s
        """
        with engine.raw_connection() as raw:
            cur = raw.cursor()
            execute_values(cur, sql, rows, page_size=10_000)
            raw.commit()
        return len(rows)

    except Exception:
        # fallback: to_sql with explicit JSON -> text
        try:
            from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
            dtype = {"payload": JSONB}
        except Exception:
            dtype = None  # let pandas decide

        df_sql = df[ordered].copy()
        # make sure payload is a JSON string or dict (pandas + psycopg2 will adapt)
        return int(
            df_sql.to_sql(
                "patient_records",
                engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=10_000,
                dtype=dtype,
            )
            or len(df_sql)
        )


# ---------- simple local analysis runner (by strategy) ----------
CLASSIFICATION_MODELS = {
    "DiseaseRiskPredictor",
    "ReadmissionPredictor", "Readmission90DPredictor",
    "MortalityRiskModel", "ICUAdmissionPredictor", "SepsisEarlyWarning",
    "DiabetesComplicationRisk", "HypertensionControlPredictor",
    "HeartFailure30DRisk", "StrokeRiskPredictor", "COPDExacerbationPredictor",
    "AKIRiskPredictor", "AdverseDrugEventPredictor", "NoShowAppointmentPredictor",
}
REGRESSION_MODELS = {"LengthOfStayRegressor", "CostOfCareRegressor", "AnemiaSeverityRegressor"}

def _safe_make_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def _load_all_records(engine: Engine, dataset_id: int) -> pd.DataFrame:
    with engine.begin() as con:
        df = pd.read_sql(
            text("SELECT * FROM patient_records WHERE dataset_id=:d ORDER BY id"),
            con, params={"d": int(dataset_id)}
        )
    return df

def _features_from_records(df: pd.DataFrame) -> pd.DataFrame:
    drop_cols = {"id", "dataset_id"}
    return df.drop(columns=[c for c in drop_cols if c in df.columns])

def _run_predictions_for_strategy(engine: Engine, dataset_id: int, parsed: Dict[str, Any]) -> Dict[str, Any]:
    selected = parsed.get("selected_models") or []
    thresholds = parsed.get("thresholds") or {}
    exports_dir = os.path.join("artifacts", "exports", f"dataset_{dataset_id}")
    _safe_make_dir(exports_dir)

    df_all = _load_all_records(engine, dataset_id)
    if df_all.empty:
        return {"summary": "No records available for analysis", "exports": {}}

    patient_ids = df_all.get("patient_id", pd.Series([None] * len(df_all)))
    X = _features_from_records(df_all)

    risk_results: Dict[str, Any] = {"models": {}, "patients": []}
    anomaly_results: Dict[str, Any] = {"method": "zscore+iqr", "patients": []}

    from joblib import load as _load
    for m in selected:
        model_path = os.path.join("artifacts", "models", f"{m}.joblib")
        if not os.path.exists(model_path):
            risk_results["models"][m] = {"error": "model artifact not found"}
            continue

        try:
            model = _load(model_path)
            if m in CLASSIFICATION_MODELS and hasattr(model, "predict_proba"):
                prob = model.predict_proba(X)[:, 1]
                thr = float(thresholds.get(m, 0.5))
                pred = (prob >= thr).astype(int)
                risk_results["models"][m] = {
                    "threshold": thr,
                    "positives": int(pred.sum()),
                    "n": int(len(pred))
                }
            elif m in REGRESSION_MODELS and hasattr(model, "predict"):
                val = model.predict(X)
                risk_results["models"][m] = {"n": int(len(val)), "mean": float(pd.Series(val).mean())}
            else:
                risk_results["models"][m] = {"error": "unsupported model interface"}
        except Exception as e:
            risk_results["models"][m] = {"error": f"prediction failure: {e}"}

    # per-patient predictions
    per_patient: List[Dict[str, Any]] = []
    for i in range(len(X)):
        entry = {"patient_id": None if pd.isna(patient_ids.iloc[i]) else str(patient_ids.iloc[i]), "predictions": {}}
        for m in selected:
            model_path = os.path.join("artifacts", "models", f"{m}.joblib")
            if not os.path.exists(model_path):
                continue
            try:
                model = _load(model_path)
                if m in CLASSIFICATION_MODELS and hasattr(model, "predict_proba"):
                    score = float(model.predict_proba(X.iloc[[i]])[:, 1][0])
                    thr = float(thresholds.get(m, 0.5))
                    entry["predictions"][m] = {"score": score, "pred": int(score >= thr), "threshold": thr}
                elif m in REGRESSION_MODELS and hasattr(model, "predict"):
                    pred = float(model.predict(X.iloc[[i]])[0])
                    entry["predictions"][m] = {"prediction": pred}
            except Exception:
                continue
        per_patient.append(entry)
    risk_results["patients"] = per_patient

    # anomaly detector
    num_cols = X.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        z = (X[num_cols] - X[num_cols].mean()) / (X[num_cols].std(ddof=0) + 1e-9)
        z_abs = z.abs()
        z_flag = (z_abs > 3).any(axis=1)

        try:
            q1 = X[num_cols].quantile(0.25)
            q3 = X[num_cols].quantile(0.75)
            iqr = (q3 - q1)
            low = q1 - 1.5 * iqr
            high = q3 + 1.5 * iqr
            iqr_flag = ((X[num_cols] < low) | (X[num_cols] > high)).any(axis=1)
            flagged = (z_flag | iqr_flag)
            method_components = ["zscore>3", "iqr_1.5"]
        except Exception:
            flagged = z_flag
            method_components = ["zscore>3"]

        anomaly_results["summary"] = {
            "n_flagged": int(flagged.sum()),
            "n_total": int(len(flagged)),
            "method_components": method_components
        }
        anomaly_patients: List[Dict[str, Any]] = []
        for i, is_anom in enumerate(flagged.tolist()):
            if is_anom:
                anomaly_patients.append({
                    "patient_id": None if pd.isna(patient_ids.iloc[i]) else str(patient_ids.iloc[i]),
                    "zscore_any_gt3": bool(z_flag.iloc[i]),
                })
        anomaly_results["patients"] = anomaly_patients
    else:
        anomaly_results["summary"] = {"n_flagged": 0, "n_total": int(len(X)), "note": "no numeric columns"}

    # exports
    exports_dir = os.path.join("artifacts", "exports", f"dataset_{dataset_id}")
    _safe_make_dir(exports_dir)
    risk_path = os.path.join(exports_dir, "risk_prediction.json")
    anom_path = os.path.join(exports_dir, "anomaly_detection.json")
    with open(risk_path, "w", encoding="utf-8") as f:
        json.dump(risk_results, f, indent=2)
    with open(anom_path, "w", encoding="utf-8") as f:
        json.dump(anomaly_results, f, indent=2)

    return {
        "summary": {
            "risk_models": list(risk_results["models"].keys()),
            "anomaly_flagged": anomaly_results.get("summary", {}).get("n_flagged", 0),
        },
        "exports": {
            "risk_prediction": risk_path,
            "anomaly_detection": anom_path
        }
    }

# ---------- Routes ----------
@router.get("")
def list_datasets() -> Dict[str, Any]:
    """
    Return ONLY canonical DB datasets (plus file registry as 'source':'file').
    Frontend should use the 'id' from the DB rows for /datasets/{id}.
    """
    out: List[Dict[str, Any]] = []
    # DB datasets
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        with eng.begin() as con:
            rows = con.execute(
                text("SELECT id, name, n_rows, n_cols, created_at FROM datasets ORDER BY id DESC")
            ).mappings().all()
            for r in rows:
                item = dict(r)
                item["source"] = "db"
                out.append(item)
    except Exception:
        pass

    # file-registry references (secondary)
    try:
        files = registry.list()
        for f in files:
            f = dict(f)
            f["source"] = "file_registry"
            out.append(f)
    except Exception:
        pass

    return {"datasets": out}

@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None)
) -> Dict[str, Any]:
    ensure_data_dir()
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty file.")

    original_name = file.filename or f"dataset_{uuid.uuid4().hex}"
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in [".csv", ".parquet", ".pq", ".feather", ".xlsx"]:
        ext = ".csv"
    safe_name = (name or os.path.splitext(original_name)[0]).strip() or f"dataset_{uuid.uuid4().hex}"

    fname = f"{safe_name}{ext}"
    path = os.path.join(registry.data_dir, fname)
    with open(path, "wb") as f:
        f.write(raw)

    try:
        df = load_dataframe(path)
    except Exception as e:
        try:
            os.remove(path)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e}")

    try:
        df = map_columns(df)
    except Exception:
        pass

    n_rows, n_cols = int(len(df)), int(len(df.columns))

    # ---- DB ingest ----
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        dataset_id = _register_dataset(eng, safe_name, n_rows, n_cols)
        inserted = _insert_records(eng, dataset_id, df)
        if inserted == 0:
            raise HTTPException(status_code=500, detail="No rows were inserted into patient_records")

    except Exception as e:
        # If DB fails, tell the UI clearly and stop (to avoid phantom IDs)
        ds_file = registry.add_from_path(path, name=safe_name)
        return {
            "dataset": {
                "id": None,
                "name": safe_name,
                "n_rows": n_rows,
                "n_cols": n_cols,
                "ingest": "file_only",
                "file_registry_id": ds_file.get("id"),
                "warning": f"DB ingest failed: {e}"
            }
        }

    # also register in file registry (non-blocking)
    try:
        ds_file = registry.add_from_path(path, name=safe_name)
    except Exception:
        ds_file = {"id": None}

    # ADD THIS RETURN STATEMENT:
    return {
        "dataset": {
            "id": dataset_id,
            "name": safe_name,
            "n_rows": n_rows,
            "n_cols": n_cols,
            "ingest": "postgres",
            "file_registry_id": ds_file.get("id"),
        }
    }

@router.get("/debug")
def _debug_list_db() -> Dict[str, Any]:
    """Quick DB view to confirm uploaded datasets actually exist."""
    eng = _get_engine()
    _ensure_tables(eng)
    with eng.begin() as con:
        rows = con.execute(text("SELECT id, name, n_rows, n_cols, created_at FROM datasets ORDER BY id DESC")).mappings().all()
    return {"db_datasets": [dict(r) for r in rows]}

@router.get("/{dataset_id}")
def get_dataset(dataset_id: str) -> Dict[str, Any]:
    # DB first
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        with eng.begin() as con:
            row = con.execute(
                text("SELECT id, name, n_rows, n_cols, created_at FROM datasets WHERE id=:id"),
                {"id": int(dataset_id)}
            ).mappings().first()
            if row:
                out = dict(row)
                out["source"] = "db"
                return {"dataset": out}
    except Exception:
        pass

    # registry fallback
    ds = registry.get(dataset_id)
    if ds:
        ds = dict(ds)
        ds["source"] = "file_registry"
        return {"dataset": ds}

    raise HTTPException(status_code=404, detail="Dataset not found")

@router.get("/{dataset_id}/columns")
def dataset_columns(dataset_id: str) -> Dict[str, Any]:
    # prefer DB schema
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        with eng.begin() as con:
            q = text("SELECT * FROM patient_records WHERE dataset_id=:d LIMIT 1")
            row = con.execute(q, {"d": int(dataset_id)}).mappings().first()
            if row:
                rec = dict(row)
                # drop id/payload and any non-scalar
                cols = []
                for k, v in list(rec.items()):
                    if k == "id" or k == "payload":
                        continue
                    if isinstance(v, (dict, list, set)):
                        continue
                    cols.append({"name": k, "dtype": type(v).__name__})
                return {"columns": cols, "rows": _count_rows(eng, dataset_id)}
    except Exception:
        pass

    # fallback to file
    ds = registry.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = load_dataframe(registry.path_for(dataset_id))
    df = _only_scalar_columns(df)
    cols = [{"name": c, "dtype": str(df[c].dtype)} for c in df.columns]
    return {"columns": cols, "rows": len(df)}

def _count_rows(engine: Engine, dataset_id: int) -> int:
    with engine.begin() as con:
        n = con.execute(text("SELECT COUNT(*) FROM patient_records WHERE dataset_id=:d"), {"d": int(dataset_id)}).scalar_one()
    return int(n)

@router.get("/{dataset_id}/summary")
def dataset_summary(dataset_id: str) -> Dict[str, Any]:
    df: Optional[pd.DataFrame] = None
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        with eng.begin() as con:
            df = pd.read_sql(
                text("SELECT * FROM patient_records WHERE dataset_id=:d"),
                con, params={"d": int(dataset_id)}
            )
        # drop internal / non-scalar columns for overview
        if "id" in df.columns:
            df = df.drop(columns=["id"])
        df = _only_scalar_columns(df)
    except Exception:
        pass

    if df is None or df.empty:
        ds = registry.get(dataset_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Dataset not found")
        df = load_dataframe(registry.path_for(dataset_id))
        df = _only_scalar_columns(df)

    meta, numeric, categorical = dataframe_overview(df)
    sample = head_sample(df, limit=10)
    return {"meta": meta, "numeric": numeric, "categorical": categorical, "sample": sample}

@router.get("/{dataset_id}/sample")
def dataset_sample(dataset_id: str, limit: int = 50) -> Dict[str, Any]:
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        with eng.begin() as con:
            df = pd.read_sql(
                text("SELECT * FROM patient_records WHERE dataset_id=:d LIMIT :lim"),
                con, params={"d": int(dataset_id), "lim": int(limit)}
            )
        if "id" in df.columns:
            df = df.drop(columns=["id"])
        # keep a readable preview; convert dict/list to JSON strings
        for c in list(df.columns):
            if c == "payload":
                df = df.drop(columns=[c])
                continue
            if df[c].map(lambda v: isinstance(v, (dict, list, set))).any():
                df[c] = df[c].map(lambda v: json.dumps(v, default=str))
        return {"rows": df.to_dict(orient="records")}
    except Exception:
        pass

    ds = registry.get(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = load_dataframe(registry.path_for(dataset_id))
    df = _only_scalar_columns(df)
    return {"rows": head_sample(df, limit=limit)}
@router.post("/{dataset_id}/backfill")
def backfill_patient_records(dataset_id: str) -> Dict[str, Any]:
    df = _load_registry_df(dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="No source file found in registry to backfill from.")
    try:
        eng = _get_engine()
        _ensure_tables(eng)
        inserted = _insert_records(eng, int(dataset_id), df)
        return {"dataset_id": int(dataset_id), "inserted": int(inserted)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backfill failed: {e}")
