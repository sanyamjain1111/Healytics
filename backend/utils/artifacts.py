
import json
from pathlib import Path
from typing import Dict, Any
import numpy as np
import joblib
import shap
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

from ..paths import ARTIFACT_DIR, REPORT_DIR

def _safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-","_") else "_" for c in name)

def save_model_artifacts(model_name: str, best_estimator, X_test, metrics: Dict[str, Any]) -> Dict[str, str]:
    mname = _safe_name(model_name)
    out_dir = ARTIFACT_DIR / mname
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save metrics
    metrics_path = out_dir / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    # Save model
    model_path = out_dir / "best_model.joblib"
    joblib.dump(best_estimator, model_path)

    # SHAP summary
    shap_png = out_dir / "shap_summary.png"
    try:
        # If pipeline, get preprocessor & clf
        clf = best_estimator
        X_trans = None
        try:
            pre = best_estimator.named_steps.get("pre")
            clf = best_estimator.named_steps.get("clf", best_estimator)
            X_trans = pre.transform(X_test)
        except Exception:
            # Not a pipeline
            X_trans = X_test

        # Use a sample for performance
        if hasattr(X_trans, "toarray"):
            X_mat = X_trans[:2000]
        else:
            X_mat = np.array(X_trans)[:2000]

        explainer = shap.Explainer(clf)
        shap_values = explainer(X_mat)
        shap.summary_plot(shap_values, show=False)
        plt.tight_layout()
        plt.savefig(shap_png, dpi=160)
        plt.close()
    except Exception as e:
        with open(out_dir / "shap_error.txt", "w") as f:
            f.write(str(e))

    return {
        "metrics": str(metrics_path),
        "model": str(model_path),
        "shap": str(shap_png) if shap_png.exists() else ""
    }
