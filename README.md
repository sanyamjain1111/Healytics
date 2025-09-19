
# Medical IntelliAnalytics Pro (AI-Driven)

Production-ready scaffold for an AI-driven medical analytics platform.  
**Stack:** FastAPI (backend) · Next.js/TS (frontend) · PostgreSQL · scikit-learn/XGBoost · Gemini for strategy.

## Quick Start

```bash
# 1) Python env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Datasets (100k patients + linked tables)
python scripts/generate_synthetic_data.py --patients 100000

# 3) Train a baseline (risk predictor as example)
python training_data/model_training_scripts/train_all_models.py --train-test 0.2

# 4) Run backend
uvicorn backend.main:app --reload --port 8000
```

## Environment
Copy `.env.example` to `.env`, add `GEMINI_API_KEY` and DB URL.

## Notes
- This repo includes **full preprocessing** (missing values, outlier handling, encoding, scaling), **hyperparameter tuning** via `RandomizedSearchCV`, and **cross‑validation**.
- AI strategy (Gemini) is integrated behind an interface. By default it runs in **simulation mode** if no key is provided.


---

## Expanded Model Library (17+ models)
Classification: ReadmissionPredictor, Readmission90DPredictor, MortalityRiskModel, ICUAdmissionPredictor, SepsisEarlyWarning, DiabetesComplicationRisk, HypertensionControlPredictor, HeartFailure30DRisk, StrokeRiskPredictor, COPDExacerbationPredictor, AKIRiskPredictor, AdverseDrugEventPredictor, NoShowAppointmentPredictor, DiseaseRiskPredictor (baseline).

Regression: LengthOfStayRegressor, CostOfCareRegressor, AnemiaSeverityRegressor.

### Train everything (targets auto-derived if missing)
```bash
python training_data/model_training_scripts/train_all_models_full.py
```

### Train one model with a custom target
```bash
python training_data/model_training_scripts/train_model.py --model MortalityRiskModel --estimator xgboost --target mortality_1y
```


## Artifacts & Reports
- Trained models are saved to `backend/artifacts/<ModelName>/best_model.joblib` with `metrics.json` and `shap_summary.png`.
- Reports (HTML + PDF) are emitted to `backend/reports/<ModelName>/`.

## API (new)
- `GET /models` — list available models
- `POST /models/train` — body: `{ "model_name": "MortalityRiskModel", "target": "mortality_1y", "estimator": "xgboost" }`
- `GET /models/{model}/artifacts` — list artifact files
- `GET /models/{model}/report/{fmt}` — `fmt` = html|pdf

## Frontend
- Open `/models` route in the Next.js app to train models and open reports.
# Healytics
