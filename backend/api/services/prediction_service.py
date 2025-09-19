# app/services/prediction_service.py
from __future__ import annotations
from typing import Dict, Any, List
import os, json
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from joblib import load as _load

CLASSIFICATION_MODELS = {
    "DiseaseRiskPredictor",
    "ReadmissionPredictor","Readmission90DPredictor",
    "MortalityRiskModel","ICUAdmissionPredictor","SepsisEarlyWarning",
    "DiabetesComplicationRisk","HypertensionControlPredictor",
    "HeartFailure30DRisk","StrokeRiskPredictor","COPDExacerbationPredictor",
    "AKIRiskPredictor","AdverseDrugEventPredictor","NoShowAppointmentPredictor",
}
REGRESSION_MODELS = {"LengthOfStayRegressor","CostOfCareRegressor","AnemiaSeverityRegressor"}

def _safe_make_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def _load_all_records(engine: Engine, dataset_id: int) -> pd.DataFrame:
    with engine.begin() as con:
        df = pd.read_sql(text("SELECT * FROM patient_records WHERE dataset_id=:d ORDER BY id"),
                         con, params={"d": int(dataset_id)})
    if "id" in df.columns:
        df = df.drop(columns=["id"])
    return df

def _features_from_records(df: pd.DataFrame) -> pd.DataFrame:
    drop_cols = {"id","dataset_id"}
    return df.drop(columns=[c for c in drop_cols if c in df.columns])

def run_predictions_for_strategy(engine: Engine, dataset_id: int, parsed: Dict[str, Any]) -> Dict[str, Any]:
    selected = parsed.get("selected_models") or []
    thresholds = parsed.get("thresholds") or {}
    exports_dir = os.path.join("artifacts","exports",f"dataset_{dataset_id}")
    _safe_make_dir(exports_dir)

    df_all = _load_all_records(engine, dataset_id)
    if df_all.empty:
        return {"summary":"No records available for analysis","exports":{}}

    patient_ids = df_all.get("patient_id", pd.Series([None]*len(df_all)))
    X = _features_from_records(df_all)

    risk_results: Dict[str, Any] = {"models":{}, "patients":[]}
    anomaly_results: Dict[str, Any] = {"method":"zscore+iqr", "patients":[]}

    # model summaries
    for m in selected:
        path = os.path.join("artifacts","models",f"{m}.joblib")
        if not os.path.exists(path):
            risk_results["models"][m] = {"error":"model artifact not found"}
            continue
        try:
            model = _load(path)
            if m in CLASSIFICATION_MODELS and hasattr(model, "predict_proba"):
                prob = model.predict_proba(X)[:,1]
                thr = float(thresholds.get(m, 0.5))
                pred = (prob >= thr).astype(int)
                risk_results["models"][m] = {"threshold":thr, "positives":int(pred.sum()), "n":int(len(pred))}
            elif m in REGRESSION_MODELS and hasattr(model, "predict"):
                val = model.predict(X)
                risk_results["models"][m] = {"n":int(len(val)), "mean":float(pd.Series(val).mean())}
            else:
                risk_results["models"][m] = {"error":"unsupported model interface"}
        except Exception as e:
            risk_results["models"][m] = {"error":f"prediction failure: {e}"}

    # per-patient detail
    for i in range(len(X)):
        entry = {"patient_id": None if pd.isna(patient_ids.iloc[i]) else str(patient_ids.iloc[i]), "predictions": {}}
        for m in selected:
            path = os.path.join("artifacts","models",f"{m}.joblib")
            if not os.path.exists(path):
                continue
            try:
                model = _load(path)
                if m in CLASSIFICATION_MODELS and hasattr(model, "predict_proba"):
                    score = float(model.predict_proba(X.iloc[[i]])[:,1][0])
                    thr = float(thresholds.get(m, 0.5))
                    entry["predictions"][m] = {"score":score, "pred":int(score>=thr), "threshold":thr}
                elif m in REGRESSION_MODELS and hasattr(model, "predict"):
                    pred = float(model.predict(X.iloc[[i]])[0])
                    entry["predictions"][m] = {"prediction":pred}
            except Exception:
                pass
        risk_results["patients"].append(entry)

    # simple anomaly flags
    num_cols = X.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        z = (X[num_cols] - X[num_cols].mean()) / (X[num_cols].std(ddof=0) + 1e-9)
        z_flag = (z.abs() > 3).any(axis=1)
        try:
            q1, q3 = X[num_cols].quantile(0.25), X[num_cols].quantile(0.75)
            iqr = (q3 - q1)
            low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
            iqr_flag = ((X[num_cols] < low) | (X[num_cols] > high)).any(axis=1)
        except Exception:
            iqr_flag = pd.Series([False]*len(X), index=X.index)
        flagged = (z_flag | iqr_flag)
        anomaly_results["summary"] = {"n_flagged": int(flagged.sum()), "n_total": int(len(flagged)), "method_components":["zscore>3","iqr_1.5"]}
        anomaly_results["patients"] = [
            {"patient_id": None if pd.isna(patient_ids.iloc[i]) else str(patient_ids.iloc[i]),
             "zscore_any_gt3": bool(z_flag.iloc[i]), "iqr_outlier": bool(iqr_flag.iloc[i])}
            for i in range(len(X)) if flagged.iloc[i]
        ]
    else:
        anomaly_results["summary"] = {"n_flagged": 0, "n_total": int(len(X)), "note":"no numeric columns"}

    # write exports
    risk_path = os.path.join(exports_dir,"risk_prediction.json")
    anom_path = os.path.join(exports_dir,"anomaly_detection.json")
    with open(risk_path,"w",encoding="utf-8") as f: json.dump(risk_results,f,indent=2)
    with open(anom_path,"w",encoding="utf-8") as f: json.dump(anomaly_results,f,indent=2)

    return {
        "summary": {"risk_models": list(risk_results["models"].keys()),
                    "anomaly_flagged": anomaly_results.get("summary",{}).get("n_flagged",0)},
        "exports": {"risk_prediction": risk_path, "anomaly_detection": anom_path}
    }
