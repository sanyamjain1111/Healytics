from __future__ import annotations
import os, re, json, math
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Try to read a settings object, otherwise fall back to env var
try:
    from ..config import settings  # type: ignore
    _GEMINI_KEY = getattr(settings, "GEMINI_API_KEY", None)
except Exception:
    _GEMINI_KEY = os.getenv("GEMINI_API_KEY")


# ----------------------------- Gemini helpers -----------------------------

def _gemini_client():
    if not _GEMINI_KEY:
        return None
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=_GEMINI_KEY)
        return genai
    except Exception:
        return None


_GEMINI_MAPPING_PROMPT = """
You are a clinical data scientist. You will receive a JSON block with:
- "column_names": list of column names from a tabular healthcare dataset
- "sample": object of {column_name: [example values...]} with up to 10 examples per column
- "notes": optional hints

Return **JSON ONLY** (no prose) mapping each input column to:
  {
    "detected_type": one of [
      "patient_id","encounter_id","age","sex","height_cm","weight_kg",
      "bmi","systolic_bp","diastolic_bp","map","heart_rate","respiratory_rate",
      "temperature_c","spo2","glucose","hba1c","creatinine","egfr","bun",
      "cholesterol_total","ldl","hdl","triglycerides","hemoglobin",
      "diagnosis_code","diagnosis_text","procedure_code","procedure_text",
      "medication","dose","route","smoking_status","alcohol_use",
      "readmission_flag","mortality_flag","icu_admit_flag","sepsis_flag",
      "aki_flag","length_of_stay","discharge_disposition","payer",
      "appointment_dt","no_show_flag","cost","label","timestamp","date","other"
    ],
    "confidence": float in [0,1],
    "rationale": short phrase (<=12 words)
  }

Also return a top-level "medical_specialty" guess (e.g., "general","cardiology","endocrinology","pulmonology","nephrology","critical_care","operations"),
and "suggested_analyses": a list from ["risk_prediction","critical_care_early_warning","population_health","anomaly_detection","operations"].

FORMAT:
{
  "column_mappings": { "<col>": {"detected_type":"...", "confidence":0.87, "rationale":"..."} , ... },
  "medical_specialty": "...",
  "suggested_analyses": ["...","..."]
}
Return strictly valid JSON. Do not include backticks or markdown code fences.
"""


# ----------------------------- Heuristic helpers -----------------------------

_ID_PATTERNS = [
    r"(?:^|_)patient(?:_|$).*id", r"(?:^|_)mrn(?:_|$)", r"(?:^|_)pid(?:_|$)", r"patient.*number",
    r"(?:^|_)encounter(?:_|$).*id", r"(?:^|_)visit(?:_|$).*id", r"(?:^|_)account(?:_|$).*id"
]
_NUM_NAME_MAP = {
    "age": [r"^age$"],
    "height_cm": [r"height"],
    "weight_kg": [r"weight"],
    "bmi": [r"\bbmi\b"],
    "systolic_bp": [r"systolic|sbp"],
    "diastolic_bp": [r"diastolic|dbp"],
    "map": [r"\bmap\b|mean.*arterial"],
    "heart_rate": [r"heart.*rate|pulse|\bhr\b"],
    "respiratory_rate": [r"resp.*rate|\brr\b"],
    "temperature_c": [r"temp|temperature"],
    "spo2": [r"spo2|oxygen|o2.*sat"],
    "glucose": [r"glucose|blood.*sugar|\bbg\b"],
    "hba1c": [r"hba1c|a1c"],
    "creatinine": [r"creatinine|\bcr\b"],
    "egfr": [r"\begfr\b|gfr"],
    "bun": [r"\bbun\b"],
    "cholesterol_total": [r"cholesterol.*total|\bchol\b"],
    "ldl": [r"\bldl\b"],
    "hdl": [r"\bhdl\b"],
    "triglycerides": [r"triglyceride|\btg\b"],
    "hemoglobin": [r"hemoglobin|\bhgb\b|\bhb\b"],
    "length_of_stay": [r"length.*stay|\blos\b"],
    "cost": [r"cost|billing|charge|payment|amount"],
}
_CAT_NAME_MAP = {
    "sex": [r"sex|gender"],
    "diagnosis_code": [r"\bicd\b|diagnosis.*code"],
    "diagnosis_text": [r"diagnosis|dx"],
    "procedure_code": [r"\bcpt\b|procedure.*code"],
    "procedure_text": [r"procedure|surgery"],
    "medication": [r"medication|drug|rx"],
    "route": [r"route"],
    "smoking_status": [r"smok"],
    "alcohol_use": [r"alcohol|etoh"],
    "discharge_disposition": [r"discharge.*disposition|disposition"],
    "payer": [r"payer|insurance"],
    "appointment_dt": [r"appointment|schedule|appt|visit.*date|start.*time|checkin"],
    "no_show_flag": [r"no[_\s-]?show"],
    "readmission_flag": [r"readmission|readmit"],
    "mortality_flag": [r"death|expired|mortality"],
    "icu_admit_flag": [r"\bicu\b|critical.*care"],
    "sepsis_flag": [r"sepsis"],
    "aki_flag": [r"\baki\b|acute.*kidney"],
    "label": [r"\blabel\b|target|outcome|result"],
    "timestamp": [r"timestamp|datetime|time"],
    "date": [r"date$|^date$"]
}

def _regex_match(name: str, patterns: List[str]) -> bool:
    return any(re.search(p, name, flags=re.I) for p in patterns)

def _is_id_like(col: str) -> bool:
    return _regex_match(col, _ID_PATTERNS)

def _is_binary_like(series: pd.Series) -> bool:
    vals = series.dropna().unique()
    if len(vals) <= 1: 
        return False
    if len(vals) == 2:
        return True
    # also allow {0,1,2} but mostly 0/1
    vset = set(vals.tolist())
    return vset.issubset({0,1,True,False})

def _content_guess(col: str, s: pd.Series) -> Tuple[str, float, str]:
    """Content-driven guess with simple ranges and value heuristics."""
    name = col.lower()
    s_nonnull = s.dropna()
    ex = s_nonnull.head(3).tolist()

    # IDs
    if _is_id_like(name):
        return ("patient_id" if "patient" in name or "mrn" in name or "pid" in name else "encounter_id", 0.95, "ID-like name pattern")

    # Sex / Gender
    if s_nonnull.dtype == "O":
        top = [str(v).strip().lower() for v in s_nonnull.astype(str).head(50)]
        if any(v in {"m","f","male","female","other","nonbinary"} for v in top):
            return ("sex", 0.9, "Contains values like M/F/male/female")

    # Binary flags (outcome-ish)
    if _is_binary_like(s):
        if _regex_match(name, _CAT_NAME_MAP["no_show_flag"]): return ("no_show_flag", 0.9, "Binary and name suggests no-show")
        if _regex_match(name, _CAT_NAME_MAP["readmission_flag"]): return ("readmission_flag", 0.9, "Binary and readmission pattern")
        if _regex_match(name, _CAT_NAME_MAP["mortality_flag"]): return ("mortality_flag", 0.9, "Binary and mortality pattern")
        if _regex_match(name, _CAT_NAME_MAP["icu_admit_flag"]): return ("icu_admit_flag", 0.85, "Binary and ICU pattern")
        if _regex_match(name, _CAT_NAME_MAP["sepsis_flag"]): return ("sepsis_flag", 0.85, "Binary and sepsis pattern")
        if _regex_match(name, _CAT_NAME_MAP["aki_flag"]): return ("aki_flag", 0.85, "Binary and AKI pattern")
        return ("label", 0.6, "Binary distribution")

    # Numeric ranges
    if pd.api.types.is_numeric_dtype(s):
        q1, q3 = s_nonnull.quantile(0.25), s_nonnull.quantile(0.75)
        mn, mx = s_nonnull.min(), s_nonnull.max()
        rng = (mn, mx)

        if _regex_match(name, _NUM_NAME_MAP["age"]) or (0 <= mn <= 120 and mx <= 120):
            return ("age", 0.85, f"Range looks like age {rng}")
        if _regex_match(name, _NUM_NAME_MAP["systolic_bp"]) or (80 <= mn <= 200 and 100 <= mx <= 260):
            return ("systolic_bp", 0.7, f"Systolic-ish range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["diastolic_bp"]) or (40 <= mn <= 140 and 60 <= mx <= 180):
            return ("diastolic_bp", 0.7, f"Diastolic-ish range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["heart_rate"]) or (30 <= mn <= 200 and mx <= 250):
            return ("heart_rate", 0.65, f"HR-ish range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["temperature_c"]) or (30 <= mn <= 44):
            return ("temperature_c", 0.65, f"T in Celsius range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["spo2"]) or (80 <= mn <= 100):
            return ("spo2", 0.6, f"SpO2-ish {rng}")
        if _regex_match(name, _NUM_NAME_MAP["glucose"]) or (40 <= mn and mx <= 1000):
            return ("glucose", 0.65, f"Glucose-like range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["hba1c"]) or (3 <= mn and mx <= 20):
            return ("hba1c", 0.65, f"HbA1c-like range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["creatinine"]) or (0.1 <= mn and mx <= 20):
            return ("creatinine", 0.65, f"Creatinine-like range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["egfr"]) or (1 <= mn and mx <= 200):
            return ("egfr", 0.6, f"eGFR-like range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["length_of_stay"]) or (0 <= mn and mx <= 365):
            return ("length_of_stay", 0.6, f"LOS-like range {rng}")
        if _regex_match(name, _NUM_NAME_MAP["cost"]) or (mx > 100 and s_nonnull.mean() > 50):
            return ("cost", 0.55, f"Cost-like magnitude {rng}")

    # Coded fields and other cats
    if _regex_match(name, _CAT_NAME_MAP["diagnosis_code"]):
        return ("diagnosis_code", 0.9, "ICD-like name")
    if _regex_match(name, _CAT_NAME_MAP["procedure_code"]):
        return ("procedure_code", 0.9, "CPT-like name")
    if _regex_match(name, _CAT_NAME_MAP["diagnosis_text"]):
        return ("diagnosis_text", 0.7, "Diagnosis text pattern")
    if _regex_match(name, _CAT_NAME_MAP["procedure_text"]):
        return ("procedure_text", 0.7, "Procedure text pattern")
    if _regex_match(name, _CAT_NAME_MAP["medication"]):
        return ("medication", 0.7, "Medication pattern")
    if _regex_match(name, _CAT_NAME_MAP["route"]):
        return ("route", 0.6, "Routes pattern")
    if _regex_match(name, _CAT_NAME_MAP["smoking_status"]):
        return ("smoking_status", 0.7, "Smoking pattern")
    if _regex_match(name, _CAT_NAME_MAP["alcohol_use"]):
        return ("alcohol_use", 0.6, "Alcohol pattern")
    if _regex_match(name, _CAT_NAME_MAP["payer"]):
        return ("payer", 0.6, "Payer/insurance pattern")
    if _regex_match(name, _CAT_NAME_MAP["appointment_dt"]):
        return ("appointment_dt", 0.6, "Appointment/schedule pattern")
    if _regex_match(name, _CAT_NAME_MAP["timestamp"]):
        return ("timestamp", 0.55, "Timestamp pattern")
    if _regex_match(name, _CAT_NAME_MAP["date"]):
        return ("date", 0.55, "Date pattern")

    return ("other", 0.4, "Unrecognized; defaulting to other")


def _guess_specialty(columns: List[str]) -> str:
    s = [c.lower() for c in columns]
    if any(k in " ".join(s) for k in ["hba1c", "glucose"]): return "endocrinology"
    if any(k in " ".join(s) for k in ["systolic", "diastolic", "heart_rate", "cholesterol", "ldl", "hdl"]): return "cardiology"
    if any("spo2" in c or "resp" in c for c in s): return "pulmonology"
    if any("creatinine" in c or "egfr" in c or "bun" in c for c in s): return "nephrology"
    if any("icu" in c or "sepsis" in c for c in s): return "critical_care"
    if any("appointment" in c or "payer" in c or "cost" in c for c in s): return "operations"
    return "general"


def _data_quality(df: pd.DataFrame) -> Tuple[float, Dict[str, Any]]:
    if df is None or df.empty:
        return 0.0, {"completeness": 0.0, "duplicates": 0.0, "outlier_rate": 0.0}
    completeness = float(1.0 - df.isna().mean().mean())
    # duplicates (if patient_id present)
    dup_rate = 0.0
    pid = None
    for c in df.columns:
        if _is_id_like(c.lower()):
            pid = c
            break
    if pid is not None:
        dup_rate = float(1.0 - df[pid].nunique() / max(1, len(df)))

    # outlier rate (IQR per numeric col)
    out_rate_parts = []
    for c in df.select_dtypes(include=[np.number]).columns:
        s = df[c].dropna()
        if len(s) < 10: 
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        out_rate_parts.append(float(((s < lower) | (s > upper)).mean()))
    out_rate = float(np.mean(out_rate_parts)) if out_rate_parts else 0.0

    # Simple aggregate
    dq = max(0.0, min(1.0, 0.6 * completeness + 0.2 * (1 - dup_rate) + 0.2 * (1 - out_rate)))
    return dq, {
        "completeness": round(completeness, 3),
        "duplicates": round(dup_rate, 3),
        "outlier_rate": round(out_rate, 3)
    }


# ----------------------------- Public class -----------------------------

class IntelligentColumnMapper:
    """
    Uses Gemini (when available) to infer semantic column types from a real sample,
    with a robust heuristic fallback (regex + content ranges).
    """

    async def analyze_medical_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        if df is None or df.empty:
            return {
                "column_mappings": {},
                "medical_specialty": "general",
                "data_quality_score": 0.0,
                "quality_breakdown": {"completeness": 0.0, "duplicates": 0.0, "outlier_rate": 0.0},
                "suggested_analyses": ["risk_prediction"]
            }

        # Prepare sample for LLM
        sample = {}
        for c in df.columns:
            vals = df[c].dropna().head(10).tolist()
            # Keep values JSON-serializable
            sample[str(c)] = [self._safe_val(v) for v in vals]

        payload = {
            "column_names": list(map(str, df.columns.tolist())),
            "sample": sample,
            "notes": "Infer healthcare semantics. Prefer specific clinical features when confident."
        }

        # Try Gemini
        genai = _gemini_client()
        if genai is not None:
            try:
                model = genai.GenerativeModel("gemini-1.5-pro")
                resp = model.generate_content(_GEMINI_MAPPING_PROMPT + "\n\n" + json.dumps(payload))
                text = getattr(resp, "text", None) or (
                    resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else None
                )
                if text:
                    text = text.strip()
                    if text.startswith("```"):
                        text = text.strip("`")
                        if text.startswith("json"):
                            text = text[4:].strip()
                    parsed = json.loads(text)
                    if isinstance(parsed, dict) and "column_mappings" in parsed:
                        # Normalize: add source flag
                        for k, v in parsed.get("column_mappings", {}).items():
                            v.setdefault("confidence", 0.7)
                            v.setdefault("rationale", "LLM-inferred")
                            v["source"] = "gemini"
                        dq, breakdown = _data_quality(df)
                        return {
                            "column_mappings": parsed["column_mappings"],
                            "medical_specialty": parsed.get("medical_specialty", _guess_specialty(df.columns.tolist())),
                            "data_quality_score": round(dq, 3),
                            "quality_breakdown": breakdown,
                            "suggested_analyses": parsed.get("suggested_analyses", ["risk_prediction","anomaly_detection"])
                        }
            except Exception:
                # fall through to heuristic
                pass

        # Heuristic fallback (regex + content)
        mappings: Dict[str, Any] = {}
        for c in df.columns:
            dtype = df[c].dtype
            detected, conf, why = _content_guess(str(c), df[c])
            mappings[str(c)] = {
                "detected_type": detected,
                "confidence": round(float(conf), 3),
                "rationale": why,
                "examples": [self._safe_val(v) for v in df[c].dropna().head(3).tolist()],
                "source": "heuristic"
            }

        dq, breakdown = _data_quality(df)
        return {
            "column_mappings": mappings,
            "medical_specialty": _guess_specialty(df.columns.tolist()),
            "data_quality_score": round(dq, 3),
            "quality_breakdown": breakdown,
            "suggested_analyses": self._suggest_analyses(mappings)
        }

    # ------------------------- small utils -------------------------

    @staticmethod
    def _safe_val(v: Any) -> Any:
        if isinstance(v, (np.generic,)):
            return v.item()
        try:
            json.dumps(v)
            return v
        except Exception:
            return str(v)

    @staticmethod
    def _suggest_analyses(mappings: Dict[str, Any]) -> List[str]:
        types = {m["detected_type"] for m in mappings.values()}
        out = ["risk_prediction"]
        if {"systolic_bp", "diastolic_bp", "spo2", "heart_rate"} & types:
            out.append("critical_care_early_warning")
        if {"readmission_flag", "no_show_flag", "cost"} & types:
            out.append("operations")
        out.append("anomaly_detection")
        if len(out) > 1:
            out.append("population_health")
        # de-dupe while preserving order
        seen, res = set(), []
        for x in out:
            if x not in seen:
                res.append(x); seen.add(x)
        return res
