import numpy as np
import pandas as pd

# In production, set True to require real labels (no fabrication).
STRICT_LABELS_ONLY = False

def _col(df, name, default=0.0):
    s = df.get(name)
    if s is None:
        return np.full(len(df), default, dtype=float)
    return pd.to_numeric(s, errors="coerce").fillna(default).to_numpy()

def _logit(x): 
    return 1.0 / (1.0 + np.exp(-x))

def _make_binary(df, name, z, prevalence_q=0.7):
    if name in df.columns:
        return df
    p = _logit(z)
    thr = np.quantile(p, prevalence_q)
    df[name] = (p > thr).astype(int)
    return df

def add_or_update_targets(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Features (safe)
    age   = _col(df, "age", 50)
    bmi   = _col(df, "bmi", 25)
    sbp   = _col(df, "systolic_bp", 120)
    glu   = _col(df, "glucose", 110)
    hgb   = _col(df, "hemoglobin", 13.5)
    chol  = _col(df, "cholesterol", 180)
    smoke = _col(df, "smoker", 0)
    noise = lambda s: np.random.normal(0, s, size=len(df))

    REQUIRED = [
        "label_readmit","mortality_1y","icu_admit","sepsis_label","dm_complication",
        "htn_uncontrolled","hf_30d","stroke_label","copd_exac","aki_label","ade_label",
        "no_show"
    ]
    if STRICT_LABELS_ONLY:
        missing = [t for t in REQUIRED if t not in df.columns]
        if missing:
            raise ValueError(f"Missing required labels: {missing}. Provide real labels or disable STRICT_LABELS_ONLY.")

    # Task-specific latent risks (reduced coupling)
    z_mort   = 0.05*(age-60) + 0.03*(glu-120) + 0.02*(sbp-130) + 0.02*(chol-180) + 0.6*smoke + noise(0.8)
    z_icu    = 0.04*(age-55) + 0.03*(sbp-140) + 0.03*(bmi-28)  + 0.4*smoke + noise(0.7)
    z_sepsis = 0.02*(age-50) + 0.05*(glu-120) + 0.02*(bmi-27)  + 0.03*(sbp-120) + noise(0.8)
    z_dm     = 0.01*(age-45) + 0.06*(glu-115) + 0.02*(bmi-27)  + 0.2*smoke + noise(0.6)
    z_htn    = 0.02*(age-50) + 0.06*(sbp-135) + 0.02*(bmi-27)  + noise(0.7)
    z_hf     = 0.05*(age-65) + 0.03*(sbp-140) + 0.02*(bmi-29)  + 0.02*(chol-190) + noise(0.7)
    z_strk   = 0.05*(age-65) + 0.02*(sbp-140) + 0.03*(chol-200) + 0.2*smoke + noise(0.7)
    z_copd   = 0.01*(age-55) + 0.02*(sbp-130) + 0.06*smoke + noise(0.7)
    z_aki    = 0.03*(age-60) + 0.04*(glu-120) + 0.02*(sbp-135) + noise(0.7)
    z_ade    = 0.02*(age-50) + 0.02*(glu-115) + 0.02*(sbp-130) + 0.02*(chol-180) + noise(0.8)
    z_ns     = 0.01*(age-40) + 0.01*(bmi-26)  + noise(0.9)

    df = _make_binary(df, "mortality_1y",        z_mort,   prevalence_q=0.85)
    df = _make_binary(df, "icu_admit",           z_icu,    prevalence_q=0.80)
    df = _make_binary(df, "sepsis_label",        z_sepsis, prevalence_q=0.75)
    df = _make_binary(df, "dm_complication",     z_dm,     prevalence_q=0.70)
    df = _make_binary(df, "htn_uncontrolled",    z_htn,    prevalence_q=0.70)
    df = _make_binary(df, "hf_30d",              z_hf,     prevalence_q=0.82)
    df = _make_binary(df, "stroke_label",        z_strk,   prevalence_q=0.88)
    df = _make_binary(df, "copd_exac",           z_copd,   prevalence_q=0.78)
    df = _make_binary(df, "aki_label",           z_aki,    prevalence_q=0.82)
    df = _make_binary(df, "ade_label",           z_ade,    prevalence_q=0.80)
    df = _make_binary(df, "no_show",             z_ns,     prevalence_q=0.60)

    # Readmission (prefer real if present)
    if "label_readmit" not in df.columns:
        if "readmission_30d" in df.columns:
            df["label_readmit"] = pd.to_numeric(df["readmission_30d"], errors="coerce").fillna(0).astype(int)
        else:
            z_readmit = 0.03*(age-55) + 0.03*(sbp-135) + 0.03*(bmi-28) + 0.02*(glu-115) + noise(0.8)
            p = _logit(z_readmit)
            df["label_readmit"] = (p > np.quantile(p, 0.75)).astype(int)
    else:
        df["label_readmit"] = pd.to_numeric(df["label_readmit"], errors="coerce").fillna(0).astype(int)

    # Regression targets
    if "los_days" not in df.columns:
        base = 3 + 0.05*(age-50) + 0.02*(sbp-120) + 0.03*(glu-110) + np.where(smoke==1, 0.8, 0)
        df["los_days"] = np.clip(base + np.random.normal(0,1,len(df)), 0.5, 30)

    if "cost_of_care" not in df.columns:
        base = 5000 + 20*age + 5*glu + 10*chol + np.where(smoke==1, 1500, 0)
        df["cost_of_care"] = np.clip(base + np.random.normal(0,500,len(df)), 1500, 50000)

    if "anemia_severity_score" not in df.columns:
        df["anemia_severity_score"] = np.clip(18 - hgb + np.random.normal(0,0.5,len(df)), 0, 15)

    return df
