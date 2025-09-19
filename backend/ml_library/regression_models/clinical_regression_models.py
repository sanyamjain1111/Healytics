
from ..base_medical_model import BaseMedicalModel
from typing import Dict, Any, Optional
import pandas as pd
from ..common.pipeline_builders import train_eval_regression

class _GenericRegressor(BaseMedicalModel):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = None, name: str = "GenericRegressor"):
        self.estimator = estimator
        self.target = target
        self.name = name

    async def fit_and_evaluate(self, X, y=None) -> Dict[str, Any]:
        df = pd.DataFrame(X)
        # Determine target
        target = self.target
        if y is not None:
            target_series = y
        elif target and target in df.columns:
            target_series = df[target]
            df = df.drop(columns=[target])
        else:
            return {"note": f"{self.name}: No regression target column available"}
        metrics, best = train_eval_regression(df, target_series, estimator=self.estimator)
        return {"model": self.name, **metrics}

class LengthOfStayRegressor(_GenericRegressor):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "los_days"):
        super().__init__(estimator, target, "LengthOfStayRegressor")

class CostOfCareRegressor(_GenericRegressor):
    def __init__(self, estimator: str = "elasticnet", target: Optional[str] = "cost_of_care"):
        super().__init__(estimator, target, "CostOfCareRegressor")

class AnemiaSeverityRegressor(_GenericRegressor):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "anemia_severity_score"):
        super().__init__(estimator, target, "AnemiaSeverityRegressor")
