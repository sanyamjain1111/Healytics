
import json, sys, math
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.metrics import (
    roc_auc_score, average_precision_score, f1_score, accuracy_score,
    precision_score, recall_score, r2_score, mean_squared_error
)
from sklearn.model_selection import train_test_split
import joblib

# --- Config ---
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "joined_training_sample.csv"
MODELS_DIRS = [ROOT / "artifacts" / "models", ROOT / "training_outputs"]
METRICS_DIR = ROOT / "training_outputs"
OUT_SUMMARY_CSV = ROOT / "training_outputs" / "verification_summary.csv"
OUT_SUMMARY_JSON = ROOT / "training_outputs" / "verification_summary.json"

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
        # try both <name>.joblib and <name>_model.joblib
        for fname in [f"{name}.joblib", f"{name}_model.joblib"]:
            p = d / fname
            if p.exists():
                return p
    return None

def find_metrics_path(name: str):
    p = METRICS_DIR / f"{name}_metrics.json"
    return p if p.exists() else None

def safe_auc(y_true, y_score):
    try:
        if len(np.unique(y_true)) < 2:
            return float("nan")
        return roc_auc_score(y_true, y_score)
    except Exception:
        return float("nan")

def main():
    assert DATA.exists(), f"Dataset not found: {DATA}"
    df = pd.read_csv(DATA)
    summaries = []

    # --- Verify classifiers ---
    for model_name, target in CLASSIFICATION_MODELS.items():
        model_path = find_model_path(model_name)
        metrics_path = find_metrics_path(model_name)

        row = {"model": model_name, "type": "classification", "target": target}
        row["model_file"] = str(model_path) if model_path else ""
        row["metrics_file"] = str(metrics_path) if metrics_path else ""

        try:
            if target not in df.columns:
                row["status"] = "FAIL"
                row["reason"] = f"Target '{target}' missing in dataset"
                summaries.append(row); continue

            X = df.drop(columns=[target])
            y = pd.to_numeric(df[target], errors="coerce").fillna(0).astype(int)

            # metrics.json on disk
            if metrics_path:
                try:
                    m = json.loads(Path(metrics_path).read_text())
                    for k,v in m.items():
                        if isinstance(v, (int,float,str)):
                            row[f"train_{k}"] = v
                except Exception as e:
                    row["metrics_read_error"] = str(e)

            # load model
            if model_path:
                pipe = joblib.load(model_path)
                # Smoke inference on head (predict + proba)
                yhat = pipe.predict(X.head(64))
                row["smoke_pred_mean"] = float(np.mean(yhat))
                if hasattr(pipe, "predict_proba"):
                    proba = pipe.predict_proba(X.head(64))[:, -1]
                    row["smoke_proba_mean"] = float(np.mean(proba))

                # Small holdout for recomputed metrics
                Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
                # Use the trained pipeline directly (no refit)
                yh = pipe.predict(Xte)
                row["hold_f1"] = float(f1_score(yte, yh, zero_division=0))
                row["hold_acc"] = float(accuracy_score(yte, yh))
                if hasattr(pipe, "predict_proba"):
                    ys = pipe.predict_proba(Xte)[:, -1]
                    row["hold_auc"] = float(safe_auc(yte, ys))
                    row["hold_ap"] = float(average_precision_score(yte, ys))

                # Heuristic pass/fail
                row["status"] = "PASS" if (not math.isnan(row.get("hold_auc", float("nan"))) and row.get("hold_auc", 0) >= 0.60) else "WARN"
            else:
                row["status"] = "FAIL"
                row["reason"] = "Model file not found"

        except Exception as e:
            row["status"] = "FAIL"
            row["reason"] = str(e)
        summaries.append(row)

    # --- Verify regressors ---
    for model_name, target in REGRESSION_MODELS.items():
        model_path = find_model_path(model_name)
        metrics_path = find_metrics_path(model_name)

        row = {"model": model_name, "type": "regression", "target": target}
        row["model_file"] = str(model_path) if model_path else ""
        row["metrics_file"] = str(metrics_path) if metrics_path else ""

        try:
            if target not in df.columns:
                row["status"] = "FAIL"
                row["reason"] = f"Target '{target}' missing in dataset"
                summaries.append(row); continue

            X = df.drop(columns=[target])
            y = pd.to_numeric(df[target], errors="coerce")

            if metrics_path:
                try:
                    m = json.loads(Path(metrics_path).read_text())
                    for k,v in m.items():
                        if isinstance(v, (int,float,str)):
                            row[f"train_{k}"] = v
                except Exception as e:
                    row["metrics_read_error"] = str(e)

            if model_path:
                pipe = joblib.load(model_path)
                # Smoke inference
                yh = pipe.predict(X.head(64))
                row["smoke_pred_mean"] = float(np.mean(yh))

                # Holdout quality
                Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
                ypred = pipe.predict(Xte)
                row["hold_r2"] = float(r2_score(yte, ypred))
                row["hold_rmse"] = float(np.sqrt(mean_squared_error(yte, ypred)))
                row["status"] = "PASS" if row["hold_r2"] >= 0.10 else "WARN"
            else:
                row["status"] = "FAIL"
                row["reason"] = "Model file not found"

        except Exception as e:
            row["status"] = "FAIL"
            row["reason"] = str(e)
        summaries.append(row)

    # Save results
    df_sum = pd.DataFrame(summaries)
    df_sum.to_csv(OUT_SUMMARY_CSV, index=False)
    Path(OUT_SUMMARY_JSON).write_text(json.dumps(summaries, indent=2))

    # Pretty print minimal view
    view = df_sum[[c for c in df_sum.columns if c in ("model","type","target","status","hold_auc","hold_ap","hold_f1","hold_acc","hold_r2","hold_rmse")]]
    print(view.to_string(index=False))

if __name__ == "__main__":
    main()
