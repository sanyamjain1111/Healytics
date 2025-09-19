# app/routers/reports.py
from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from pathlib import Path
import os, json, time, math, asyncio, inspect, traceback

# Optional: pandas only used for future extensions; currently not required for core logic
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# DB engine (grandparent import from backend/database.py)
try:
    from ...database import engine as _app_engine  # type: ignore
except Exception:
    _app_engine = None

# Optional AI insight generator
try:
    from ...ai_services.insight_generator import AIInsightGenerator  # type: ignore
    _AI_AVAILABLE = True
    print("✓ AI service imported successfully")
except ImportError as e:
    _AI_AVAILABLE = False
    print(f"✗ AI service import failed (ImportError): {e}")
except Exception as e:
    _AI_AVAILABLE = False
    print(f"✗ AI service import failed (Other): {type(e).__name__}: {e}")

router = APIRouter(prefix="/reports", tags=["reports"])

# ---------- infra helpers ----------
def _get_engine() -> Engine:
    if _app_engine is not None:
        return _app_engine
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set and no app engine found")
    return create_engine(url, future=True)

def _ensure_tables(engine: Engine) -> None:
    DDL = """
    CREATE TABLE IF NOT EXISTS analyses (
      id BIGSERIAL PRIMARY KEY,
      dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
      strategy_id INT,
      kind TEXT,                     -- 'risk' | 'anomaly'
      artifact_path TEXT,
      summary JSONB,
      created_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS reports (
      id BIGSERIAL PRIMARY KEY,
      dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
      strategy_id INT,
      risk_json TEXT,
      anomaly_json TEXT,
      summary JSONB,
      insights JSONB,
      report_json TEXT,
      report_md TEXT,
      created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    with engine.begin() as con:
        for stmt in filter(None, DDL.split(";")):
            st = stmt.strip()
            if st:
                con.execute(text(st + ";"))

def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _latest_artifact(engine: Engine, dataset_id: int, kind: str, strategy_id: Optional[int]) -> Optional[Dict[str, Any]]:
    q = """
      SELECT id, artifact_path, summary
      FROM analyses
      WHERE dataset_id=:d AND kind=:k
        AND (:s IS NULL OR strategy_id=:s)
      ORDER BY id DESC
      LIMIT 1
    """
    with engine.begin() as con:
        row = con.execute(text(q), {"d": int(dataset_id), "k": kind, "s": strategy_id}).mappings().first()
        if row:
            return {"artifact_path": row["artifact_path"], "summary": row["summary"]}
    return None

def _ensure_dir(p: str) -> None:
    Path(p).parent.mkdir(parents=True, exist_ok=True)

# ---------- request / response models ----------
class ReportGenerateRequest(BaseModel):
    dataset_id: int
    strategy_id: Optional[int] = None
    risk_json: Optional[str] = None      # if not given, resolve from analyses table
    anomaly_json: Optional[str] = None   # if not given, resolve from analyses table

    # NEW: knobs for “high risk” logic & output sizes
    score_cutoff: float = Field(0.80, ge=0.0, le=1.0, description="Classification risk score to consider 'high'")
    min_positive_models: int = Field(2, ge=1, description="Min # of models predicting positive to flag a patient")
    top_n_patients: int = Field(20, ge=1, le=200, description="How many high-risk patients to list")
    top_n_anomalies: int = Field(20, ge=1, le=200, description="How many top anomalies to list")

# ---------- core extraction helpers ----------
def _is_classification_output(v: Any) -> bool:
    return isinstance(v, dict) and ("score" in v or "pred" in v)

def _is_regression_output(v: Any) -> bool:
    return isinstance(v, dict) and "prediction" in v and "score" not in v and "pred" not in v

def _patient_risk_stats(
    patient_entry: Dict[str, Any],
    score_cutoff: float
) -> Tuple[int, float, Dict[str, Any]]:
    """
    Returns:
      n_pos: # of classification models with pred=1 (or score>=threshold if pred missing)
      avg_score: mean of available classification risk scores
      detail: per-model distilled info
    """
    n_pos = 0
    scores: List[float] = []
    detail: Dict[str, Any] = {}
    for model_name, out in patient_entry.items():
        if model_name == "patient_id":
            continue
        if _is_classification_output(out):
            score = float(out.get("score", out.get("prob", 0.0)))
            thr = float(out.get("threshold", score_cutoff))
            pred = int(out.get("pred", int(score >= thr)))
            n_pos += int(pred == 1)
            scores.append(score)
            detail[model_name] = {"score": score, "pred": pred, "threshold": thr}
        elif _is_regression_output(out):
            # keep but don't include in avg_score; it’s not normalized
            detail[model_name] = {"prediction": float(out["prediction"])}
        else:
            # unknown shape -> ignore
            pass
    avg_score = float(sum(scores) / len(scores)) if scores else 0.0
    return n_pos, avg_score, detail

def _extract_high_risk_patients(
    risk: Dict[str, Any],
    score_cutoff: float,
    min_positive_models: int,
    top_n: int
) -> List[Dict[str, Any]]:
    """
    Build a ranked list of high-risk patients using:
      1) # positive models (desc)
      2) average classification score (desc)
    """
    patients = (risk or {}).get("patients", [])
    ranked: List[Dict[str, Any]] = []
    for p in patients:
        if not isinstance(p, dict):
            continue
        pid = str(p.get("patient_id", "unknown"))
        n_pos, avg_score, detail = _patient_risk_stats(p, score_cutoff)
        ranked.append({
            "patient_id": pid,
            "positive_models": n_pos,
            "avg_score": round(avg_score, 4),
            "models": detail
        })

    # Apply filter & sort
    filtered = [
        r for r in ranked
        if (r["positive_models"] >= min_positive_models) or (r["avg_score"] >= score_cutoff)
    ]
    filtered.sort(key=lambda r: (r["positive_models"], r["avg_score"]), reverse=True)
    return filtered[:top_n]

def _extract_top_anomalies(anomaly: Dict[str, Any], top_n: int) -> List[Dict[str, Any]]:
    pts = (anomaly or {}).get("patients", [])
    safe_rows = []
    for r in pts:
        if not isinstance(r, dict):
            continue
        pid = str(r.get("patient_id", "unknown"))
        flagged = int(r.get("anomaly_flag", r.get("anomaly", r.get("flag", 0))))
        score = float(r.get("anomaly_score", r.get("score", 0.0)) or 0.0)
        safe_rows.append({"patient_id": pid, "anomaly_flag": flagged, "anomaly_score": score})
    safe_rows.sort(key=lambda x: x["anomaly_score"], reverse=True)
    return safe_rows[:top_n]

def _model_counts_summary(risk: Dict[str, Any]) -> List[Dict[str, Any]]:
    counts = (risk or {}).get("summary", {}).get("counts", {}) or {}
    rows = []
    for m, c in counts.items():
        pos = int(c.get("positives", 0))
        tot = int(c.get("total", 0))
        rate = (pos / tot) if tot else 0.0
        rows.append({"model": m, "positives": pos, "total": tot, "rate": round(rate, 4)})
    rows.sort(key=lambda x: x["positives"], reverse=True)
    return rows

# ---------- narrative builder ----------
def _build_narrative(
    dataset_id: int,
    model_rows: List[Dict[str, Any]],
    high_risk: List[Dict[str, Any]],
    anomalies: List[Dict[str, Any]],
    cfg: ReportGenerateRequest
) -> Dict[str, Any]:
    # Top model sentences
    if model_rows:
        lead_models = ", ".join([f"{r['model']} ({r['positives']}/{r['total']})" for r in model_rows[:3]])
        model_para = (
            f"In dataset {dataset_id}, the strongest risk signals came from: {lead_models}. "
            f"Overall, {sum(r['positives'] for r in model_rows)} positive predictions were generated across "
            f"{len(model_rows)} configured model(s)."
        )
    else:
        model_para = (
            "No model-level positives were recorded. Ensure selected models are configured and artifacts are available."
        )

    # High-risk sentences
    if high_risk:
        top_names = ", ".join([f"{p['patient_id']} (pos={p['positive_models']}, avg={p['avg_score']:.2f})"
                               for p in high_risk[:5]])
        hr_count = len(high_risk)
        hr_para = (
            f"{hr_count} patient(s) met high-risk criteria "
            f"(≥{cfg.min_positive_models} positive model(s) or avg score ≥{cfg.score_cutoff:.2f}). "
            f"Examples include: {top_names}. "
            "These patients should be prioritized for clinical review and potential intervention."
        )
    else:
        hr_para = (
            "No patients met the high-risk criteria based on current thresholds; consider lowering the cutoff "
            "or reviewing model calibration if this contradicts clinical expectations."
        )

    # Anomaly sentences
    if anomalies:
        top_anom = ", ".join([f"{a['patient_id']} (score={a['anomaly_score']:.3f})" for a in anomalies[:5]])
        an_para = (
            f"Unsupervised anomaly detection highlighted {len(anomalies)} notable patient(s). "
            f"Top outliers include: {top_anom}. "
            "Anomalies may reflect rare physiology, data quality issues, or emergent risk patterns."
        )
    else:
        an_para = "No significant anomalies were detected among numeric features."

    # Recommendations
    rec_para = (
        "Recommended next steps: (1) review high-risk patients for confirmatory clinical signals; "
        "(2) adjust model thresholds if prevalence is misaligned; "
        "(3) audit outliers for data quality and clinical plausibility; "
        "(4) incorporate clinician feedback to refine the decision thresholds and follow-up workflows."
    )

    return {
        "paragraphs": [
            model_para,
            hr_para,
            an_para,
            rec_para
        ]
    }

# ---------- insights (AI + heuristic fusion) ----------
def _heuristic_insights(
    dataset_id: int,
    risk: Dict[str, Any],
    anomaly: Dict[str, Any],
    cfg: ReportGenerateRequest
) -> Dict[str, Any]:
    model_rows = _model_counts_summary(risk)
    high_risk = _extract_high_risk_patients(risk, cfg.score_cutoff, cfg.min_positive_models, cfg.top_n_patients)
    anomalies = _extract_top_anomalies(anomaly, cfg.top_n_anomalies)

    # compact machine-readable block
    base = {
        "executive_summary": f"Automated analysis completed. Found {len(high_risk)} high-risk patient(s) and "
                             f"{len([a for a in anomalies if a['anomaly_flag']==1])} anomaly-flagged cases.",
        "key_findings": {
            "models": model_rows,
            "high_risk_patients": high_risk,
            "top_anomalies": anomalies
        },
        "recommendations": [
            "Prioritize patients flagged by multiple models.",
            "Validate thresholds vs. expected prevalence.",
            "Investigate top anomalies for data/clinical causes."
        ]
    }

    # long-form narrative paragraphs
    narrative = _build_narrative(dataset_id, model_rows, high_risk, anomalies, cfg)
    base["narrative"] = narrative
    return base

def _maybe_run_ai_insights(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Try AIInsightGenerator; return None on failure/unavailability."""
    if not _AI_AVAILABLE:
        return None
    try:
        gen = AIInsightGenerator()
        fn = getattr(gen, "create_comprehensive_report", None)
        if fn is None:
            return None
        if inspect.iscoroutinefunction(fn):
            # safe for sync context
            return asyncio.run(fn(payload))
        return fn(payload)
    except Exception:
        traceback.print_exc()
        return None

def _fuse_ai_and_heuristic(ai_out: Optional[Dict[str, Any]], heur_out: Dict[str, Any]) -> Dict[str, Any]:
    """Merge AI output (if any) with heuristic—heuristic always provides patient highlights & narrative."""
    if not isinstance(ai_out, dict):
        return heur_out
    # merge shallowly
    merged = {**heur_out}
    # keep AI exec summary if present; else heuristic
    if "executive_summary" in ai_out:
        merged["executive_summary"] = ai_out["executive_summary"]
    # merge key_findings
    if "key_findings" in ai_out and isinstance(ai_out["key_findings"], dict):
        merged["key_findings"] = {**heur_out.get("key_findings", {}), **ai_out["key_findings"]}
    # merge recommendations
    if "recommendations" in ai_out and isinstance(ai_out["recommendations"], list):
        merged["recommendations"] = list(dict.fromkeys(  # de-dup keep order
            [*ai_out["recommendations"], *heur_out.get("recommendations", [])]
        ))
    # keep heuristic narrative (AI gen may not provide paragraphs)
    return merged

# ---------- endpoints ----------
@router.post("/generate")
def generate_report(req: ReportGenerateRequest) -> Dict[str, Any]:
    """
    Build insights + a compact markdown/JSON report from the latest (or provided) risk/anomaly artifacts,
    with long-form narrative paragraphs and explicit high-risk patient call-outs.
    """
    eng = _get_engine()
    _ensure_tables(eng)

    # Resolve artifact paths
    risk_path = req.risk_json
    anom_path = req.anomaly_json

    if not risk_path:
        last_risk = _latest_artifact(eng, req.dataset_id, "risk", req.strategy_id)
        if not last_risk:
            raise HTTPException(status_code=400, detail="No risk analysis JSON found. Run /analytics/run first.")
        risk_path = last_risk["artifact_path"]
    if not anom_path:
        last_anom = _latest_artifact(eng, req.dataset_id, "anomaly", req.strategy_id)
        if not last_anom:
            raise HTTPException(status_code=400, detail="No anomaly analysis JSON found. Run /analytics/run first.")
        anom_path = last_anom["artifact_path"]

    if not os.path.exists(risk_path) or not os.path.exists(anom_path):
        raise HTTPException(status_code=400, detail="Provided analysis artifact path(s) do not exist on disk.")

    risk = _read_json(risk_path)
    anomaly = _read_json(anom_path)

    # Build summary header
    summary = {
        "dataset_id": req.dataset_id,
        "strategy_id": req.strategy_id,
        "risk_overview": (risk or {}).get("summary", {}),
        "anomaly_overview": (anomaly or {}).get("summary", {}),
        "params": {
            "score_cutoff": req.score_cutoff,
            "min_positive_models": req.min_positive_models,
            "top_n_patients": req.top_n_patients,
            "top_n_anomalies": req.top_n_anomalies
        }
    }

    # Heuristic insights + AI fusion
    heur = _heuristic_insights(req.dataset_id, risk, anomaly, req)
    ai = _maybe_run_ai_insights({"risk": risk, "anomaly": anomaly, "summary": summary})
    insights = _fuse_ai_and_heuristic(ai, heur)

    # Render a verbose Markdown report
    ts = time.strftime("%Y%m%d_%H%M%S")
    base_dir = f"artifacts/reports/{req.dataset_id}/{ts}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)

    report_json_path = f"{base_dir}/report.json"
    report_md_path = f"{base_dir}/report.md"

    report_json = {
        "summary": summary,
        "insights": insights,
        "sources": {
            "risk_json": risk_path,
            "anomaly_json": anom_path
        }
    }

    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)

    # Markdown with paragraphs + patient callouts
    model_rows = insights.get("key_findings", {}).get("models", [])
    high_risk = insights.get("key_findings", {}).get("high_risk_patients", [])
    anomalies = insights.get("key_findings", {}).get("top_anomalies", [])
    paragraphs = insights.get("narrative", {}).get("paragraphs", [])

    md_lines: List[str] = []
    md_lines.append(f"# Clinical Analysis Report – Dataset {req.dataset_id}")
    md_lines.append(f"_Generated: {ts}_\n")
    md_lines.append("## Overview")
    md_lines.append(f"- **Strategy ID**: {req.strategy_id}")
    md_lines.append(f"- **Risk JSON**: `{risk_path}`")
    md_lines.append(f"- **Anomaly JSON**: `{anom_path}`")
    md_lines.append("")
    md_lines.append("## Executive Summary")
    md_lines.append(insights.get("executive_summary", ""))
    md_lines.append("")

    # Narrative paragraphs
    if paragraphs:
        md_lines.append("## Narrative")
        for p in paragraphs:
            md_lines.append(p)
            md_lines.append("")

    # Compact tables in JSON blocks for devs
    md_lines.append("## Model Snapshot")
    md_lines.append("```json")
    md_lines.append(json.dumps(model_rows, indent=2))
    md_lines.append("```")

    md_lines.append("\n## High-risk Patients")
    md_lines.append("_Definition: ≥{0} positive model(s) **or** avg score ≥{1:.2f}_".format(
        req.min_positive_models, req.score_cutoff
    ))
    md_lines.append("```json")
    md_lines.append(json.dumps(high_risk, indent=2))
    md_lines.append("```")

    md_lines.append("\n## Top Anomalies")
    md_lines.append("```json")
    md_lines.append(json.dumps(anomalies, indent=2))
    md_lines.append("```")

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # persist index row
    with eng.begin() as con:
        con.execute(
            text("""INSERT INTO reports (dataset_id, strategy_id, risk_json, anomaly_json, summary, insights, report_json, report_md)
                    VALUES (:d,:s,:r,:a,:sum,:ins,:j,:m)"""),
            {
                "d": int(req.dataset_id),
                "s": req.strategy_id,
                "r": risk_path,
                "a": anom_path,
                "sum": json.dumps(summary),
                "ins": json.dumps(insights),
                "j": report_json_path,
                "m": report_md_path,
            }
        )

    return {
        "dataset_id": req.dataset_id,
        "report_json": report_json_path,
        "report_md": report_md_path,
        "summary": summary,
        "insights": insights
    }

@router.get("/latest")
def latest_report(dataset_id: int = Query(...)) -> Dict[str, Any]:
    """Fetch the newest report pointers for a dataset."""
    eng = _get_engine()
    _ensure_tables(eng)
    with eng.begin() as con:
        row = con.execute(
            text("""SELECT id, strategy_id, report_json, report_md, created_at
                    FROM reports WHERE dataset_id=:d ORDER BY id DESC LIMIT 1"""),
            {"d": int(dataset_id)}
        ).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="No reports found for dataset")
        return {
            "id": int(row["id"]),
            "strategy_id": row["strategy_id"],
            "report_json": row["report_json"],
            "report_md": row["report_md"],
            "created_at": str(row["created_at"]),
        }
