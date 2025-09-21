# -*- coding: utf-8 -*-
"""
Train all models directly via pipeline_builder and save artifacts to artifacts/models/*.joblib.
Bypasses model classes to avoid classifier/regressor mismatches.
Run:
  python -m training_data.model_training_scripts.train_all_models_full
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from training_data.utils.derive_targets import add_or_update_targets
from backend.ml_library.common.pipeline_builders import (
    train_eval_classification, train_eval_regression
)

# ---------- Paths ----------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_MODELS_DIR = PROJECT_ROOT / "artifacts" / "models"
ARTIFACT_MODELS_DIR.mkdir(parents=True, exist_ok=True)
OUTDIR = PROJECT_ROOT / "training_outputs"
OUTDIR.mkdir(parents=True, exist_ok=True)

# ---------- Task registry ----------
CLASSIFICATION_MODELS = {
    "ReadmissionPredictor": "label_readmit",
    "Readmission90DPredictor": "label_readmit",
    "MortalityRiskModel": "mortality_1y",
    "ICUAdmissionPredictor": "icu_admit",
    "SepsisEarlyWarning": "sepsis_label",
    "DiabetesComplicationRisk": "dm_complication",
    "HypertensionControlPredictor": "htn_uncontrolled",
    "HeartFailure30DRisk": "hf_30d",
    "StrokeRiskPredictor": "stroke_label",
    "COPDExacerbationPredictor": "copd_exac",
    "AKIRiskPredictor": "aki_label",
    "AdverseDrugEventPredictor": "ade_label",
    "NoShowAppointmentPredictor": "no_show",
    "DiseaseRiskPredictor": "outcome",
}
REGRESSION_MODELS = {
    "LengthOfStayRegressor": "los_days",
    "CostOfCareRegressor": "cost_of_care",
    "AnemiaSeverityRegressor": "anemia_severity_score",
}

def _safe(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-","_") else "_" for ch in name)

def _pick_estimator(model_name: str, is_classification: bool) -> str:
    m = model_name.lower()
    if is_classification:
        return "xgboost" if any(k in m for k in ("risk","sepsis","stroke","mortality","icu")) else "random_forest"
    # regression families
    return "xgboost" if "cost" in m else "random_forest"

def _coerce_binary(y: pd.Series) -> pd.Series:
    y = pd.to_numeric(y, errors="coerce")
    if y.dropna().nunique() == 2:
        return y.fillna(0).astype(int)
    thr = np.nanmedian(y)
    return (y > thr).astype(int)

def _load_data() -> pd.DataFrame:
    p = PROJECT_ROOT / "data" / "joined_training_sample.csv"
    df = pd.read_csv(p) if p.exists() else pd.read_csv(PROJECT_ROOT / "data" / "patients.csv")
    return add_or_update_targets(df)

def _save(model_name: str, pipeline, metrics: dict):
    out_path = ARTIFACT_MODELS_DIR / f"{_safe(model_name)}.joblib"
    joblib.dump(pipeline, out_path)
    with open(OUTDIR / f"{model_name}_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print(f"[OK] {model_name} -> {out_path}")

def main():
    df = _load_data()

    # --- Classification ---
    for model_name, target in CLASSIFICATION_MODELS.items():
        try:
            if target not in df.columns:
                raise ValueError(f"{model_name}: target '{target}' missing after derive_targets.")
            X = df.drop(columns=[target])
            y = _coerce_binary(df[target])
            if pd.Series(y).nunique() < 2:
                raise ValueError(f"{model_name}: y has a single class; cannot train AUC model.")
            est = _pick_estimator(model_name, True)
            metrics, pipeline = train_eval_classification(X, y, estimator=est, test_size=0.2)
            _save(model_name, pipeline, metrics)
        except Exception as e:
            with open(OUTDIR / f"{model_name}_metrics.json", "w", encoding="utf-8") as f:
                json.dump({"error": str(e)}, f, indent=2)
            print(f"[FAIL] {model_name}: {e}")

    # --- Regression ---
    for model_name, target in REGRESSION_MODELS.items():
        try:
            if target not in df.columns:
                raise ValueError(f"{model_name}: target '{target}' missing after derive_targets.")
            X = df.drop(columns=[target])
            y = pd.to_numeric(df[target], errors="coerce")
            est = _pick_estimator(model_name, False)
            metrics, pipeline = train_eval_regression(X, y, estimator=est, test_size=0.2)
            _save(model_name, pipeline, metrics)
        except Exception as e:
            with open(OUTDIR / f"{model_name}_metrics.json", "w", encoding="utf-8") as f:
                json.dump({"error": str(e)}, f, indent=2)
            print(f"[FAIL] {model_name}: {e}")

if __name__ == "__main__":
    main()
