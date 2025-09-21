
from ..base_medical_model import BaseMedicalModel
from typing import Dict, Any
import numpy as np
from sklearn.ensemble import IsolationForest

class ClinicalAnomalyDetector(BaseMedicalModel):
    def __init__(self):
        self.model = IsolationForest(n_estimators=200, contamination=0.02, random_state=42)

    async def fit_and_evaluate(self, X, y=None) -> Dict[str, Any]:
        Xn = X.select_dtypes(include=[np.number]).fillna(X.median(numeric_only=True))
        self.model.fit(Xn)
        scores = self.model.score_samples(Xn).tolist()
        return {"anomaly_score_summary": {"min": float(min(scores)), "max": float(max(scores))}}
