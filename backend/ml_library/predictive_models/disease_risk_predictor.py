
from ..base_medical_model import BaseMedicalModel
from typing import Dict, Any, Optional
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import roc_auc_score, classification_report
from imblearn.over_sampling import SMOTE

class DiseaseRiskPredictor(BaseMedicalModel):
    def __init__(self, estimator: str = "random_forest"):
        self.estimator_name = estimator

    def _build_estimator(self):
        # Using RandomForest for portability; XGBoost selectable if installed
        if self.estimator_name.lower() == "xgboost":
            from xgboost import XGBClassifier
            return XGBClassifier(objective="binary:logistic", eval_metric="logloss", n_estimators=300)
        return RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42)

    async def fit_and_evaluate(self, X, y) -> Dict[str, Any]:
        # Identify cols
        num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = [c for c in X.columns if c not in num_cols]

        # Preprocess: impute, scale/encode
        num_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        cat_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("enc", OneHotEncoder(handle_unknown="ignore"))
        ])
        pre = ColumnTransformer([("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)])

        est = self._build_estimator()
        pipe = Pipeline([("pre", pre), ("clf", est)])

        # Train/test split (stratified 80/20)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

        # SMOTE on the transformed numeric subset is tricky in a pipeline; do a simple approach on raw (num-only) if binary
        # For simplicity, skip SMOTE here to keep pipeline consistent and robust across environments.

        param_grid = {
            "clf__n_estimators": [200, 300, 400] if self.estimator_name != "xgboost" else [200, 300],
        } if self.estimator_name != "xgboost" else {
            "clf__n_estimators": [200, 300],
            "clf__max_depth": [4, 6, 8, None]
        }

        search = RandomizedSearchCV(
            pipe, param_distributions=param_grid, n_iter=3, scoring="roc_auc", cv=3, random_state=42, n_jobs=-1
        )
        search.fit(X_train, y_train)
        best = search.best_estimator_
        proba = best.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, proba)
        report = classification_report(y_test, best.predict(X_test), output_dict=True)
        return {"auc": float(auc), "report": report, "best_params": search.best_params_}
