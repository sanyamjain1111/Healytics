
from typing import Dict, Any, Optional
import pandas as pd
import importlib
from pathlib import Path
from ..ml_library.model_factory import DynamicModelFactory
from ..paths import ARTIFACT_DIR
from ..utils.artifacts import save_model_artifacts
from ..utils.reporting import generate_reports
from training_data.utils.derive_targets import add_or_update_targets
from sklearn.model_selection import train_test_split

def load_training_frame() -> pd.DataFrame:
    p = Path("/mnt/data/medical-intellianalytics-pro/data/joined_training_sample.csv")
    if p.exists():
        df = pd.read_csv(p)
    else:
        df = pd.read_csv("/mnt/data/medical-intellianalytics-pro/data/patients.csv")
    return add_or_update_targets(df)

async def train_model_api(model_name: str, estimator: str = "random_forest", target: Optional[str] = None) -> Dict[str, Any]:
    df = load_training_frame()
    X = df.copy()
    y = None
    if target and target in X.columns:
        y = X[target]
        X = X.drop(columns=[target])

    module_path = DynamicModelFactory.MODEL_REGISTRY.get(model_name)
    if not module_path:
        return {"error": f"Unknown model {model_name}"}
    module = importlib.import_module(module_path)
    cls = getattr(module, model_name)
    model = cls(estimator=estimator, target=target)

    import asyncio
    # Train while also capturing a test split for SHAP plotting
    if y is not None:
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        # Recombine for the model API (it does its own split internally), but keep X_te for SHAP
        res = await model.fit_and_evaluate(X, y)
        # Best estimator is not returned; re-train quickly on the split to extract fitted estimator
        # (We mimic the internal split/training to produce a "best" model; for a production system, refactor to return it)
        from ..ml_library.common.pipeline_builders import build_classification_pipeline
        pipe, _ = build_classification_pipeline(X, estimator=estimator)
        pipe.fit(X_tr, y_tr)
        artifacts = save_model_artifacts(model_name, pipe, X_te, res)
    else:
        res = await model.fit_and_evaluate(X, y)
        artifacts = {"metrics": "", "model": "", "shap": ""}

    reports = generate_reports(model_name, artifacts)
    return {"metrics": res, "artifacts": artifacts, "reports": reports}
