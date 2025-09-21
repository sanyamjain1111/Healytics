
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

NUMERIC_COLS = [
    "bmi","systolic_bp","diastolic_bp","heart_rate","resp_rate","temperature_c","spo2",
    "glucose","hba1c","creatinine","egfr","hemoglobin","wbc","platelets","cholesterol_total","ldl","hdl","triglycerides"
]

def run_anomaly_detection(df: pd.DataFrame, contamination: float = 0.02):
    sel = [c for c in NUMERIC_COLS if c in df.columns]
    X = df[sel].fillna(df[sel].median())
    if X.empty:
        return {"summary":{"message":"No numeric columns for anomaly detection"}, "per_patient":[]}
    iso = IsolationForest(random_state=42, contamination=contamination)
    scores = iso.fit_predict(X)  # -1 outlier, 1 normal
    decision = iso.decision_function(X)  # the lower, the more abnormal
    outliers = (scores == -1).astype(int)
    payload = pd.DataFrame({
            "patient_id": df.get("patient_id", pd.Series(range(len(df)))),
            "anomaly": outliers,
            "anomaly_score": -decision
    })
    summary = {
        "contamination": contamination,
        "num_outliers": int(outliers.sum()),
        "rate": float(outliers.mean())
    }
    return {"summary": summary, "per_patient": payload.to_dict(orient="records")}
