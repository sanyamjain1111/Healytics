# app/routers/strategy.py
from __future__ import annotations
from typing import Dict, Any, Optional, List
import json, os
from fastapi import APIRouter, HTTPException, Body, Query, Form, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Prefer shared DB engine if present
try:
    from ...database import engine as _app_engine  # type: ignore
except Exception:
    _app_engine = None
# --- Gemini availability ---
from ...ai_services.gemini_strategist import GeminiStrategist  # ensure import works




router = APIRouter(tags=["strategies"])

# ---- Catalog (typo fixed) ----
STRATEGIES = [
    {
        "id": "readmission",
        "name": "Readmission Risk Suite",
        "models": ["ReadmissionPredictor", "Readmission90DPredictor", "LengthOfStayRegressor"],
    },
    {
        "id": "critical-care",
        "name": "Critical Care Early Warning",
        "models": ["SepsisEarlyWarning", "ICUAdmissionPredictor", "MortalityRiskModel", "AKIRiskPredictor"],
    },
    {
        "id": "chronic",
        "name": "Chronic Disease Risk",
        "models": [
            "DiabetesComplicationRisk","HypertensionControlPredictor",
            "HeartFailure30DRisk","StrokeRiskPredictor","COPDExacerbationPredictor","AnemiaSeverityRegressor"
        ],
    },
    {
        "id": "ops",
        "name": "Operational & Quality",
        "models": ["NoShowAppointmentPredictor","CostOfCareRegressor","AdverseDrugEventPredictor","DiseaseRiskPredictor"],
    },
]

_DEFAULT_THRESHOLDS = {
    "ReadmissionPredictor": 0.10, "Readmission90DPredictor": 0.10,
    "MortalityRiskModel": 0.35, "SepsisEarlyWarning": 0.35, "AKIRiskPredictor": 0.35,
    "HeartFailure30DRisk": 0.40, "StrokeRiskPredictor": 0.45,
    "DiabetesComplicationRisk": 0.40, "HypertensionControlPredictor": 0.50,
    "COPDExacerbationPredictor": 0.50, "NoShowAppointmentPredictor": 0.50,
    "AdverseDrugEventPredictor": 0.50, "DiseaseRiskPredictor": 0.50,
}

def _get_engine() -> Engine:
    if _app_engine is not None:
        return _app_engine
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set and no app engine found")
    return create_engine(url, future=True)

DDL = """
CREATE TABLE IF NOT EXISTS strategies (
  id SERIAL PRIMARY KEY,
  dataset_id VARCHAR(255) NOT NULL,
  raw_text TEXT,
  parsed JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
"""
def _ensure_tables(engine: Engine) -> None:
    with engine.begin() as con:
        for stmt in filter(None, DDL.split(";")):
            st = stmt.strip()
            if st:
                con.execute(text(st + ";"))

def _all_catalog_models() -> List[str]:
    return [m for s in STRATEGIES for m in s["models"]]

def _augment_models(selected: List[str], cap: int = 8) -> List[str]:
    cleaned: List[str] = []
    for x in selected or []:
        if isinstance(x, str):
            cleaned.append(x)
        elif isinstance(x, dict) and "model_name" in x:
            cleaned.append(str(x["model_name"]))
        else:
            cleaned.append(str(x))
    cleaned = list(dict.fromkeys(cleaned))
    if len(cleaned) >= 3:
        return cleaned[:cap]
    # seed from each category, then fill
    for grp in STRATEGIES:
        for m in grp["models"]:
            if m not in cleaned:
                cleaned.append(m); break
        if len(cleaned) >= cap:
            break
    for m in _all_catalog_models():
        if len(cleaned) >= cap: break
        if m not in cleaned: cleaned.append(m)
    return cleaned[:cap]

CLASSIFIERS = {
    "ReadmissionPredictor","Readmission90DPredictor","MortalityRiskModel","ICUAdmissionPredictor",
    "SepsisEarlyWarning","DiabetesComplicationRisk","HypertensionControlPredictor","HeartFailure30DRisk",
    "StrokeRiskPredictor","COPDExacerbationPredictor","AKIRiskPredictor","AdverseDrugEventPredictor",
    "NoShowAppointmentPredictor","DiseaseRiskPredictor"
}

async def _try_gemini_generate(dataset_id: str, objective: Optional[str]) -> tuple[Dict[str, Any], str]:
    strat = GeminiStrategist()
    parsed, rationale = strat.generate_parsed(dataset_id=dataset_id, objective=objective)  # Remove 'await'
    # Normalize: keep thresholds only for classifiers
    th = parsed.get("thresholds", {}) or {}
    parsed["thresholds"] = {k: v for k, v in th.items() if k in CLASSIFIERS}
    return parsed, f"{rationale}"
# Public helper
async def create_and_store_strategy(dataset_id: str, preset_id: Optional[str] = None, objective: Optional[str] = None) -> Dict[str, Any]:
    eng = _get_engine()
    _ensure_tables(eng)

    if preset_id:
        match = next((s for s in STRATEGIES if s["id"] == preset_id), None)
        if not match:
            raise HTTPException(status_code=404, detail="Unknown preset_id")
        models = _augment_models(match["models"])
        parsed = {
            "version": "1.0",
            "selected_models": models,
            "thresholds": {m: _DEFAULT_THRESHOLDS.get(m, 0.5) for m in models},
            "post_processing": {"calibration":"none"},
            "validation_plan": {"cv_folds":3,"metrics":{"classification":["roc_auc","pr_auc","f1","recall"],"regression":["mae","r2"]}},
            "visualization_specifications": {
                "risk_scores":{"type":"RiskHeatmap","x_label":"Patients","y_label":"Models","title":"Patient Risk Heatmap"},
                "feature_importance":{"type":"Bar","x_label":"Features","y_label":"Importance","title":"Top Feature Importances"},
                "distributions":{"type":"Histogram","x_label":"Value","y_label":"Frequency","title":"Distributions by Feature"},
            },
            "confidence_score": 0.68,
            "medical_specialty_focus":"general",
        }
        rationale = f"Preset strategy '{match['name']}' selected."
    else:
        try:
            parsed, rationale = await _try_gemini_generate(dataset_id=dataset_id, objective=objective)
        except Exception as e:
            combined = _augment_models(STRATEGIES[1]["models"] + STRATEGIES[2]["models"])
            parsed = {
                "version":"1.0",
                "selected_models": combined,
                "thresholds": {m: _DEFAULT_THRESHOLDS.get(m, 0.5) for m in combined},
                "post_processing":{"calibration":"none"},
                "validation_plan":{"cv_folds":3,"metrics":{"classification":["roc_auc","pr_auc","f1","recall"],"regression":["mae","r2"]}},
                "visualization_specifications":{
                    "risk_scores":{"type":"RiskHeatmap","x_label":"Patients","y_label":"Models","title":"Patient Risk Heatmap"},
                    "feature_importance":{"type":"Bar","x_label":"Features","y_label":"Importance","title":"Top Feature Importances"},
                    "distributions":{"type":"Histogram","x_label":"Value","y_label":"Frequency","title":"Distributions by Feature"},
                },
                "confidence_score":0.6,
                "medical_specialty_focus":"general",
            }
            rationale = f"Fallback strategy used: {e}"

    raw_text = rationale + "\n\n" + json.dumps(parsed, indent=2)
    with eng.begin() as con:
        sid = con.execute(
            text("INSERT INTO strategies (dataset_id, raw_text, parsed) VALUES (:d, :t, :p) RETURNING id"),
            {"d": str(dataset_id), "t": raw_text, "p": json.dumps(parsed)}
        ).scalar_one()

    return {"id": int(sid), "dataset_id": str(dataset_id), "raw_text": raw_text, "parsed": parsed}

# API models & endpoints
class StrategyRequest(BaseModel):
    dataset_id: Optional[str] = None
    preset_id: Optional[str] = None
    objective: Optional[str] = "Optimize clinical risk and anomaly detection with explainable outputs."
    class Config:
        extra = "ignore"

@router.get("/strategies")
@router.get("/strategy")
def list_strategies() -> Dict[str, Any]:
    return {"strategies": STRATEGIES}

@router.post("/strategies/generate")
@router.post("/strategy/generate")
async def generate_strategy(
    request: Request,
    dataset_id_q: Optional[str] = Query(default=None, alias="dataset_id"),
    preset_id_q: Optional[str] = Query(default=None, alias="preset_id"),
    objective_q: Optional[str] = Query(default=None, alias="objective"),
    dataset_id_f: Optional[str] = Form(default=None),
    preset_id_f: Optional[str] = Form(default=None),
    objective_f: Optional[str] = Form(default=None),
) -> Dict[str, Any]:
    body = None
    if "application/json" in (request.headers.get("content-type") or ""):
        try:
            raw = await request.body()
            if raw:
                body = json.loads(raw.decode())
        except Exception:
            body = None

    dataset_id = (body or {}).get("dataset_id") or dataset_id_q or dataset_id_f
    preset_id  = (body or {}).get("preset_id")  or preset_id_q  or preset_id_f
    objective  = (body or {}).get("objective")  or objective_q  or objective_f

    if dataset_id is None:
        raise HTTPException(status_code=400, detail="dataset_id is required.")

    strategy = await create_and_store_strategy(dataset_id=dataset_id, preset_id=preset_id, objective=objective)
    return {"strategy": strategy}
