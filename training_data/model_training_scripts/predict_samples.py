
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Predict sample outputs using saved pipelines.
See header in this file for usage examples.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

DEFAULT_INPUT = ROOT / "data" / "joined_training_sample.csv"
MODELS_DIRS = [ROOT / "artifacts" / "models", ROOT / "training_outputs"]
METRICS_DIR = ROOT / "training_outputs"

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

def find_model_path(name: str):
    for d in MODELS_DIRS:
        for fname in (f"{name}.joblib", f"{name}_model.joblib"):
            p = Path(d) / fname
            if p.exists():
                return p
    return None

def find_threshold(name: str, default=0.5) -> float:
    mf = METRICS_DIR / f"{name}_metrics.json"
    if mf.exists():
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
            return float(m.get("train_best_threshold", default))
        except Exception:
            return default
    return default

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=str, default=str(DEFAULT_INPUT), help="Input CSV path")
    ap.add_argument("--out", type=str, default="predictions_sample.csv", help="Output CSV path")
    ap.add_argument("--n", type=int, default=5, help="Number of rows to score if --ids not passed")
    ap.add_argument("--ids", type=str, default="", help="Comma-separated patient_id values to score")
    ap.add_argument("--only", type=str, default="", help="Comma-separated model names to run")
    ap.add_argument("--random", action="store_true", help="Sample random N rows instead of head(N)")
    return ap.parse_args()

def main():
    args = parse_args()
    data_path = Path(args.input)
    assert data_path.exists(), f"Input not found: {data_path}"

    df = pd.read_csv(data_path)
    if "patient_id" not in df.columns:
        df["patient_id"] = np.arange(len(df)).astype(str)

    # Select rows
    if args.ids:
        ids = [s.strip() for s in args.ids.split(",") if s.strip()]
        sub = df[df["patient_id"].astype(str).isin(ids)].copy()
        if sub.empty:
            raise SystemExit(f"No matching rows for patient_id in {ids}")
    else:
        sub = df.sample(args.n, random_state=42) if args.random else df.head(args.n).copy()

    only = set([s.strip() for s in args.only.split(",") if s.strip()])
    do_clf = {m:t for m,t in CLASSIFICATION_MODELS.items() if (not only or m in only)}
    do_reg = {m:t for m,t in REGRESSION_MODELS.items() if (not only or m in only)}

    out_rows = []
    for i, row in sub.iterrows():
        rec = {"patient_id": row.get("patient_id", str(i))}
        row_df = pd.DataFrame([row])

        for model_name, target in do_clf.items():
            model_path = find_model_path(model_name)
            if not model_path:
                rec[f"{model_name}_err"] = "model_missing"; continue
            pipe = joblib.load(model_path)
            X = row_df.drop(columns=[c for c in [target] if c in row_df.columns])
            try:
                if hasattr(pipe, "predict_proba"):
                    prob = float(pipe.predict_proba(X)[0, -1])
                else:
                    score = float(pipe.decision_function(X)[0])
                    prob = 1.0 / (1.0 + np.exp(-score))
            except Exception as e:
                rec[f"{model_name}_err"] = f"infer:{e}"; continue
            thr = find_threshold(model_name, default=0.5)
            rec[f"{model_name}_proba"] = round(prob, 6)
            rec[f"{model_name}_thr"]   = round(thr, 4)
            rec[f"{model_name}_pred"]  = int(prob >= thr)

        for model_name, target in do_reg.items():
            model_path = find_model_path(model_name)
            if not model_path:
                rec[f"{model_name}_err"] = "model_missing"; continue
            pipe = joblib.load(model_path)
            X = row_df.drop(columns=[c for c in [target] if c in row_df.columns])
            try:
                val = float(pipe.predict(X)[0])
                rec[f"{model_name}_pred"] = round(val, 4)
            except Exception as e:
                rec[f"{model_name}_err"] = f"infer:{e}"; continue

        out_rows.append(rec)

    out_df = pd.DataFrame(out_rows)
    out_path = Path(args.out)
    out_df.to_csv(out_path, index=False)
    print(f"Wrote {len(out_df)} predictions to: {out_path.resolve()}")
    with pd.option_context("display.max_columns", 200):
        print(out_df.head(min(10, len(out_df))).to_string(index=False))

if __name__ == "__main__":
    main()
