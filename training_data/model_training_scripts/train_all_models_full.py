
import json, importlib
from pathlib import Path
import pandas as pd
from training_data.utils.derive_targets import add_or_update_targets
from backend.ml_library.model_factory import DynamicModelFactory

DEFAULT_TARGETS = {
    # classification
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

    # regression
    "LengthOfStayRegressor": "los_days",
    "CostOfCareRegressor": "cost_of_care",
    "AnemiaSeverityRegressor": "anemia_severity_score"
}

def load_data():
    p = Path("data/joined_training_sample.csv")
    if p.exists():
        df = pd.read_csv(p)
    else:
        df = pd.read_csv("data/patients.csv")
    return add_or_update_targets(df)
import asyncio
def main():
    df = load_data()
    outdir = Path("training_outputs")
    outdir.mkdir(parents=True, exist_ok=True)

    for model_name in DynamicModelFactory.MODEL_REGISTRY.keys():
        if model_name == "ClinicalAnomalyDetector":
            # Skip here; unsupervised
            continue
        target = DEFAULT_TARGETS.get(model_name)
        X = df.copy()
        y = None
        if target and target in X.columns:
            y = X[target]
            X = X.drop(columns=[target])

        module = importlib.import_module(DynamicModelFactory.MODEL_REGISTRY[model_name])
        cls = getattr(module, model_name)
        # Choose sensible default estimator
        est = "xgboost" if "Risk" in model_name or "Sepsis" in model_name or "Stroke" in model_name else "random_forest"
        model = cls(estimator=est)
        try:
            res = asyncio.run(model.fit_and_evaluate(X, y))
            with open(outdir/f"{model_name}_metrics.json", "w") as f:
                json.dump(res, f, indent=2)
            print(f"Trained {model_name}:", json.dumps(res)[:200], "...")
        except Exception as e:
            err = {"error": str(e)}
            with open(outdir/f"{model_name}_metrics.json", "w") as f:
                json.dump(err, f, indent=2)
            print(f"FAILED {model_name}:", e)

if __name__ == "__main__":
    main()
