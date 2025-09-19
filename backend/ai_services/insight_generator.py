from __future__ import annotations
import os, json
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd

# Try to read a settings object, otherwise fall back to env var
try:
    from ..config import settings  # type: ignore
    _GEMINI_KEY = getattr(settings, "GEMINI_API_KEY", None)
except Exception:
    _GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def _gemini_client():
    if not _GEMINI_KEY:
        return None
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=_GEMINI_KEY)
        return genai
    except Exception:
        return None


_LLM_REPORT_PROMPT = """
You are a clinical analytics expert. You will receive a JSON with:
- "strategy": selected model list, thresholds, preprocessing
- "model_results": per-model metrics (auc/f1/precision/recall/mae/r2) and optional cohort counts
- "anomaly_results": optional anomaly summary
- "schema": optional dataset schema summary
Return **JSON ONLY** with:
{
  "executive_summary": "...",
  "key_findings": ["...", "..."],
  "recommendations": ["...", "..."],
  "cohorts_of_interest": [{"name":"...","definition":"...","why":"..."}],
  "visualization_titles": {
    "histograms": {"title":"Feature Distributions","xlabel":"Value","ylabel":"Frequency"},
    "risk_heatmap": {"title":"Patient Risk Heatmap","xlabel":"Patients","ylabel":"Models"},
    "feature_importance": {"title":"Top Predictors","xlabel":"Importance","ylabel":"Feature"}
  }
}
Be concise and concrete. No markdown, no backticks; return valid JSON only.
"""


class AIInsightGenerator:
    """
    Generates a clinical-style narrative + visualization titles.
    Uses Gemini when available; otherwise deterministic summary.
    """

    async def create_comprehensive_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # expected keys (some optional):
        # - strategy: Dict
        # - model_results: Dict[str, Any]
        # - anomaly_results: Optional[Dict[str, Any]]
        # - schema: Optional[Dict[str, Any]]
        strategy = payload.get("strategy") or {}
        model_results = payload.get("model_results") or {}
        anomaly_results = payload.get("anomaly_results") or {}
        schema = payload.get("schema") or {}

        # 1) Try Gemini for a polished narrative
        genai = _gemini_client()
        if genai is not None:
            try:
                model = genai.GenerativeModel("gemini-1.5-pro")
                ctx = {"strategy": strategy, "model_results": model_results, "anomaly_results": anomaly_results, "schema": schema}
                resp = model.generate_content(_LLM_REPORT_PROMPT + "\n\n" + json.dumps(ctx, default=self._safe_default))
                text = getattr(resp, "text", None) or (
                    resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else None
                )
                if text:
                    t = text.strip()
                    if t.startswith("```"):
                        t = t.strip("`")
                        if t.startswith("json"): t = t[4:].strip()
                    parsed = json.loads(t)
                    if isinstance(parsed, dict) and "executive_summary" in parsed:
                        # ensure visualization labels present
                        viz = parsed.get("visualization_titles") or {}
                        viz = self._with_default_viz_titles(viz)
                        parsed["visualization_titles"] = viz
                        return parsed
            except Exception:
                pass  # fall through to deterministic summary

        # 2) Deterministic fallback summary
        return self._deterministic_summary(strategy, model_results, anomaly_results, schema)

    # -------------------- deterministic summary --------------------

    def _deterministic_summary(
        self,
        strategy: Dict[str, Any],
        model_results: Dict[str, Any],
        anomaly_results: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:

        selected = strategy.get("selected_models", [])
        thresholds = strategy.get("thresholds", {})

        # basic ranking by AUC/MAE if available
        ranked = self._rank_models(model_results)

        # concise executive summary
        lines = []
        if selected:
            lines.append(f"{len(selected)} models executed: {', '.join(selected[:6])}{'...' if len(selected)>6 else ''}.")
        if ranked:
            top = ranked[0]
            lines.append(f"Top performer: {top['name']} ({top['metric']}: {top['value']:.3f}).")
        if anomaly_results:
            lines.append("Anomaly detector flagged potential outliers or data quality issues.")
        if schema:
            rows = schema.get("rows")
            lines.append(f"Dataset size: {rows} rows." if rows is not None else "")

        executive = " ".join([s for s in lines if s])

        findings = []
        for r in ranked[:5]:
            findings.append(f"{r['name']} {r['metric']}={r['value']:.3f}")

        recs = []
        if thresholds:
            recs.append("Validate decision thresholds with clinicians; adjust for sensitivity vs. specificity.")
        if anomaly_results:
            recs.append("Investigate outlier cohorts and re-check data entry pipelines.")
        if selected:
            recs.append("Deploy phased rollout with shadow evaluation before production alerts.")

        viz_titles = self._with_default_viz_titles({})

        return {
            "executive_summary": executive or "Automated analysis completed.",
            "key_findings": findings or ["Models executed; see detailed metrics."],
            "recommendations": recs or ["Review results with domain experts."],
            "cohorts_of_interest": self._simple_cohorts(schema),
            "visualization_titles": viz_titles
        }

    # -------------------- helpers --------------------

    @staticmethod
    def _safe_default(o: Any):
        if isinstance(o, (np.generic,)):
            return o.item()
        return str(o)

    @staticmethod
    def _rank_models(model_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        ranked = []
        for name, res in model_results.items():
            # prefer AUC for classifiers; MAE for regressors
            if "auc" in res:
                ranked.append({"name": name, "metric": "AUC", "value": float(res["auc"])})
            elif "mae" in res:
                ranked.append({"name": name, "metric": "MAE (lower better)", "value": float(res["mae"]) * -1.0})  # invert for sorting
            elif "r2" in res:
                ranked.append({"name": name, "metric": "R2", "value": float(res["r2"])})
        ranked.sort(key=lambda x: x["value"], reverse=True)
        # repair inverted MAE label for display
        for r in ranked:
            if r["metric"].startswith("MAE"):
                r["value"] = abs(r["value"])
        return ranked

    @staticmethod
    def _with_default_viz_titles(v: Dict[str, Any]) -> Dict[str, Any]:
        def ensure(key, title, xlabel, ylabel):
            blk = v.get(key) or {}
            blk.setdefault("title", title)
            blk.setdefault("xlabel", xlabel)
            blk.setdefault("ylabel", ylabel)
            v[key] = blk

        ensure("histograms", "Feature Distributions", "Value", "Frequency")
        ensure("risk_heatmap", "Patient Risk Heatmap", "Patients", "Models")
        ensure("feature_importance", "Top Predictors", "Importance", "Feature")
        ensure("calibration", "Calibration Curve", "Predicted Probability", "Observed Frequency")
        ensure("roc", "ROC Curve", "False Positive Rate", "True Positive Rate")
        return v

    @staticmethod
    def _simple_cohorts(schema: Dict[str, Any]) -> List[Dict[str, str]]:
        cats = schema.get("categorical") or []
        nums = schema.get("numerical") or []
        cohorts = []
        if any("diabetes" in (c.get("name","").lower()) for c in cats):
            cohorts.append({"name": "Diabetes", "definition": "diagnosis_text contains 'diabetes'", "why": "Chronic risk management"})
        if any(n.get("name","").lower() in {"age","age_years"} for n in nums):
            cohorts.append({"name": "Elderly 65+", "definition": "age >= 65", "why": "Higher risk profile"})
        return cohorts[:3]
