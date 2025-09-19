from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

def head_sample(df: pd.DataFrame, limit: int = 50) -> Dict[str, Any]:
    sub = df.head(limit).astype(object).where(pd.notna(df.head(limit)), None)
    return {"columns": list(sub.columns), "rows": sub.values.tolist()}

# add at top
import json


def _coerce_hashable(s: pd.Series) -> pd.Series:
    """Turn dict/list/set cells into JSON strings so nunique/describe work."""
    if s.dtype == "object":
        if s.map(lambda v: isinstance(v, (dict, list, set))).any():
            return s.map(lambda v: json.dumps(v, default=str) if isinstance(v, (dict, list, set)) else v)
    return s

def dataframe_overview(df: pd.DataFrame) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    meta = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "missing_pct": float(df.isna().mean().mean()) if len(df) else 0.0,
    }

    numeric, categorical = [], []
    for c in df.columns:
        s = _coerce_hashable(df[c])
        try:
            nunique = int(s.nunique(dropna=True))
        except TypeError:
            # ultimate fallback
            nunique = int(s.astype(str).nunique(dropna=True))

        if pd.api.types.is_numeric_dtype(s):
            d = s.describe(percentiles=[0.25, 0.5, 0.75])
            numeric.append({
                "column": c,
                "count": int(d.get("count", 0)),
                "mean": float(d.get("mean", np.nan)) if pd.notna(d.get("mean", np.nan)) else None,
                "std": float(d.get("std", np.nan)) if pd.notna(d.get("std", np.nan)) else None,
                "min": float(d.get("min", np.nan)) if pd.notna(d.get("min", np.nan)) else None,
                "q25": float(d.get("25%", np.nan)) if pd.notna(d.get("25%", np.nan)) else None,
                "median": float(d.get("50%", np.nan)) if pd.notna(d.get("50%", np.nan)) else None,
                "q75": float(d.get("75%", np.nan)) if pd.notna(d.get("75%", np.nan)) else None,
                "max": float(d.get("max", np.nan)) if pd.notna(d.get("max", np.nan)) else None,
                "unique": nunique,
            })
        else:
            categorical.append({
                "column": c,
                "unique": nunique,
                "top": s.mode(dropna=True).iloc[0] if nunique and not s.mode(dropna=True).empty else None,
                "missing": int(s.isna().sum()),
            })

    return meta, numeric, categorical


def _safe_float(x) -> Optional[float]:
    try:
        if x is None:
            return None
        v = float(x)
        if np.isnan(v) or np.isinf(v):
            return None
        return v
    except Exception:
        return None

def histograms_for_columns(df: pd.DataFrame, columns: Optional[List[str]] = None, bins: int = 20) -> List[Dict[str, Any]]:
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()[:10]
    out = []
    for c in columns:
        if c not in df.columns:
            continue
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        if len(s) == 0:
            continue
        counts, bin_edges = np.histogram(s.values, bins=bins)
        out.append({
            "column": c,
            "bins": bin_edges.tolist(),
            "counts": counts.tolist()
        })
    return out

def duckdb_query(df: pd.DataFrame, sql: str) -> Tuple[List[str], List[List[Any]]]:
    import duckdb
    con = duckdb.connect()
    con.register("data", df)
    try:
        res = con.execute(sql).fetchdf()
    finally:
        con.close()
    cols = list(res.columns)
    # Convert NaNs to None for JSON serialization
    rows = res.astype(object).where(pd.notna(res), None).values.tolist()
    return cols, rows