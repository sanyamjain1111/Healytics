from __future__ import annotations
import os
import json
from typing import Dict, Any, Optional, Tuple, List

import pandas as pd

# Try to use app settings, but fall back to env vars if not present
try:
    from ..config import settings  # type: ignore
    _GEMINI_KEY = getattr(settings, "GEMINI_API_KEY", None)
except Exception:
    _GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Optional prompt import; provide a safe default
try:
    from ..ai_prompts.strategy_prompts import STRATEGY_PROMPT  # type: ignore
except Exception:
    STRATEGY_PROMPT = (
        "You are a senior clinical data scientist. Given the column mapping, dataset characteristics, "
        "and medical context, design a full analysis plan:\n"
        "- Preprocessing (imputation strategy, outlier handling method, encoding, scaling)\n"
        "- Candidate models (name, estimator type, priority, expected insights)\n"
        "- Visualization specs (key charts and why)\n"
        "- Validation plan (CV folds, metrics, calibration)\n"
        "Return JSON only."
    )

# DB access if available
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Try to reuse the app engine if defined
try:
    from ..database import engine as _app_engine  # type: ignore
except Exception:
    _app_engine = None

# Fallback to file-registry loader if DB not populated
try:
    from ..api.services.datasets_service import registry, load_dataframe  # type: ignore
except Exception:
    registry = None
    load_dataframe = None


# ------------------------- infra helpers -------------------------

def _get_engine() -> Optional[Engine]:
    """Return an Engine if DATABASE_URL (or app engine) is available, else None."""
    if _app_engine is not None:
        return _app_engine
    url = os.getenv("DATABASE_URL")
    if not url:
        return None
    try:
        return create_engine(url, future=True)
    except Exception:
        return None


def _load_dataset_frame(dataset_id: int) -> pd.DataFrame:
    """
    Prefer Postgres (patient_records). Fall back to file registry if available.
    """
    eng = _get_engine()
    if eng is not None:
        try:
            with eng.begin() as con:
                df = pd.read_sql(
                    text("SELECT * FROM patient_records WHERE dataset_id=:d"),
                    con,
                    params={"d": int(dataset_id)}
                )
            if "id" in df.columns:
                df = df.drop(columns=["id"])
            return df
        except Exception:
            pass

    # fallback to registry
    if registry is not None and load_dataframe is not None:
        try:
            ds = registry.get(str(dataset_id))
            if ds:
                return load_dataframe(registry.path_for(str(dataset_id)))
        except Exception:
            pass

    # If everything fails, return empty
    return pd.DataFrame()


def _basic_schema_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Small summary for the prompt and for heuristics.
    """
    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": [],
            "numerical": [],
            "categorical": []
        }
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numerical": num_cols,
        "categorical": cat_cols
    }


# ------------------------- heuristic strategy -------------------------

# Buckets that map to your trained model names
READMISSION_MODELS = ["ReadmissionPredictor", "Readmission90DPredictor", "LengthOfStayRegressor"]
CRITICAL_MODELS = ["SepsisEarlyWarning", "ICUAdmissionPredictor", "MortalityRiskModel", "AKIRiskPredictor"]
CHRONIC_MODELS = ["DiabetesComplicationRisk", "HypertensionControlPredictor", "HeartFailure30DRisk",
                  "StrokeRiskPredictor", "COPDExacerbationPredictor", "AnemiaSeverityRegressor"]
OPS_MODELS = ["NoShowAppointmentPredictor", "CostOfCareRegressor", "AdverseDrugEventPredictor", "DiseaseRiskPredictor"]

def _infer_models_from_columns(cols: List[str]) -> List[str]:
    """
    Heuristic selection of model suites based on column presence.
    """
    lc = [c.lower() for c in cols]

    selected: List[str] = []

    # Signals for chronic disease risk
    if any(k in lc for k in ["hba1c", "glucose", "creatinine", "egfr", "hypertension_history", "diabetes_history"]):
        selected += CHRONIC_MODELS

    # Vitals -> critical care early warning
    if any(k in lc for k in ["spo2", "systolic_bp", "diastolic_bp", "heart_rate", "respiratory_rate", "temperature"]):
        selected += CRITICAL_MODELS

    # Scheduling / ops signals
    if any(k in lc for k in ["appointment", "no_show", "cost", "billing", "payer"]):
        selected += OPS_MODELS

    # Readmission-ish signals
    if any(k in lc for k in ["discharge", "length_of_stay", "readmission", "readmit"]):
        selected += READMISSION_MODELS

    # Always include disease risk as a catch-all if nothing else matched
    if not selected:
        selected += ["DiseaseRiskPredictor"]

    # dedupe, keep order
    out = []
    seen = set()
    for m in selected:
        if m not in seen:
            out.append(m)
            seen.add(m)
    return out


def _heuristic_strategy(df: pd.DataFrame, objective: Optional[str]) -> Tuple[Dict[str, Any], str]:
    schema = _basic_schema_summary(df)
    selected = _infer_models_from_columns(schema["columns"])
    thresholds = {m: 0.5 for m in selected}

    parsed = {
        "version": "1.0",
        "selected_models": selected,
        "thresholds": thresholds,
        "post_processing": {
            "calibration": "none"
        },
        "preprocessing": {
            "imputation": "median",
            "outliers": "iqr_clipping",
            "encoding": "onehot",
            "scaling": "standard"
        },
        "validation": {
            "cv_folds": 3,
            "metrics": ["roc_auc", "f1", "precision", "recall"]
        },
    }
    rationale = (
        "Heuristic strategy generated without Gemini. "
        f"Detected columns: {', '.join(schema['columns'][:20])}{'...' if len(schema['columns'])>20 else ''}. "
        f"Selected models: {', '.join(selected)}."
    )
    return parsed, rationale


# ------------------------- Gemini-backed strategy -------------------------

def _gemini_client():
    """
    Return a ready-to-use Gemini client if library and key are available.
    """
    if not _GEMINI_KEY:
        return None
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=_GEMINI_KEY)
        return genai
    except Exception:
        return None


def _call_gemini(genai, prompt: str) -> Optional[Dict[str, Any]]:
    """
    Call Gemini and parse JSON from the response text.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", None) or (resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else None)
        if not text:
            return None
        # Extract JSON (the prompt requests JSON only).
        # If the model includes fences, strip them.
        text = text.strip()
        if text.startswith("```"):
            # remove triple-fence block
            text = text.strip("`")
            # after stripping fences, sometimes "json" remains at the top
            if text.startswith("json"):
                text = text[4:].strip()
        return json.loads(text)
    except Exception:
        return None


def _to_parsed_strategy_from_llm(raw_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize an LLM-returned structure into the parsed strategy we use downstream.
    """
    # Try to read candidate models
    models = []
    thresholds = {}

    # Accept a variety of shapes from the LLM:
    # 1) {"model_execution_plan":{"primary_models":[{"model_name":...}]}}
    # 2) {"selected_models":[...]}
    if "model_execution_plan" in raw_json and isinstance(raw_json["model_execution_plan"], dict):
        prim = raw_json["model_execution_plan"].get("primary_models", [])
        for m in prim:
            name = m.get("model_name") if isinstance(m, dict) else None
            if name:
                models.append(name)
    elif "selected_models" in raw_json and isinstance(raw_json["selected_models"], list):
        models = [str(x) for x in raw_json["selected_models"]]

    # default if empty
    if not models:
        models = ["DiseaseRiskPredictor"]

    thresholds = {m: 0.5 for m in models}

    # Preprocessing normalization
    pre = raw_json.get("preprocessing_strategy") or raw_json.get("preprocessing") or {}
    if not isinstance(pre, dict):
        pre = {}

    parsed = {
        "version": "1.0",
        "selected_models": models,
        "thresholds": thresholds,
        "post_processing": {"calibration": "none"},
        "preprocessing": {
            "imputation": pre.get("imputation", "median"),
            "outliers": pre.get("outliers", "iqr_clipping"),
            "encoding": pre.get("encoding", "onehot"),
            "scaling": pre.get("scaling", "standard"),
        },
        "validation": raw_json.get("validation_plan", {"cv_folds": 3, "metrics": ["roc_auc", "f1", "precision", "recall"]}),
        "visualizations": raw_json.get("visualization_specifications", {}),
    }
    return parsed


# ------------------------- public API -------------------------

def generate_strategy(dataset_id: int, objective: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
    """
    Main entry used by /strategies/generate.
    Returns (parsed_strategy_dict, rationale_str).
    """
    df = _load_dataset_frame(dataset_id)

    # Try Gemini first if possible
    genai = _gemini_client()
    if genai is not None:
        schema = _basic_schema_summary(df)
        # Build the full prompt
        user = {
            "dataset_id": dataset_id,
            "objective": objective or "Optimize clinical risk and anomaly detection with explainable outputs.",
            "schema": schema,
            "hints": {
                "available_model_names": READMISSION_MODELS + CRITICAL_MODELS + CHRONIC_MODELS + OPS_MODELS
            }
        }
        full_prompt = f"{STRATEGY_PROMPT.strip()}\n\n<CONTEXT>\n{json.dumps(user, indent=2)}\n</CONTEXT>"
        raw = _call_gemini(genai, full_prompt)
        if isinstance(raw, dict):
            parsed = _to_parsed_strategy_from_llm(raw)
            rationale = "Gemini-generated strategy based on dataset schema and objective."
            return parsed, rationale

    # Fallback heuristic
    parsed, rationale = _heuristic_strategy(df, objective)
    return parsed, rationale


# ------------------------- backwards-compatible class -------------------------

class GeminiStrategist:
    """
    Backwards-compatible class wrapper.
    """
    async def generate_comprehensive_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Context may include dataset_id and medical_context
        dataset_id = context.get("dataset_id")
        df = _load_dataset_frame(dataset_id) if dataset_id is not None else pd.DataFrame()

        genai = _gemini_client()
        if genai is not None:
            user = {
                "dataset_id": dataset_id,
                "objective": context.get("objective", "Optimize clinical risk and anomaly detection with explainable outputs."),
                "schema": _basic_schema_summary(df),
                "medical_context": context.get("medical_context", {}),
                "hints": {
                    "available_model_names": READMISSION_MODELS + CRITICAL_MODELS + CHRONIC_MODELS + OPS_MODELS
                }
            }
            full_prompt = f"{STRATEGY_PROMPT.strip()}\n\n<CONTEXT>\n{json.dumps(user, indent=2)}\n</CONTEXT>"
            raw = _call_gemini(genai, full_prompt)
            if isinstance(raw, dict):
                return raw

        # simple heuristic structure that resembles your previous class’s return
        models = [{"model_name": m, "parameters": {}, "priority": "medium", "expected_insights": "Model outputs"} 
                  for m in _infer_models_from_columns(_basic_schema_summary(df)["columns"])]
        return {
            "preprocessing_strategy": {
                "imputation": "simple",
                "outliers": "iqr_clipping",
                "encoding": "onehot",
                "scaling": "standard"
            },
            "model_execution_plan": {"primary_models": models},
            "visualization_specifications": {"chart_types": {"risk_scores": "RiskHeatmap"}},
            "confidence_score": 0.7,
            "medical_specialty_focus": context.get("medical_context", {}).get("specialty", "general")
        }
