# app/routers/analytics.py
from __future__ import annotations

from typing import Dict, Any, List, Optional, Iterable
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import os
import json
import time
from pathlib import Path
import glob

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from ..services.datasets_service import registry, load_dataframe
from ..services.analysis_service import histograms_for_columns, duckdb_query

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

import joblib
from ...paths import ARTIFACT_DIR


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
    # Use your local DSN (or read from env if you prefer)
    url = "postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
    if not url:
        raise RuntimeError("DATABASE_URL not set and no app engine found")
    return create_engine(url, future=True)


# ===========================
# Robust schema alignment
# ===========================

def _iter_objects(obj) -> Iterable:
    """Recursively yield nested estimators/transformers inside common sklearn wrappers."""
    if obj is None:
        return
    yield obj

    # Pipelines
    if hasattr(obj, "named_steps") and isinstance(getattr(obj, "named_steps"), dict):
        for step in obj.named_steps.values():
            yield from _iter_objects(step)
    if hasattr(obj, "steps") and isinstance(getattr(obj, "steps"), (list, tuple)):
        for _, step in obj.steps:
            yield from _iter_objects(step)

    # ColumnTransformer (contains transformer list)
    if hasattr(obj, "transformers"):
        for _, tr, _ in getattr(obj, "transformers"):
            yield from _iter_objects(tr)
    if hasattr(obj, "transformers_"):
        for _, tr, _ in getattr(obj, "transformers_"):
            yield from _iter_objects(tr)

    # Common meta-estimators and wrappers
    for attr in (
        "best_estimator_", "estimator", "base_estimator",
        "final_estimator", "classifier", "regressor",
        "pipeline", "preprocessor_", "model"
    ):
        if hasattr(obj, attr):
            try:
                yield from _iter_objects(getattr(obj, attr))
            except Exception:
                pass


def _all_column_transformers(model) -> List[ColumnTransformer]:
    cts: List[ColumnTransformer] = []
    for node in _iter_objects(model):
        if isinstance(node, ColumnTransformer):
            cts.append(node)
    return cts


def _expected_input_columns(model) -> Optional[List[str]]:
    """
    Return the union of ORIGINAL feature columns the ColumnTransformer(s) were fit on.
    Prefer feature_names_in_ from each CT; otherwise gather selectors from transformers_.
    """
    cts = _all_column_transformers(model)
    if not cts:
        return None

    expected: List[str] = []
    seen = set()

    for ct in cts:
        cols = getattr(ct, "feature_names_in_", None)
        if cols is not None:
            for c in list(cols):
                if c not in seen:
                    seen.add(c)
                    expected.append(str(c))
            continue

        # Fallback: collect declared selectors
        transformers = getattr(ct, "transformers_", None) or getattr(ct, "transformers", [])
        for _, _, sel in transformers:
            if sel in (None, "drop"):
                continue
            if isinstance(sel, str):
                if sel not in seen:
                    seen.add(sel)
                    expected.append(sel)
            else:
                try:
                    for c in list(sel):
                        if c not in seen:
                            seen.add(c)
                            expected.append(str(c))
                except Exception:
                    pass

    return expected or None


def _align_X_to_model(model, X: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure X contains every column the preprocessor expects; add missing as NaN
    and order columns to match fit-time schema. Extra columns are ignored.
    """
    exp = _expected_input_columns(model)
    if not exp:
        return X  # no CT found; use as-is

    Xin = X.copy()
    for c in exp:
        if c not in Xin.columns:
            Xin[c] = np.nan
    # Order & restrict to expected schema
    return Xin[exp]


# ===========================
# DB & dataset helpers
# ===========================

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
    name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in model_name)
    candidates = [
        ARTIFACT_DIR / "models" / f"{model_name}.joblib",
        ARTIFACT_DIR / "models" / f"{name}.joblib",
    ]
    for p in candidates:
        if Path(p).exists():
            return str(p)
    hits = glob.glob(str(ARTIFACT_DIR / "models" / f"*{name}*.joblib"))
    return hits[0] if hits else None


# ---- model cache: load artifacts once per process (or per request) ----
_MODEL_CACHE: dict[str, Any] = {}


def _load_model_cached(model_name: str):
    pth = _artifact_path(model_name)
    if not pth:
        raise FileNotFoundError(f"Model artifact not found: {model_name}. Train it first.")
    mdl = _MODEL_CACHE.get(pth)
    if mdl is None:
        mdl = joblib.load(pth)
        _MODEL_CACHE[pth] = mdl
    return mdl


def _predict_with_model(model_name: str, X: pd.DataFrame, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Single-row convenience used by /adhoc/predict. Uses the cache.
    """
    model = _load_model_cached(model_name)

    # Ensure columns/ordering match the training schema
    Xin = _align_X_to_model(model, X)

    # Classification
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(Xin)[:, 1]
        prob = float(proba[0])
        return {"score": prob, "pred": int(prob >= threshold), "threshold": threshold, "source": "model"}

    # Fall back to decision_function if available
    if hasattr(model, "decision_function"):
        score = float(np.ravel(model.decision_function(Xin))[0])
        return {"score": score, "pred": int(score >= 0.0), "threshold": 0.0, "source": "model:decision_function"}

    # Regression
    if hasattr(model, "predict"):
        val = float(np.ravel(model.predict(Xin))[0])
        return {"prediction": val, "source": "model"}

    raise TypeError(f"{model_name}: loaded artifact supports neither predict_proba, decision_function, nor predict.")


def _bulk_predict_one(model_name: str, model, X_df: pd.DataFrame, threshold: float) -> Dict[str, Any]:
    """
    Vectorized scoring for one model across the full dataframe.
    Returns a dict describing classification or regression outputs.
    """
    Xin = _align_X_to_model(model, X_df)

    # Classification path
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(Xin)[:, 1]
        preds = (proba >= float(threshold)).astype(int)
        return {
            "kind": "classification",
            "scores": proba.astype(float),
            "preds": preds.astype(int),
            "threshold": float(threshold),
            "note": "constant_predictions" if float(np.nanstd(proba)) < 1e-12 else None,
        }

    # Regression path
    if hasattr(model, "predict"):
        vals = model.predict(Xin)
        return {
            "kind": "regression",
            "values": np.asarray(vals, dtype=float),
        }

    return {"kind": "error", "error": "unsupported model interface"}


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

    # -------- Vectorized scoring per model (FAST) --------
    # Load each model once
    models = {m: _load_model_cached(m) for m in selected}

    # Score per model across the full dataframe
    per_model_outputs: Dict[str, Dict[str, Any]] = {}
    for m in selected:
        th = float(thresholds.get(m, 0.5))
        try:
            per_model_outputs[m] = _bulk_predict_one(m, models[m], df, th)
        except Exception as e:
            per_model_outputs[m] = {"kind": "error", "error": str(e)}

    # Build per-patient rows from bulk arrays
    risk_rows: List[Dict[str, Any]] = []
    n = len(df)
    for i in range(n):
        entry = {"patient_id": str(df.iloc[i].get("patient_id", i))}
        for m in selected:
            out = per_model_outputs.get(m, {"kind": "error", "error": "missing"})
            if out.get("kind") == "classification":
                score = float(out["scores"][i])
                pred = int(out["preds"][i])
                entry[m] = {
                    "score": score,
                    "pred": pred,
                    "threshold": float(thresholds.get(m, 0.5)),
                    "source": "model",
                }
            elif out.get("kind") == "regression":
                entry[m] = {"prediction": float(out["values"][i]), "source": "model"}
            else:
                entry[m] = {"error": out.get("error", "prediction failure")}
        risk_rows.append(entry)

    # Summary (handle classifiers & regressors)
    risk_summary: Dict[str, Any] = {
        "dataset_id": req.dataset_id,
        "strategy_id": (strategy or {}).get("id"),
        "selected_models": selected,
        "counts": {},
    }
    for m in selected:
        out = per_model_outputs.get(m, {})
        if out.get("kind") == "classification":
            positives = int(np.sum(out["preds"])) if "preds" in out else 0
            risk_summary["counts"][m] = {"positives": positives, "total": int(n)}
        elif out.get("kind") == "regression":
            mean_pred = float(np.mean(out["values"])) if "values" in out else None
            risk_summary["counts"][m] = {"n": int(n), "mean_prediction": mean_pred}
        else:
            risk_summary["counts"][m] = {"error": out.get("error", "prediction failure")}

    risk_payload = {"summary": risk_summary, "patients": risk_rows}
    risk_path = f"{base_dir}/risk_prediction.json"
    _write_json(risk_path, risk_payload)

    # -------- Anomaly JSON --------
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    ana_rows: List[Dict[str, Any]] = []
    if num_cols:
        X = df[num_cols].fillna(df[num_cols].median())
        iso = IsolationForest(n_estimators=200, random_state=42, contamination="auto")
        scores = iso.fit_predict(X)          # -1 anomaly, 1 normal
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
            text("INSERT INTO analyses (dataset_id, strategy_id, kind, artifact_path, summary) "
                 "VALUES (:d,:s,'risk',:p,:sum)"),
            {"d": int(req.dataset_id), "s": (strategy or {}).get("id"), "p": risk_path,
             "sum": json.dumps(risk_summary)}
        )
        con.execute(
            text("INSERT INTO analyses (dataset_id, strategy_id, kind, artifact_path, summary) "
                 "VALUES (:d,:s,'anomaly',:p,:sum)"),
            {"d": int(req.dataset_id), "s": (strategy or {}).get("id"), "p": anomaly_path,
             "sum": json.dumps(anomaly_summary)}
        )

    return {
        "risk_json": risk_path,
        "anomaly_json": anomaly_path,
        "summary": {"risk": risk_summary, "anomaly": anomaly_summary},
    }
