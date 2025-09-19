
from ..base_medical_model import BaseMedicalModel
from typing import Dict, Any, Optional
import pandas as pd
from ..common.pipeline_builders import train_eval_classification

class _GenericClassifier(BaseMedicalModel):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = None, name: str = "GenericClassifier"):
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
            # fallbacks
            for col in ["label_readmit", "outcome"]:
                if col in df.columns:
                    target = col
                    target_series = df[col]
                    df = df.drop(columns=[col])
                    break
            else:
                return {"note": f"{self.name}: No target column available"}
        metrics, best = train_eval_classification(df, target_series, estimator=self.estimator)
        return {"model": self.name, **metrics}

class ReadmissionPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "label_readmit"):
        super().__init__(estimator, target, "ReadmissionPredictor")

class Readmission90DPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "label_readmit"):
        super().__init__(estimator, target, "Readmission90DPredictor")

class MortalityRiskModel(_GenericClassifier):
    def __init__(self, estimator: str = "xgboost", target: Optional[str] = "mortality_1y"):
        super().__init__(estimator, target, "MortalityRiskModel")

class ICUAdmissionPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "icu_admit"):
        super().__init__(estimator, target, "ICUAdmissionPredictor")

class SepsisEarlyWarning(_GenericClassifier):
    def __init__(self, estimator: str = "xgboost", target: Optional[str] = "sepsis_label"):
        super().__init__(estimator, target, "SepsisEarlyWarning")

class DiabetesComplicationRisk(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "dm_complication"):
        super().__init__(estimator, target, "DiabetesComplicationRisk")

class HypertensionControlPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "htn_uncontrolled"):
        super().__init__(estimator, target, "HypertensionControlPredictor")

class HeartFailure30DRisk(_GenericClassifier):
    def __init__(self, estimator: str = "xgboost", target: Optional[str] = "hf_30d"):
        super().__init__(estimator, target, "HeartFailure30DRisk")

class StrokeRiskPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "xgboost", target: Optional[str] = "stroke_label"):
        super().__init__(estimator, target, "StrokeRiskPredictor")

class COPDExacerbationPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "copd_exac"):
        super().__init__(estimator, target, "COPDExacerbationPredictor")

class AKIRiskPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "aki_label"):
        super().__init__(estimator, target, "AKIRiskPredictor")

class AdverseDrugEventPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "ade_label"):
        super().__init__(estimator, target, "AdverseDrugEventPredictor")

class NoShowAppointmentPredictor(_GenericClassifier):
    def __init__(self, estimator: str = "random_forest", target: Optional[str] = "no_show"):
        super().__init__(estimator, target, "NoShowAppointmentPredictor")
