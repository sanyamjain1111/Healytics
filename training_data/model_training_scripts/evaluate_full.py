# -*- coding: utf-8 -*-
import json, math, os, argparse
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import (
    roc_auc_score, average_precision_score, f1_score, accuracy_score,
    precision_score, recall_score, confusion_matrix, r2_score, mean_squared_error
)
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "joined_training_sample.csv"
MODELS_DIRS = [ROOT / "artifacts" / "models", ROOT / "training_outputs"]
METRICS_DIR = ROOT / "training_outputs"
PLOTS = ROOT / "training_outputs" / "metrics_plots"
PLOTS.mkdir(parents=True, exist_ok=True)

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

def find_model_path(name):
    for d in MODELS_DIRS:
        p = (Path(d) / f"{name}.joblib")
        if p.exists(): return p
        p2 = (Path(d) / f"{name}_model.joblib")
        if p2.exists(): return p2
    return None

def find_threshold(name, default=0.5):
    mf = METRICS_DIR / f"{name}_metrics.json"
    if not mf.exists(): return default
    try:
        m = json.loads(mf.read_text(encoding="utf-8"))
        for k in ("train_best_threshold","best_threshold","optimal_threshold","decision_threshold","threshold"):
            if k in m: return float(m[k])
    except Exception:
        pass
    return default

def plot_confusion(cm, labels, title, outpath):
    fig = plt.figure()
    plt.imshow(cm, interpolation="nearest")
    plt.title(title)
    plt.xticks([0,1], labels); plt.yticks([0,1], labels)
    for (i,j),v in np.ndenumerate(cm):
        plt.text(j, i, int(v), ha='center', va='center')
    plt.xlabel("Predicted"); plt.ylabel("True")
    fig.savefig(outpath, dpi=150, bbox_inches="tight"); plt.close(fig)

def main():
    df = pd.read_csv(DATA)
    if "patient_id" not in df.columns:
        df["patient_id"] = np.arange(len(df)).astype(str)

    rows = []

    # --- Classification ---
    for model_name, target in CLASSIFICATION_MODELS.items():
        model_path = find_model_path(model_name)
        if not model_path or target not in df.columns:
            rows.append({"model":model_name,"type":"classification","status":"FAIL",
                         "reason": "missing model or target"}); continue

        pipe = joblib.load(model_path)
        X = df.drop(columns=[target])
        y = pd.to_numeric(df[target], errors="coerce").fillna(0).astype(int)

        # Get scores
        if hasattr(pipe, "predict_proba"):
            yscore = pipe.predict_proba(X)[:, -1]
        else:
            yscore = pipe.decision_function(X)
            yscore = 1.0/(1.0+np.exp(-yscore))

        thr = find_threshold(model_name, 0.5)
        yhat = (yscore >= thr).astype(int)

        # Metrics
        auc = roc_auc_score(y, yscore)
        ap = average_precision_score(y, yscore)
        f1 = f1_score(y, yhat, zero_division=0)
        prec = precision_score(y, yhat, zero_division=0)
        rec = recall_score(y, yhat, zero_division=0)
        acc = accuracy_score(y, yhat)

        # Confusion matrix plot
        cm = confusion_matrix(y, yhat, labels=[0,1])
        plot_confusion(cm, ["0","1"], f"{model_name}\nthr={thr:.2f}", PLOTS / f"{model_name}_cm.png")

        rows.append({
            "model": model_name, "type":"classification", "target": target,
            "thr": thr, "AUC": auc, "AP": ap, "F1": f1, "Precision": prec, "Recall": rec, "Accuracy": acc,
            "cm_TN": int(cm[0,0]), "cm_FP": int(cm[0,1]), "cm_FN": int(cm[1,0]), "cm_TP": int(cm[1,1]),
            "status": "OK"
        })

    # --- Regression ---
    for model_name, target in REGRESSION_MODELS.items():
        model_path = find_model_path(model_name)
        if not model_path or target not in df.columns:
            rows.append({"model":model_name,"type":"regression","status":"FAIL",
                         "reason":"missing model or target"}); continue

        pipe = joblib.load(model_path)
        X = df.drop(columns=[target])
        y = pd.to_numeric(df[target], errors="coerce")
        ypred = pipe.predict(X)
        r2 = r2_score(y, ypred)
        rmse = float(np.sqrt(mean_squared_error(y, ypred)))
        rows.append({
            "model": model_name, "type":"regression", "target": target,
            "R2": r2, "RMSE": rmse, "status": "OK"
        })

    out = pd.DataFrame(rows)
    out_path = METRICS_DIR / "evaluation_full.csv"
    out.to_csv(out_path, index=False)
    print(out.sort_values("model").to_string(index=False))
    print(f"\nSaved table → {out_path}")
    print(f"Saved confusion matrices → {PLOTS}")

if __name__ == "__main__":
    main()
