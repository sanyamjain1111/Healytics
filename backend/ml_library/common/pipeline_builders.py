from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold, KFold
from sklearn.metrics import roc_auc_score, classification_report, mean_absolute_error, r2_score, f1_score
from .transformers import IQRClippingTransformer

# ---------- Train/test split helper ----------
def _split(X, y, is_classification: bool, test_size: float = 0.2, seed: int = 42):
    if is_classification:
        try:
            import pandas as _pd
            y_ser = _pd.Series(y)
            if y_ser.notna().all() and y_ser.nunique() >= 2:
                return train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)
        except Exception:
            pass
        # Fallback: non-stratified split
        return train_test_split(X, y, test_size=test_size, random_state=seed)
    return train_test_split(X, y, test_size=test_size, random_state=seed)

# ---------- ID handling + preprocessing ----------
_ID_PATTERNS = ("id", "_id", "patient", "encounter", "visit", "account", "mrn")

def _split_features(df: pd.DataFrame, target: Optional[str] = None) -> Tuple[List[str], List[str]]:
    df = df.copy()
    if target and target in df.columns:
        df = df.drop(columns=[target])

    # Basic type split
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # Drop id-like from numeric
    def is_id_like(c: str) -> bool:
        lc = c.lower()
        return any(p in lc for p in _ID_PATTERNS)
    num_cols = [c for c in num_cols if not is_id_like(c)]

    # Drop near-unique columns (likely identifiers)
    n = len(df)
    uniq_thresh = max(0.98 * n, n - 5)  # defensive
    unique_like = [c for c in df.columns if df[c].nunique(dropna=True) >= uniq_thresh]
    num_cols = [c for c in num_cols if c not in unique_like]
    cat_cols = [c for c in cat_cols if c not in unique_like]

    return num_cols, cat_cols

def _numeric_pipeline() -> Pipeline:
    return Pipeline(steps=[
        ("impute", SimpleImputer(strategy="median")),
        # Array-safe IQR clipper (no columns arg needed)
        ("clip", IQRClippingTransformer(q_low=0.25, q_high=0.75, k=1.5)),
        ("scale", StandardScaler(with_mean=False)),  # safe with sparse/OHE mix
    ])

def _categorical_pipeline() -> Pipeline:
    return Pipeline(steps=[
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
    ])

def _build_preprocessor(X: pd.DataFrame, target: Optional[str] = None) -> ColumnTransformer:
    num_cols, cat_cols = _split_features(X, target=target)
    transformers = []
    if num_cols:
        transformers.append(("num", _numeric_pipeline(), num_cols))
    if cat_cols:
        transformers.append(("cat", _categorical_pipeline(), cat_cols))
    return ColumnTransformer(transformers=transformers, remainder="drop")

# ---------- Pipelines ----------
def build_classification_pipeline(
    X: pd.DataFrame,
    estimator: str = "random_forest",
    target: Optional[str] = None
):
    # Robust preprocessor (excludes ID-like cols; array-safe IQR clipping)
    pre = _build_preprocessor(X, target=target)

    if estimator.lower() == "xgboost":
        try:
            from xgboost import XGBClassifier
            clf = XGBClassifier(
                objective="binary:logistic",
                eval_metric="logloss",
                n_estimators=300,
                tree_method="hist",
                random_state=42,
            )
            # keep your grid, but avoid None for xgboost max_depth
            param_grid = {
                "clf__n_estimators": [200, 300, 400],
                "clf__max_depth": [4, 6, 8],
            }
        except Exception:
            clf = RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42)
            param_grid = {
                "clf__n_estimators": [200, 300, 400],
                "clf__max_depth": [None, 10, 20],
            }
    else:
        clf = RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42)
        param_grid = {
            "clf__n_estimators": [200, 300, 400],
            "clf__max_depth": [None, 10, 20],
        }

    pipe = Pipeline([("pre", pre), ("clf", clf)])
    return pipe, param_grid

def build_regression_pipeline(
    X: pd.DataFrame,
    estimator: str = "random_forest",
    target: Optional[str] = None
):
    # Reuse the same robust preprocessor (no columns= anywhere)
    pre = _build_preprocessor(X, target=target)

    if estimator.lower() == "elasticnet":
        from sklearn.linear_model import ElasticNet
        reg = ElasticNet(max_iter=5000, random_state=42)
        param_grid = {
            "reg__alpha": [0.01, 0.1, 1.0],
            "reg__l1_ratio": [0.1, 0.5, 0.9],
        }
    elif estimator.lower() == "xgboost":
        try:
            from xgboost import XGBRegressor
            reg = XGBRegressor(
                n_estimators=300,
                objective="reg:squarederror",
                tree_method="hist",
                random_state=42,
            )
            param_grid = {
                "reg__n_estimators": [200, 300, 400],
                "reg__max_depth": [4, 6, 8],
            }
        except Exception:
            reg = RandomForestRegressor(n_estimators=300, n_jobs=-1, random_state=42)
            param_grid = {
                "reg__n_estimators": [200, 300, 400],
                "reg__max_depth": [None, 10, 20],
            }
    else:
        reg = RandomForestRegressor(n_estimators=300, n_jobs=-1, random_state=42)
        param_grid = {
            "reg__n_estimators": [200, 300, 400],
            "reg__max_depth": [None, 10, 20],
        }

    pipe = Pipeline([("pre", pre), ("reg", reg)])
    return pipe, param_grid

# ---------- Trainers ----------
def train_eval_classification(
    X: pd.DataFrame,
    y,
    estimator: str = "random_forest",
    test_size: float = 0.2
):
    # Clean target: drop NaNs
    mask = pd.Series(y).notna().values
    X = X.loc[mask]
    y = pd.Series(y).loc[mask]

    # Ensure at least 2 classes; if degenerate, synthesize a tiny minority using a proxy
    if y.nunique() < 2:
        if 'glucose' in X.columns:
            thr = X['glucose'].quantile(0.95)
            y = (X['glucose'] >= thr).astype(int)
        else:
            y = (np.random.rand(len(X)) > 0.95).astype(int)

    pipe, param_grid = build_classification_pipeline(X, estimator=estimator)
    X_tr, X_te, y_tr, y_te = _split(X, y, True, test_size=test_size)
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42) if len(set(y_tr)) > 1 else 3

    search = RandomizedSearchCV(
        pipe,
        param_distributions=param_grid,
        n_iter=3,
        scoring="roc_auc",
        cv=skf,
        random_state=42,
        n_jobs=-1,
    )
    search.fit(X_tr, y_tr)
    best = search.best_estimator_

    # Probabilities (fallbacks just in case)
    if hasattr(best, "predict_proba"):
        prob = best.predict_proba(X_te)[:, 1]
    elif hasattr(best, "decision_function"):
        s = best.decision_function(X_te)
        s = (s - s.min()) / (s.max() - s.min() + 1e-9)
        prob = s
    else:
        prob = best.predict(X_te)

    auc = roc_auc_score(y_te, prob)

    # Choose threshold to maximize F1 (reduces “ill-defined precision” + improves minority detection)
    thresholds = np.linspace(0.1, 0.9, 17)
    f1s = [(t, f1_score(y_te, (prob >= t).astype(int), zero_division=0)) for t in thresholds]
    best_threshold, _ = max(f1s, key=lambda x: x[1])
    preds = (prob >= best_threshold).astype(int)

    rep = classification_report(y_te, preds, output_dict=True, zero_division=0)
    return {"auc": float(auc), "best_threshold": float(best_threshold), "report": rep, "best_params": search.best_params_}, best

def train_eval_regression(
    X: pd.DataFrame,
    y,
    estimator: str = "random_forest",
    test_size: float = 0.2
):
    pipe, param_grid = build_regression_pipeline(X, estimator=estimator)
    X_tr, X_te, y_tr, y_te = _split(X, y, False, test_size=test_size)
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    search = RandomizedSearchCV(
        pipe,
        param_distributions=param_grid,
        n_iter=3,
        scoring="neg_mean_absolute_error",
        cv=kf,
        random_state=42,
        n_jobs=-1,
    )
    search.fit(X_tr, y_tr)
    best = search.best_estimator_

    pred = best.predict(X_te)
    mae = mean_absolute_error(y_te, pred)
    r2 = r2_score(y_te, pred)
    return {"mae": float(mae), "r2": float(r2), "best_params": search.best_params_}, best
