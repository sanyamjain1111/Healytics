# backend/ai_services/insight_generator.py
from __future__ import annotations
import os, json
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd

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
- "model_results": per-model aggregates (e.g., n, positives, prevalence; and/or auc/f1/mae/r2 if available)
- "anomaly_results": anomaly summary (counts/notes)
- "schema": dataset schema summary

Return JSON ONLY with:
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

Requirements for executive_summary:
- Single narrative paragraph of roughly 300–400 words.
- Clearly describe dataset scale, strongest risk signals (top models or highest prevalence), notable patterns in model_results,
  and any anomaly highlights. Explain implications for care pathways and operational triage.
- Avoid markdown and avoid backticks. No references, no bullet points. JSON string only.

Key lists:
- key_findings: at least 5 concise bullets, concrete and quantitative where possible.
- recommendations: at least 5 actionable bullets appropriate for clinicians/ops.
- cohorts_of_interest: 2–4 entries; include "why" grounded in results.

Respond with valid JSON only (no markdown, no code fences).
"""

class AIInsightGenerator:
    async def create_comprehensive_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        strategy = payload.get("strategy") or {}
        model_results = payload.get("model_results") or {}
        anomaly_results = payload.get("anomaly_results") or {}
        schema = payload.get("schema") or {}

        genai = _gemini_client()
        if genai is not None:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
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
                        viz = parsed.get("visualization_titles") or {}
                        viz = self._with_default_viz_titles(viz)
                        parsed["visualization_titles"] = viz
                        return parsed
            except Exception:
                pass  # deterministic fallback below

        return self._deterministic_summary(strategy, model_results, anomaly_results, schema)

    # (the rest of your class stays the same)
    @staticmethod
    def _safe_default(o: Any):
        if isinstance(o, (np.generic,)):
            return o.item()
        return str(o)

    @staticmethod
    def _rank_models(model_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        ranked = []
        for name, res in model_results.items():
            if "auc" in res:
                ranked.append({"name": name, "metric": "AUC", "value": float(res["auc"])})
            elif "mae" in res:
                ranked.append({"name": name, "metric": "MAE (lower better)", "value": float(res["mae"]) * -1.0})
            elif "r2" in res:
                ranked.append({"name": name, "metric": "R2", "value": float(res["r2"])})
            elif "prevalence" in res:
                ranked.append({"name": name, "metric": "Prevalence", "value": float(res["prevalence"])})
        ranked.sort(key=lambda x: x["value"], reverse=True)
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

    def _deterministic_summary(self, strategy, model_results, anomaly_results, schema) -> Dict[str, Any]:
        ranked = self._rank_models(model_results)
        selected = (strategy or {}).get("selected_models", [])
        lines = []
        if selected:
            lines.append(f"{len(selected)} models executed.")
        if ranked:
            lines.append(f"Top signal: {ranked[0]['name']} ({ranked[0]['metric']} {ranked[0]['value']:.3f}).")
        if anomaly_results:
            lines.append("Anomalies detected among numeric features.")
        if schema and 'rows' in schema:
            lines.append(f"Dataset size: {schema['rows']} rows.")
        executive = " ".join(lines) or "Automated analysis completed."

        findings = [f"{r['name']} {r['metric']}={r['value']:.3f}" for r in ranked[:5]] or ["Models executed; see details."]
        recs = [
            "Prioritize high-prevalence or high-AUC models for alerting.",
            "Review thresholds with clinicians.",
            "Investigate anomalies for data quality or rare phenotypes.",
            "Plan gradual deployment with shadow mode.",
            "Track post-deployment drift and re-calibrate quarterly."
        ]
        viz_titles = self._with_default_viz_titles({})
        cohorts = [{"name": "Elderly 65+", "definition": "age >= 65", "why": "Higher baseline risk"}]

        return {
            "executive_summary": executive,
            "key_findings": findings,
            "recommendations": recs,
            "cohorts_of_interest": cohorts,
            "visualization_titles": viz_titles
        }
