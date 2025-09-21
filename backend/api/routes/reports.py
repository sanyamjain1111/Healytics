# backend/api/routes/reports.py
from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from pathlib import Path
import os, json, time, math, asyncio, inspect, traceback

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
    # Fallback to the same local DSN used by analytics if env var is not set
    if not url:
        url = "postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
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

def _load_strategy(engine: Engine, dataset_id: int, strategy_id: Optional[int]) -> Optional[Dict[str, Any]]:
    with engine.begin() as con:
        if strategy_id is not None:
            row = con.execute(
                text("SELECT id, parsed FROM strategies WHERE id=:s AND dataset_id=:d"),
                {"s": int(strategy_id), "d": int(dataset_id)}
            ).mappings().first()
        else:
            row = con.execute(
                text("SELECT id, parsed FROM strategies WHERE dataset_id=:d ORDER BY id DESC LIMIT 1"),
                {"d": int(dataset_id)}
            ).mappings().first()
    if row:
        parsed = row["parsed"] if isinstance(row["parsed"], dict) else json.loads(row["parsed"])
        return {"id": int(row["id"]), "parsed": parsed}
    return None

def _schema_profile(engine: Engine, dataset_id: int) -> Dict[str, Any]:
    """Lightweight schema profile for the LLM."""
    try:
        with engine.begin() as con:
            df = pd.read_sql(
                text("SELECT * FROM patient_records WHERE dataset_id=:d LIMIT 500"),
                con, params={"d": int(dataset_id)}
            )
        if "id" in df.columns:
            df = df.drop(columns=["id"])
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = [c for c in df.columns if c not in num_cols]
        return {
            "rows": int(len(df)),
            "columns": [{"name": c, "dtype": str(df[c].dtype)} for c in df.columns],
            "numerical": [{"name": n} for n in num_cols],
            "categorical": [{"name": c} for c in cat_cols]
        }
    except Exception:
        return {}

def _build_model_results_from_risk(risk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert risk.summary.counts into per-model aggregates the LLM can use.
    Example per model:
      {"n": 10000, "positives": 342, "prevalence": 0.0342, "type":"classification"}
    """
    out: Dict[str, Any] = {}
    counts = (risk or {}).get("summary", {}).get("counts", {}) or {}
    for m, c in counts.items():
        pos = int(c.get("positives", 0))
        tot = int(c.get("total", 0))
        prev = (pos / tot) if tot else 0.0
        out[m] = {"n": tot, "positives": pos, "prevalence": float(prev), "type": "classification"}
    return out

# ---------- request / response models ----------
class ReportGenerateRequest(BaseModel):
    dataset_id: int
    strategy_id: Optional[int] = None
    risk_json: Optional[str] = None      # if not given, resolve from analyses table
    anomaly_json: Optional[str] = None   # if not given, resolve from analyses table

    # knobs for “high risk” lists produced in JSON (still useful for the MD appendix)
    score_cutoff: float = Field(0.80, ge=0.0, le=1.0, description="Classification risk score to consider 'high'")
    min_positive_models: int = Field(2, ge=1, description="Min # of models predicting positive to flag a patient")
    top_n_patients: int = Field(20, ge=1, le=200, description="How many high-risk patients to list")
    top_n_anomalies: int = Field(20, ge=1, le=200, description="How many top anomalies to list")

# ---------- ranking / extraction (used for JSON appendix) ----------
def _is_classification_output(v: Any) -> bool:
    return isinstance(v, dict) and ("score" in v or "pred" in v)

def _is_regression_output(v: Any) -> bool:
    return isinstance(v, dict) and "prediction" in v and "score" not in v and "pred" not in v

def _patient_risk_stats(patient_entry: Dict[str, Any], score_cutoff: float):
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
            detail[model_name] = {"prediction": float(out["prediction"])}
    avg_score = float(sum(scores) / len(scores)) if scores else 0.0
    return n_pos, avg_score, detail

def _extract_high_risk_patients(risk: Dict[str, Any], score_cutoff: float, min_positive_models: int, top_n: int):
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
    filtered = [
        r for r in ranked
        if (r["positive_models"] >= min_positive_models) or (r["avg_score"] >= score_cutoff)
    ]
    filtered.sort(key=lambda r: (r["positive_models"], r["avg_score"]), reverse=True)
    return filtered[:top_n]

def _extract_top_anomalies(anomaly: Dict[str, Any], top_n: int):
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

# ---------- AI fusion ----------
def _maybe_run_ai_insights(ai_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Try AIInsightGenerator; return None on failure/unavailability."""
    if not _AI_AVAILABLE:
        return None
    try:
        gen = AIInsightGenerator()
        fn = getattr(gen, "create_comprehensive_report", None)
        if fn is None:
            return None
        if inspect.iscoroutinefunction(fn):
            return asyncio.run(fn(ai_payload))
        return fn(ai_payload)
    except Exception:
        traceback.print_exc()
        return None

# ---------- endpoints ----------
@router.post("/generate")
def generate_report(req: ReportGenerateRequest) -> Dict[str, Any]:
    """
    Build insights via Gemini (JSON output) plus a Markdown file.
    The AI executive summary is used verbatim (300–400 words). Heuristic text is used only as a fallback.
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

    # Strategy + schema for LLM context
    strategy = _load_strategy(eng, req.dataset_id, req.strategy_id)
    schema = _schema_profile(eng, req.dataset_id)

    # Prepare AI payload that matches AIInsightGenerator’s contract
    ai_payload = {
        "strategy": (strategy or {}).get("parsed", {}),
        "model_results": _build_model_results_from_risk(risk),        # aggregates from your risk JSON
        "anomaly_results": anomaly.get("summary", {}),
        "schema": schema
    }
    ai_insights = _maybe_run_ai_insights(ai_payload)

    # Heuristic appendix (lists/tables) still useful for devs
    model_rows = _model_counts_summary(risk)
    high_risk = _extract_high_risk_patients(risk, req.score_cutoff, req.min_positive_models, req.top_n_patients)
    anomalies = _extract_top_anomalies(anomaly, req.top_n_anomalies)

    # Summary header
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

    # Final insights: prefer AI; fallback to a minimal machine block if AI failed
    if isinstance(ai_insights, dict) and "executive_summary" in ai_insights:
        insights = ai_insights
        # augment with the concrete high-risk/anomaly lists for the JSON appendix
        insights.setdefault("key_findings_tables", {})
        insights["key_findings_tables"]["models"] = model_rows
        insights["key_findings_tables"]["high_risk_patients"] = high_risk
        insights["key_findings_tables"]["top_anomalies"] = anomalies
    else:
        # very compact fallback without narrative
        insights = {
            "executive_summary": "Automated analysis completed.",
            "key_findings": [],
            "recommendations": [],
            "cohorts_of_interest": [],
            "visualization_titles": {},
            "key_findings_tables": {
                "models": model_rows,
                "high_risk_patients": high_risk,
                "top_anomalies": anomalies
            }
        }

    # Save artifacts
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

    # Markdown driven primarily by **AI** content (no hardcoded narrative paragraphs)
    md_lines: List[str] = []
    md_lines.append(f"# Clinical Analysis Report – Dataset {req.dataset_id}")
    md_lines.append(f"_Generated: {ts}_\n")
    md_lines.append("## Executive Summary")
    md_lines.append(insights.get("executive_summary", ""))
    md_lines.append("")

    # Optional sections from AI JSON
    key_findings = insights.get("key_findings") or []
    if key_findings:
        md_lines.append("## Key Findings")
        for k in key_findings:
            md_lines.append(f"- {k}")
        md_lines.append("")

    recs = insights.get("recommendations") or []
    if recs:
        md_lines.append("## Recommendations")
        for r in recs:
            md_lines.append(f"- {r}")
        md_lines.append("")

    cohorts = insights.get("cohorts_of_interest") or []
    if cohorts:
        md_lines.append("## Cohorts of Interest")
        for c in cohorts:
            md_lines.append(f"- **{c.get('name','')}** – {c.get('definition','')} — {c.get('why','')}")
        md_lines.append("")

    # Appendix: concrete JSON tables (dev-friendly)
    md_lines.append("## Appendix – Model Snapshot")
    md_lines.append("```json")
    md_lines.append(json.dumps(model_rows, indent=2))
    md_lines.append("```")

    md_lines.append("\n## Appendix – High-risk Patients")
    md_lines.append("_Definition: ≥{0} positive model(s) **or** avg score ≥{1:.2f}_".format(
        req.min_positive_models, req.score_cutoff
    ))
    md_lines.append("```json")
    md_lines.append(json.dumps(high_risk, indent=2))
    md_lines.append("```")

    md_lines.append("\n## Appendix – Top Anomalies")
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
