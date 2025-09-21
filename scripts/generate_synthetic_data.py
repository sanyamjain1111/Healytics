
import argparse, numpy as np, pandas as pd
from pathlib import Path
import uuid, random

OUT = Path("data")
OUT.mkdir(parents=True, exist_ok=True)

def synthesize_patients(n=100000, seed=42):
    rng = np.random.default_rng(seed)
    patient_ids = [str(1000000 + i) for i in range(n)]
    ages = rng.integers(18, 90, size=n)
    sex = rng.choice(["M","F"], size=n, p=[0.48, 0.52])
    bmi = rng.normal(26, 4.5, size=n).clip(15, 55)
    smoker = rng.choice([0,1], size=n, p=[0.78, 0.22])
    systolic = rng.normal(122, 14, size=n).clip(90, 200)
    diastolic = rng.normal(78, 10, size=n).clip(50, 130)
    heart_rate = rng.normal(74, 11, size=n).clip(40, 150)
    glucose = rng.normal(110, 25, size=n).clip(60, 350)
    cholesterol = rng.normal(185, 35, size=n).clip(100, 400)
    hgb = rng.normal(13.6, 1.8, size=n).clip(8, 18)
    # outcome based on risk factors with noise
    logit = (
        0.03*(ages-50) + 0.04*(bmi-25) + 0.02*(systolic-120) + 0.02*(glucose-110) +
        0.8*smoker + rng.normal(0, 1, size=n)
    )
    risk = 1/(1+np.exp(-logit))
    outcome = (risk > 0.6).astype(int)
    patients = pd.DataFrame({
        "patient_id": patient_ids,
        "age": ages,
        "sex": sex,
        "bmi": bmi.round(1),
        "smoker": smoker,
        "systolic_bp": systolic.round(0).astype(int),
        "diastolic_bp": diastolic.round(0).astype(int),
        "heart_rate": heart_rate.round(0).astype(int),
        "glucose": glucose.round(0).astype(int),
        "cholesterol": cholesterol.round(0).astype(int),
        "hemoglobin": hgb.round(1),
        "outcome": outcome
    })
    return patients

def synthesize_medications(patients):
    rng = np.random.default_rng(7)
    meds_list = ["Metformin","Atorvastatin","Amlodipine","Insulin","Losartan","Omeprazole","Hydrochlorothiazide"]
    rows = []
    for pid in patients["patient_id"]:
        k = rng.integers(0, 3)
        for _ in range(k):
            rows.append({
                "patient_id": pid,
                "medication": rng.choice(meds_list),
                "dose_mg": int(rng.choice([5,10,20,50,100])),
                "adherence": rng.choice(["Good","Moderate","Poor"], p=[0.6,0.3,0.1])
            })
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["patient_id","medication","dose_mg","adherence"])

def synthesize_outcomes(patients):
    rng = np.random.default_rng(9)
    # outcome already in patients, create timestamped records
    idx = rng.choice(patients.index, size=int(len(patients)*0.4), replace=False)
    recs = patients.loc[idx, ["patient_id","outcome"]].copy()
    recs["followup_months"] = rng.integers(1, 24, size=len(recs))
    recs["readmission_30d"] = rng.choice([0,1], size=len(recs), p=[0.9,0.1])
    return recs

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--patients", type=int, default=100000)
    args = ap.parse_args()
    pats = synthesize_patients(args.patients)
    meds = synthesize_medications(pats)
    outs = synthesize_outcomes(pats)
    pats.to_csv(OUT/"patients.csv", index=False)
    meds.to_csv(OUT/"medications.csv", index=False)
    outs.to_csv(OUT/"outcomes.csv", index=False)
    # quick joined sample for training/demo
    sample = pats.merge(outs[["patient_id","readmission_30d"]], on="patient_id", how="left")
    sample.rename(columns={"readmission_30d":"label_readmit"}, inplace=True)
    sample.to_csv(OUT/"joined_training_sample.csv", index=False)
    print("Saved CSVs in ./data")
