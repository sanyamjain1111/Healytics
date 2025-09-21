# backend/utils/artifacts.py
from pathlib import Path
from typing import Dict, Any
import json
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ..paths import ARTIFACT_DIR, REPORT_DIR

def _safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-","_") else "_" for c in name)

def save_model_artifacts(model_name: str, pipeline, X_te, metrics: Dict[str, Any]) -> Dict[str, str]:
    """
    Save the fitted pipeline as .joblib, metrics as JSON, and a SHAP-like
    global importance plot if feasible. Returns artifact paths.
    """
    name = _safe_name(model_name)

    model_dir   = (ARTIFACT_DIR / "models");  model_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir = (ARTIFACT_DIR / "metrics"); metrics_dir.mkdir(parents=True, exist_ok=True)
    explain_dir = (ARTIFACT_DIR / "explain"); explain_dir.mkdir(parents=True, exist_ok=True)

    model_path   = model_dir   / f"{name}.joblib"
    metrics_path = metrics_dir / f"{name}_metrics.json"
    shap_png     = explain_dir / f"{name}_summary.png"

    # 1) Save fitted pipeline
    joblib.dump(pipeline, model_path)

    # 2) Save metrics
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # 3) Best-effort global importance plot (tree-based → feature importances)
    try:
        # Try to pull the final estimator; fall back to attribute search
        final_est = getattr(pipeline, "named_steps", {}).get("model", None)
        if final_est is None:
            # pipeline could be just estimator
            final_est = pipeline

        importances = getattr(final_est, "feature_importances_", None)
        if importances is not None:
            # We won’t reconstruct exact feature names here; plot top-20 magnitudes
            idx = np.argsort(importances)[::-1][:20]
            vals = np.array(importances)[idx]
            xs = np.arange(len(idx))
            plt.figure(figsize=(6,4))
            plt.bar(xs, vals)
            plt.title(f"{model_name} – Top Feature Importances")
            plt.tight_layout()
            plt.savefig(shap_png, dpi=160)
            plt.close()
    except Exception as e:
        # Don’t fail the run for plotting issues
        with open(explain_dir / f"{name}_explain_error.txt", "w") as f:
            f.write(str(e))

    return {
        "metrics": str(metrics_path),
        "model": str(model_path),
        "explain": str(shap_png) if shap_png.exists() else ""
    }
