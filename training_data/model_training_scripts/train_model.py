
import argparse, json, importlib
import pandas as pd
from pathlib import Path
from training_data.utils.derive_targets import add_or_update_targets

def load_data():
    # Prefer the joined sample; fallback to patients-only
    p = Path("data/joined_training_sample.csv")
    if p.exists():
        df = pd.read_csv(p)
    else:
        df = pd.read_csv("data/patients.csv")
    return add_or_update_targets(df)

def main(model_name: str, estimator: str, target: str = None, outdir: str = "training_outputs"):
    from backend.ml_library.model_factory import DynamicModelFactory
    df = load_data()
    X = df.copy()
    if target and target in X.columns:
        y = X[target]
        X = X.drop(columns=[target])
    else:
        y = None  # let model pick fallback or synth

    # Instantiate model
    module_path = DynamicModelFactory.MODEL_REGISTRY.get(model_name)
    if not module_path:
        raise SystemExit(f"Unknown model: {model_name}")
    module = importlib.import_module(module_path)
    cls = getattr(module, model_name)
    model = cls(estimator=estimator, target=target)

    import asyncio
    res = asyncio.run(model.fit_and_evaluate(X, y))
    Path(outdir).mkdir(parents=True, exist_ok=True)
    with open(Path(outdir)/f"{model_name}_metrics.json", "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Model class name from registry")
    ap.add_argument("--estimator", default="random_forest", help="random_forest|xgboost|elasticnet (reg)" )
    ap.add_argument("--target", default=None, help="Optional target column name" )
    ap.add_argument("--outdir", default="training_outputs", help="Output directory for metrics/artifacts" )
    args = ap.parse_args()
    main(args.model, args.estimator, args.target, args.outdir)
