import numpy as np
import pandas as pd

def add_or_update_targets(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Basic risk score proxy
    z = (
        0.03*(df.get("age", 0)-50) +
        0.04*(df.get("bmi", 0)-25) +
        0.02*(df.get("systolic_bp", 0)-120) +
        0.02*(df.get("glucose", 0)-110) +
        0.8*(df.get("smoker", 0)) +
        np.random.normal(0, 1, size=len(df))
    )
    risk = 1/(1+np.exp(-z))

    def ensure_binary(name, prob):
        if name not in df.columns:
            df[name] = (prob > np.quantile(prob, 0.7)).astype(int)

    # Classification targets
    ensure_binary("mortality_1y", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("icu_admit", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("sepsis_label", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("dm_complication", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("htn_uncontrolled", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("hf_30d", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("stroke_label", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("copd_exac", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("aki_label", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("ade_label", risk + np.random.normal(0,0.05,len(df)))
    ensure_binary("no_show", risk + np.random.normal(0,0.05,len(df)))

    # Readmission fallback/cleanup
    if "label_readmit" not in df.columns:
        if "readmission_30d" in df.columns:
            df["label_readmit"] = (df["readmission_30d"].fillna(0)).astype(int)
        else:
            df["label_readmit"] = (risk > np.quantile(risk, 0.7)).astype(int)
    else:
        df["label_readmit"] = df["label_readmit"].fillna(0).astype(int)

    # Regression targets
    if "los_days" not in df.columns:
        base_los = 3 + 0.05*(df.get("age",0)-50) + 0.02*(df.get("systolic_bp",0)-120) + 0.03*(df.get("glucose",0)-110)
        base_los += np.where(df.get("smoker",0)==1, 0.8, 0)
        df["los_days"] = np.clip(base_los + np.random.normal(0,1,len(df)), 0.5, 30)

    if "cost_of_care" not in df.columns:
        base_cost = 5000 + 20*(df.get("age",0)) + 5*(df.get("glucose",0)) + 10*(df.get("cholesterol",0))
        base_cost += np.where(df.get("smoker",0)==1, 1500, 0)
        df["cost_of_care"] = np.clip(base_cost + np.random.normal(0,500,len(df)), 1500, 50000)

    if "anemia_severity_score" not in df.columns:
        hgb = df.get("hemoglobin")
        if hgb is None:
            hgb = 13.5 + np.random.normal(0,1.5,len(df))
        df["anemia_severity_score"] = np.clip(18 - hgb + np.random.normal(0,0.5,len(df)), 0, 15)

    return df
