# app/services/prediction_service.py
from __future__ import annotations

from typing import Dict, Any, List, Optional, Iterable
import os
import json
from pathlib import Path
import glob

import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from joblib import load as _load
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# If you have a central artifacts path constant, prefer it; else default to ./artifacts
try:
    from ...paths import ARTIFACT_DIR  # type: ignore
except Exception:
    ARTIFACT_DIR = Path("artifacts")

# -------------------------
# Model groups
# -------------------------
CLASSIFICATION_MODELS = {
    "DiseaseRiskPredictor",
    "ReadmissionPredictor", "Readmission90DPredictor",
    "MortalityRiskModel", "ICUAdmissionPredictor", "SepsisEarlyWarning",
    "DiabetesComplicationRisk", "HypertensionControlPredictor",
    "HeartFailure30DRisk", "StrokeRiskPredictor", "COPDExacerbationPredictor",
    "AKIRiskPredictor", "AdverseDrugEventPredictor", "NoShowAppointmentPredictor",
}
REGRESSION_MODELS = {"LengthOfStayRegressor", "CostOfCareRegressor", "AnemiaSeverityRegressor"}


# -------------------------
# FS helpers
# -------------------------
def _safe_make_dir(path: str | Path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def _artifact_path(model_name: str) -> Optional[str]:
    """
    Resolve a model artifact path robustly.
    """
    safe = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in model_name)
    candidates = [
        ARTIFACT_DIR / "models" / f"{model_name}.joblib",
        ARTIFACT_DIR / "models" / f"{safe}.joblib",
    ]
    for p in candidates:
        if Path(p).exists():
            return str(p)
    hits = glob.glob(str(ARTIFACT_DIR / "models" / f"*{safe}*.joblib"))
    return hits[0] if hits else None


# -------------------------
# Data loading helpers
# -------------------------
def _load_all_records(engine: Engine, dataset_id: int) -> pd.DataFrame:
    with engine.begin() as con:
        df = pd.read_sql(
            text("SELECT * FROM patient_records WHERE dataset_id=:d ORDER BY id"),
            con,
            params={"d": int(dataset_id)},
        )
    if "id" in df.columns:
        df = df.drop(columns=["id"])
    return df


def _features_from_records(df: pd.DataFrame) -> pd.DataFrame:
    ID_LIKE = {"id", "dataset_id", "patient_id", "encounter_id", "timestamp", "date", "created_at", "updated_at"}
    return df.drop(columns=[c for c in ID_LIKE if c in df.columns], errors="ignore")


# -------------------------
# Column schema alignment
# -------------------------
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

    # Common meta-estimators / wrappers
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
    return [node for node in _iter_objects(model) if isinstance(node, ColumnTransformer)]


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
                sc = str(c)
                if sc not in seen:
                    seen.add(sc)
                    expected.append(sc)
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
                        sc = str(c)
                        if sc not in seen:
                            seen.add(sc)
                            expected.append(sc)
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
    return Xin[exp]


# -------------------------
# Model cache
# -------------------------
_MODEL_CACHE: dict[str, Any] = {}


def _load_model_cached(model_name: str):
    pth = _artifact_path(model_name)
    if not pth:
        raise FileNotFoundError(f"Model artifact not found: {model_name}. Train it first.")
    mdl = _MODEL_CACHE.get(pth)
    if mdl is None:
        mdl = _load(pth)
        _MODEL_CACHE[pth] = mdl
    return mdl


# -------------------------
# PUBLIC: main entry
# -------------------------
def run_predictions_for_strategy(engine: Engine, dataset_id: int, parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Batch-scoring implementation:
      * Loads each artifact once (cache).
      * Aligns features to each model's training schema.
      * Vectorized scoring (fast).
      * Handles classifiers (predict_proba or decision_function) and regressors.
      * Exports per-model summary + per-patient details + simple anomaly flags.
    """
    selected: List[str] = list(parsed.get("selected_models") or [])
    thresholds: Dict[str, float] = {str(k): float(v) for k, v in (parsed.get("thresholds") or {}).items()}

    exports_dir = ARTIFACT_DIR / "exports" / f"dataset_{dataset_id}"
    _safe_make_dir(exports_dir)

    df_all = _load_all_records(engine, dataset_id)
    if df_all.empty:
        return {"summary": "No records available for analysis", "exports": {}}

    patient_ids = df_all.get("patient_id", pd.Series([None] * len(df_all)))
    X_base = _features_from_records(df_all)

    # Load all models once
    models: Dict[str, Any] = {}
    for m in selected:
        try:
            models[m] = _load_model_cached(m)
        except Exception as e:
            models[m] = {"_load_error": str(e)}

    # Per-model vectorized outputs
    model_summaries: Dict[str, Any] = {}
    per_model_arrays: Dict[str, Dict[str, Any]] = {}

    for m in selected:
        mdl = models.get(m)
        if isinstance(mdl, dict) and "_load_error" in mdl:
            model_summaries[m] = {"error": f"model artifact not found / load error: {mdl['_load_error']}"}
            continue

        Xin = _align_X_to_model(mdl, X_base)
        try:
            if m in CLASSIFICATION_MODELS:
                if hasattr(mdl, "predict_proba"):
                    scores = np.asarray(mdl.predict_proba(Xin)[:, 1], dtype=float)
                    thr = float(thresholds.get(m, 0.5))
                    preds = (scores >= thr).astype(int)
                    per_model_arrays[m] = {"kind": "classification", "scores": scores, "preds": preds, "thr": thr}
                    model_summaries[m] = {
                        "threshold": thr,
                        "positives": int(preds.sum()),
                        "n": int(len(preds)),
                        "note": "near-constant scores" if float(np.nanstd(scores)) < 1e-12 else None,
                    }
                elif hasattr(mdl, "decision_function"):
                    # Decision scores may be any real number; keep raw scores and 0 threshold
                    scores = np.asarray(np.ravel(mdl.decision_function(Xin)), dtype=float)
                    thr = 0.0
                    preds = (scores >= thr).astype(int)
                    per_model_arrays[m] = {"kind": "classification", "scores": scores, "preds": preds, "thr": thr}
                    model_summaries[m] = {"threshold": thr, "positives": int(preds.sum()), "n": int(len(preds))}
                else:
                    model_summaries[m] = {"error": "unsupported classifier interface"}
            elif m in REGRESSION_MODELS:
                if hasattr(mdl, "predict"):
                    values = np.asarray(mdl.predict(Xin), dtype=float)
                    per_model_arrays[m] = {"kind": "regression", "values": values}
                    model_summaries[m] = {"n": int(len(values)), "mean": float(np.nanmean(values))}
                else:
                    model_summaries[m] = {"error": "unsupported regressor interface"}
            else:
                model_summaries[m] = {"error": "unknown model family"}
        except Exception as e:
            model_summaries[m] = {"error": f"prediction failure: {e}"}

    # Per-patient detail (assembled from arrays)
    patients_detail: List[Dict[str, Any]] = []
    n = len(X_base)
    for i in range(n):
        entry = {
            "patient_id": None if (i >= len(patient_ids) or pd.isna(patient_ids.iloc[i])) else str(patient_ids.iloc[i]),
            "predictions": {},
        }
        for m in selected:
            arr = per_model_arrays.get(m)
            if not arr:
                continue
            if arr["kind"] == "classification":
                entry["predictions"][m] = {
                    "score": float(arr["scores"][i]),
                    "pred": int(arr["preds"][i]),
                    "threshold": float(arr["thr"]),
                }
            elif arr["kind"] == "regression":
                entry["predictions"][m] = {"prediction": float(arr["values"][i])}
        patients_detail.append(entry)

    # Simple anomaly flags (zscore + IQR)
    anomaly_results: Dict[str, Any] = {"method": "zscore+iqr", "patients": []}
    num_cols = X_base.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        Xn = X_base[num_cols].copy()
        Xn = Xn.fillna(Xn.median())
        z = (Xn - Xn.mean()) / (Xn.std(ddof=0) + 1e-9)
        z_flag = (z.abs() > 3).any(axis=1)
        try:
            q1, q3 = Xn.quantile(0.25), Xn.quantile(0.75)
            iqr = (q3 - q1)
            low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            iqr_flag = ((Xn < low) | (Xn > high)).any(axis=1)
        except Exception:
            iqr_flag = pd.Series([False] * len(Xn), index=Xn.index)
        flagged = (z_flag | iqr_flag)
        anomaly_results["summary"] = {
            "n_flagged": int(flagged.sum()),
            "n_total": int(len(flagged)),
            "method_components": ["zscore>3", "iqr_1.5"],
        }
        anomaly_results["patients"] = [
            {
                "patient_id": None if pd.isna(patient_ids.iloc[i]) else str(patient_ids.iloc[i]),
                "zscore_any_gt3": bool(z_flag.iloc[i]),
                "iqr_outlier": bool(iqr_flag.iloc[i]),
            }
            for i in range(len(Xn)) if flagged.iloc[i]
        ]
    else:
        anomaly_results["summary"] = {"n_flagged": 0, "n_total": int(len(X_base)), "note": "no numeric columns"}

    # Write exports
    risk_results = {"models": model_summaries, "patients": patients_detail}
    exports_dir = Path(exports_dir)
    risk_path = exports_dir / "risk_prediction.json"
    anom_path = exports_dir / "anomaly_detection.json"
    _safe_make_dir(exports_dir)
    with open(risk_path, "w", encoding="utf-8") as f:
        json.dump(risk_results, f, indent=2)
    with open(anom_path, "w", encoding="utf-8") as f:
        json.dump(anomaly_results, f, indent=2)

    return {
        "summary": {
            "risk_models": list(model_summaries.keys()),
            "anomaly_flagged": anomaly_results.get("summary", {}).get("n_flagged", 0),
        },
        "exports": {"risk_prediction": str(risk_path), "anomaly_detection": str(anom_path)},
    }
