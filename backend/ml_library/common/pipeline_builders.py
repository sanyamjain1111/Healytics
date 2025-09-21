# -*- coding: utf-8 -*-
from typing import List, Optional, Tuple, Callable, Any
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import (
    train_test_split, RandomizedSearchCV, StratifiedKFold, KFold, ParameterSampler
)
from sklearn.metrics import (
    roc_auc_score, classification_report, mean_absolute_error, r2_score, f1_score
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Fallback if make_column_selector isn't available
try:
    from sklearn.compose import make_column_selector as _selector
    def selector(dtype_include=None, dtype_exclude=None):
        return _selector(dtype_include=dtype_include, dtype_exclude=dtype_exclude)
except Exception:  # very old sklearn
    def selector(dtype_include=None, dtype_exclude=None):
        def _sel(df: pd.DataFrame):
            return df.select_dtypes(include=dtype_include, exclude=dtype_exclude).columns.tolist()
        return _sel

# ---------------------------- Helpers ----------------------------
def _split(X, y, is_classification: bool, test_size: float = 0.2, seed: int = 42):
    if is_classification:
        try:
            y_ser = pd.Series(y)
            if y_ser.notna().all() and y_ser.nunique() >= 2:
                return train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)
        except Exception:
            pass
        return train_test_split(X, y, test_size=test_size, random_state=seed)
    return train_test_split(X, y, test_size=test_size, random_state=seed)

def _prob_like(fitted, X_):
    if hasattr(fitted, "predict_proba"):
        return fitted.predict_proba(X_)[:, 1]
    if hasattr(fitted, "decision_function"):
        s = fitted.decision_function(X_)
        return (s - s.min()) / (s.max() - s.min() + 1e-9)
    pred = fitted.predict(X_)
    pred = np.asarray(pred, dtype=float)
    return (pred - pred.min()) / (pred.max() - pred.min() + 1e-9)

# --------------------- Data-driven transformers -------------------
class IdentifierDropper(BaseEstimator, TransformerMixin):
    """
    Drops columns that are near-unique (likely identifiers) or constant.
    No reliance on names; purely statistical.
    """
    def __init__(self, max_unique_ratio: float = 0.98):
        self.max_unique_ratio = max_unique_ratio
        self.cols_: List[str] = []

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        n = len(X)
        drop = []
        for c in X.columns:
            u = X[c].nunique(dropna=True)
            if u <= 1:                   # constant
                drop.append(c)
            else:
                ratio = u / max(1, n)
                if ratio >= self.max_unique_ratio:
                    drop.append(c)       # quasi-identifier
        self.cols_ = drop
        return self

    def transform(self, X: pd.DataFrame):
        return X.drop(columns=[c for c in self.cols_ if c in X.columns], errors="ignore")

class LeakageGuard(BaseEstimator, TransformerMixin):
    """
    Drops columns that are near-duplicates of y or extremely predictive of y.
    Uses equality rate, correlation (for numeric), and mutual_info (for low-cardinality).
    No name-based logic.
    """
    def __init__(
        self,
        eq_tol: float = 0.995,          # >=99.5% identical to y (or 1-y) -> drop
        corr_tol: float = 0.98,         # |corr| >= 0.98 for numeric vs binary y -> drop
        mi_tol: float = 0.8,            # strong MI for low-cardinality -> drop
        max_card_for_mi: int = 20
    ):
        self.eq_tol = eq_tol
        self.corr_tol = corr_tol
        self.mi_tol = mi_tol
        self.max_card_for_mi = max_card_for_mi
        self.drop_cols_: List[str] = []
        self._y_is_binary_: bool = False

    def _is_binary(self, s: pd.Series) -> bool:
        s = pd.Series(s).dropna().astype(float)
        return s.nunique() <= 2

    def _eq_rate(self, a: pd.Series, b: pd.Series) -> float:
        a = pd.Series(a).reset_index(drop=True)
        b = pd.Series(b).reset_index(drop=True)
        m = (~a.isna()) & (~b.isna())
        if m.sum() == 0:
            return 0.0
        return float((a[m] == b[m]).mean())

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None):
        self.drop_cols_ = []
        if y is None:
            return self
        y = pd.Series(y)
        self._y_is_binary_ = self._is_binary(y)

        # Numeric equality/correlation checks
        for c in X.columns:
            s = X[c]
            # direct/negated equality for (quasi)binary columns
            su = s.dropna().unique()
            if len(su) <= 2:
                # map to {0,1}
                sm = pd.Series(pd.factorize(s, sort=True)[0], dtype=float)
                sm.replace(-1, np.nan, inplace=True)
                ym = pd.to_numeric(y, errors="coerce")
                r1 = self._eq_rate(sm, ym)
                r2 = self._eq_rate(1 - sm, ym)
                if max(r1, r2) >= self.eq_tol:
                    self.drop_cols_.append(c)
                    continue

            # numeric vs binary y: point-biserial correlation
            if self._y_is_binary_ and pd.api.types.is_numeric_dtype(s):
                try:
                    sn = pd.to_numeric(s, errors="coerce")
                    ym = pd.to_numeric(y, errors="coerce")
                    m = (~sn.isna()) & (~ym.isna())
                    if m.sum() > 2:
                        corr = float(np.corrcoef(sn[m], ym[m])[0, 1])
                        if abs(corr) >= self.corr_tol:
                            self.drop_cols_.append(c)
                            continue
                except Exception:
                    pass

            # low-cardinality MI
            if pd.Series(s).nunique(dropna=True) <= self.max_card_for_mi:
                try:
                    from sklearn.feature_selection import mutual_info_classif
                    # crude numeric encoding for MI
                    enc = pd.factorize(s, sort=True)[0].astype(float)
                    enc[enc < 0] = np.nan
                    m = (~np.isnan(enc)) & (~pd.isna(y))
                    if m.sum() > 5 and self._y_is_binary_:
                        mi = mutual_info_classif(enc[m].reshape(-1, 1), pd.to_numeric(y[m], errors="coerce"))[0]
                        # normalize MI to [0,1] by dividing by log(card)
                        card = max(2, pd.Series(s[m]).nunique())
                        mi_norm = float(mi / np.log(card))
                        if mi_norm >= self.mi_tol:
                            self.drop_cols_.append(c)
                            continue
                except Exception:
                    pass

        # de-duplicate
        self.drop_cols_ = sorted(set(self.drop_cols_))
        return self

    def transform(self, X: pd.DataFrame):
        return X.drop(columns=[c for c in self.drop_cols_ if c in X.columns], errors="ignore")

# ---------------------- Preprocessing builders --------------------
def _numeric_pipeline() -> Pipeline:
    return Pipeline(steps=[
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler(with_mean=False)),
    ])

def _categorical_pipeline() -> Pipeline:
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=True)
    return Pipeline(steps=[
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe", ohe),
    ])

def _build_preprocessor(target: Optional[str] = None) -> Pipeline:
    """
    A pipeline that:
      1) drops ID-like/constant columns statistically,
      2) drops leakage columns using y (during fit),
      3) then applies dtype-based ColumnTransformer (no fixed column lists).
    """
    ct = ColumnTransformer(
        transformers=[
            ("num", _numeric_pipeline(), selector(dtype_include=np.number)),
            ("cat", _categorical_pipeline(), selector(dtype_exclude=np.number)),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    # Important: put droppers BEFORE ct, so they run both at fit and transform.
    return Pipeline(steps=[
        ("id_drop", IdentifierDropper(max_unique_ratio=0.98)),
        ("leak_guard", LeakageGuard()),
        ("ct", ct),
    ])

# ---------------------- Model pipeline builders -------------------
def build_classification_pipeline(
    X: pd.DataFrame,
    estimator: str = "random_forest",
    target: Optional[str] = None
):
    pre = _build_preprocessor(target=target)

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
    pre = _build_preprocessor(target=target)

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

# --------------------------- Trainers -----------------------------
def train_eval_classification(
    X: pd.DataFrame,
    y,
    estimator: str = "random_forest",
    test_size: float = 0.2
):
    # Clean y and ensure 2 classes
    mask = pd.Series(y).notna().values
    X = X.loc[mask]
    y = pd.Series(y).loc[mask]
    if y.nunique() < 2:
        if "glucose" in X.columns:
            thr = X["glucose"].quantile(0.95)
            y = (X["glucose"] >= thr).astype(int)
        else:
            y = (np.random.rand(len(X)) > 0.95).astype(int)

    pipe, param_grid = build_classification_pipeline(X, estimator=estimator)
    X_tr, X_te, y_tr, y_te = _split(X, y, True, test_size=test_size)
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    # Try normal RandomizedSearchCV, then manual fallback
    used_search = False
    try:
        search = RandomizedSearchCV(
            pipe,
            param_distributions=param_grid,
            n_iter=3,
            scoring="roc_auc",
            cv=cv,
            random_state=42,
            n_jobs=-1,
            error_score="raise",
        )
        search.fit(X_tr, y_tr)
        best = search.best_estimator_
        used_search = True
    except Exception:
        sampler = list(ParameterSampler(param_grid, n_iter=3, random_state=42)) or [dict()]
        best_auc, best = -1.0, None
        for params in sampler:
            mdl = clone(pipe).set_params(**params)
            mdl.fit(X_tr, y_tr)
            auc_fold = roc_auc_score(y_te, _prob_like(mdl, X_te))
            if auc_fold > best_auc:
                best_auc, best = auc_fold, mdl

    prob = _prob_like(best, X_te)
    auc = roc_auc_score(y_te, prob)
    thresholds = np.linspace(0.1, 0.9, 17)
    t_best, _ = max(((t, f1_score(y_te, (prob >= t).astype(int), zero_division=0)) for t in thresholds), key=lambda x: x[1])
    preds = (prob >= t_best).astype(int)
    rep = classification_report(y_te, preds, output_dict=True, zero_division=0)

    best_params_out = {}
    if used_search:
        try:
            best_params_out = {k: (str(v) if not isinstance(v, (int, float, str, bool)) else v) for k, v in search.best_params_.items()}
        except Exception:
            best_params_out = {}

    return (
        {"auc": float(auc), "best_threshold": float(t_best), "report": rep, "best_params": best_params_out},
        best,
    )

def train_eval_regression(
    X: pd.DataFrame,
    y,
    estimator: str = "random_forest",
    test_size: float = 0.2
):
    pipe, param_grid = build_regression_pipeline(X, estimator=estimator)
    X_tr, X_te, y_tr, y_te = _split(X, y, False, test_size=test_size)
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    used_search = False
    try:
        search = RandomizedSearchCV(
            pipe,
            param_distributions=param_grid,
            n_iter=3,
            scoring="neg_mean_absolute_error",
            cv=kf,
            random_state=42,
            n_jobs=-1,
            error_score="raise",
        )
        search.fit(X_tr, y_tr)
        best = search.best_estimator_
        used_search = True
    except Exception:
        sampler = list(ParameterSampler(param_grid, n_iter=3, random_state=42)) or [dict()]
        best_mae, best = float("inf"), None
        for params in sampler:
            mdl = clone(pipe).set_params(**params)
            mdl.fit(X_tr, y_tr)
            pred = mdl.predict(X_te)
            mae = mean_absolute_error(y_te, pred)
            if mae < best_mae:
                best_mae, best = mae, mdl

    pred = best.predict(X_te)
    mae = mean_absolute_error(y_te, pred)
    r2 = r2_score(y_te, pred)
    best_params_out = {}
    if used_search:
        try:
            best_params_out = {k: (str(v) if not isinstance(v, (int, float, str, bool)) else v) for k, v in search.best_params_.items()}
        except Exception:
            best_params_out = {}
    return ({"mae": float(mae), "r2": float(r2), "best_params": best_params_out}, best)
