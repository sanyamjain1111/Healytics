# backend/ai_services/gemini_strategist.py
from __future__ import annotations
import os, json, math
from typing import Dict, Any, Optional, Tuple, List
import pandas as pd

# Try settings or env
try:
    from ..config import settings  # type: ignore
    _GEMINI_KEY = getattr(settings, "GEMINI_API_KEY", None)
except Exception:
    _GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Optional: shared DB engine for loading dataset by id
try:
    from ..database import engine as _app_engine  # type: ignore
except Exception:
    _app_engine = None

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Fallback dataset file registry (if present)
try:
    from ..api.services.datasets_service import registry, load_dataframe  # type: ignore
except Exception:
    registry, load_dataframe = None, None


def _engine() -> Optional[Engine]:
    if _app_engine is not None:
        return _app_engine
    url = os.getenv("DATABASE_URL")
    if not url:
        return None
    try:
        return create_engine(url, future=True)
    except Exception:
        return None


def _load_df(dataset_id: str | int) -> pd.DataFrame:
    eng = _engine()
    if eng is not None:
        try:
            with eng.begin() as con:
                df = pd.read_sql(text("SELECT * FROM patient_records WHERE dataset_id=:d"),
                                 con, params={"d": int(dataset_id)})
            if "id" in df.columns:
                df = df.drop(columns=["id"])
            return df
        except Exception:
            pass
    if registry and load_dataframe:
        try:
            node = registry.get(str(dataset_id))
            if node:
                return load_dataframe(registry.path_for(str(dataset_id)))
        except Exception:
            pass
    return pd.DataFrame()


def _schema_profile(df: pd.DataFrame) -> Dict[str, Any]:
    if df is None or df.empty:
        return {"rows": 0, "columns": [], "numerical": [], "categorical": [], "preview": []}
    
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]
    
    # Convert preview to JSON-serializable format
    preview_df = df.head(50).copy()
    
    # Convert datetime columns to strings
    datetime_cols = df.select_dtypes(include=['datetime64', 'datetimetz']).columns
    for col in datetime_cols:
        preview_df[col] = preview_df[col].astype(str)
    
    # Convert any remaining problematic types
    for col in preview_df.columns:
        if preview_df[col].dtype == 'object':
            preview_df[col] = preview_df[col].astype(str)
    
    # Convert to dict with proper handling
    preview = []
    for _, row in preview_df.iterrows():
        row_dict = {}
        for col, val in row.items():
            if pd.isna(val):
                row_dict[col] = None
            elif isinstance(val, (pd.Timestamp, pd.Timedelta)):
                row_dict[col] = str(val)
            elif isinstance(val, (int, float, str, bool)):
                row_dict[col] = val
            else:
                row_dict[col] = str(val)
        preview.append(row_dict)
    
    # lightweight numeric stats (helps the LLM decide targets & bands)
    stats = {}
    for c in num_cols[:40]:
        s = df[c]
        stats[c] = {
            "min": None if s.empty else (float(s.min()) if s.notna().any() else None),
            "max": None if s.empty else (float(s.max()) if s.notna().any() else None),
            "mean": None if s.empty else (float(s.mean()) if s.notna().any() else None),
            "sd": None if s.empty else (float(s.std()) if s.notna().any() else None),
            "missing_pct": float(s.isna().mean()),
        }
    for c in cat_cols[:40]:
        s = df[c].astype(str)
        stats[c] = {
            "unique": int(s.nunique(dropna=True)),
            "top": str(s.mode(dropna=True).iloc[0]) if s.nunique(dropna=True) > 0 else None,
            "missing_pct": float(df[c].isna().mean())
        }
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numerical": num_cols,
        "categorical": cat_cols,
        "datetime_columns": datetime_cols.tolist(),
        "stats": stats,
        "preview": preview
    }


_SYSTEM_INSTRUCTIONS = """
You are a senior clinical data scientist. Produce ONLY valid JSON (no extra text).
Given a dataset profile, design an analysis plan:

- Select relevant models from this list (names must match exactly):
  ["ReadmissionPredictor","Readmission90DPredictor","MortalityRiskModel","ICUAdmissionPredictor",
   "SepsisEarlyWarning","DiabetesComplicationRisk","HypertensionControlPredictor","HeartFailure30DRisk",
   "StrokeRiskPredictor","COPDExacerbationPredictor","AKIRiskPredictor","AdverseDrugEventPredictor",
   "NoShowAppointmentPredictor","DiseaseRiskPredictor","LengthOfStayRegressor","CostOfCareRegressor",
   "AnemiaSeverityRegressor"]

- For each selected model return: { "model_name", "task_type": "classification" | "regression",
  "target_signal_candidates": [columns or expressions], "rationale" }.

- Provide thresholds only for classification models (0..1 float). DO NOT include thresholds for regressors.

- Provide visualization specs for dashboard (risk heatmap, feature importance, distributions,
  and any regression bands). Use concise, machine-consumable keys.

- Provide preprocessing plan (imputation, outliers, encoding, scaling) & validation plan.

Return JSON with this schema:
{
  "model_execution_plan": {
    "primary_models": [
      {
        "model_name": "...",
        "task_type": "classification|regression",
        "priority": "high|medium|low",
        "target_signal_candidates": ["...", "..."],
        "rationale": "..."
      }
    ],
    "thresholds": { "<classifier>": 0.5, ... }      // classifiers only
  },
  "preprocessing": { "imputation": "...", "outliers": "...", "encoding": "...", "scaling": "..." },
  "validation_plan": { "cv_folds": 3, "metrics": { "classification": [...], "regression": [...] } },
  "visualization_specifications": {
    "risk_scores": {"type":"RiskHeatmap"},
    "feature_importance": {"type":"Bar"},
    "distributions": {"type":"Histogram"},
    "regression_bands": { "<regressor>": {"low":"p25","medium":"p50","high":"p75"} }
  }
}
"""


# JSON encoder that handles timestamps
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, pd.Timedelta):
            return str(obj)
        elif pd.isna(obj):
            return None
        return super().default(obj)


def _gemini():
    if not _GEMINI_KEY:
        return None
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=_GEMINI_KEY)
        return genai
    except Exception:
        return None


def _extract_json(txt: str) -> Optional[Dict[str, Any]]:
    if not txt:
        return None
    t = txt.strip()
    if t.startswith("```"):
        # remove fencing
        t = t.strip("`")
        if t.startswith("json"):
            t = t[4:].strip()
    try:
        return json.loads(t)
    except Exception:
        return None


def _normalize_models(raw: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    models: List[Dict[str, Any]] = []
    thresholds: Dict[str, float] = {}

    # Prefer new structure
    plan = raw.get("model_execution_plan") or {}
    prim = plan.get("primary_models") or raw.get("primary_models") or []
    if isinstance(prim, list):
        for item in prim:
            if isinstance(item, dict) and "model_name" in item:
                m = {
                    "model_name": str(item["model_name"]),
                    "task_type": str(item.get("task_type", "classification")),
                    "priority": str(item.get("priority", "medium")),
                    "target_signal_candidates": list(item.get("target_signal_candidates", [])),
                    "rationale": str(item.get("rationale", "")),
                }
                models.append(m)

    th = plan.get("thresholds") or raw.get("thresholds") or {}
    if isinstance(th, dict):
        for k, v in th.items():
            try:
                thresholds[str(k)] = float(v)
            except Exception:
                pass

    # Final defense: ensure strings
    for i, m in enumerate(models):
        models[i]["model_name"] = str(m["model_name"])
        models[i]["task_type"] = "regression" if m["model_name"].endswith("Regressor") else str(m["task_type"])

    return models, thresholds


class GeminiStrategist:
    """
    Generates a dataset-aware strategy with a strict JSON contract.
    """

    def generate_parsed(self, dataset_id: str | int, objective: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        df = _load_df(dataset_id)
        profile = _schema_profile(df)

        # Build the prompt with system + user content
        payload = {
            "objective": objective or "Clinical risk, operations, and outcomes insights with explainability.",
            "dataset_profile": profile
        }

        genai = _gemini()
        if genai is not None:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = "\n".join([
                    _SYSTEM_INSTRUCTIONS.strip(),
                    "<CONTEXT>",
                    json.dumps(payload, ensure_ascii=False, cls=DateTimeEncoder),
                    "</CONTEXT>"
                ])
                
                resp = model.generate_content(prompt)
                
                text = getattr(resp, "text", None) or (
                    resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else None
                )
                
                if text:
                    raw = _extract_json(text)
                    if isinstance(raw, dict):
                        models, thresholds = _normalize_models(raw)
                        selected = [m["model_name"] for m in models]
                        
                        parsed = {
                            "version": "1.0",
                            "selected_models": selected,
                            "thresholds": {k: v for k, v in thresholds.items() if not k.endswith("Regressor")},
                            "preprocessing": raw.get("preprocessing", {"imputation":"median","outliers":"iqr_clipping","encoding":"onehot","scaling":"standard"}),
                            "validation_plan": raw.get("validation_plan", {"cv_folds":3,"metrics":{"classification":["roc_auc","f1","recall"],"regression":["mae","r2"]}}),
                            "visualization_specifications": raw.get("visualization_specifications", {"risk_scores":{"type":"RiskHeatmap"},"feature_importance":{"type":"Bar"},"distributions":{"type":"Histogram"}}),
                            "llm_models_block": models
                        }
                        return parsed, "Gemini strategy (gemini-1.5-flash)"
                        
            except Exception:
                pass

        # Heuristic fallback
        base = [
            "SepsisEarlyWarning","ICUAdmissionPredictor","MortalityRiskModel",
            "DiabetesComplicationRisk","HypertensionControlPredictor","HeartFailure30DRisk",
            "StrokeRiskPredictor","COPDExacerbationPredictor"
        ]
        parsed = {
            "version":"1.0",
            "selected_models": base,
            "thresholds": {"SepsisEarlyWarning":0.35,"ICUAdmissionPredictor":0.5,"MortalityRiskModel":0.35,
                           "DiabetesComplicationRisk":0.4,"HypertensionControlPredictor":0.5,
                           "HeartFailure30DRisk":0.4,"StrokeRiskPredictor":0.45,"COPDExacerbationPredictor":0.5},
            "preprocessing":{"imputation":"median","outliers":"iqr_clipping","encoding":"onehot","scaling":"standard"},
            "validation_plan":{"cv_folds":3,"metrics":{"classification":["roc_auc","f1","recall"],"regression":["mae","r2"]}},
            "visualization_specifications":{"risk_scores":{"type":"RiskHeatmap"},"feature_importance":{"type":"Bar"},"distributions":{"type":"Histogram"}}
        }
        return parsed, f"Heuristic strategy: based on {profile['rows']} rows & {len(profile['columns'])} columns."