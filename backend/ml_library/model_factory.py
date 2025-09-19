
from typing import Dict, Any
import importlib

class DynamicModelFactory:
    MODEL_REGISTRY = {
        # Classification (risk) models
        "DiseaseRiskPredictor": "backend.ml_library.predictive_models.disease_risk_predictor",
        "ClinicalAnomalyDetector": "backend.ml_library.diagnostic_models.clinical_anomaly_detector",
        "ReadmissionPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "Readmission90DPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "MortalityRiskModel": "backend.ml_library.predictive_models.clinical_risk_models",
        "ICUAdmissionPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "SepsisEarlyWarning": "backend.ml_library.predictive_models.clinical_risk_models",
        "DiabetesComplicationRisk": "backend.ml_library.predictive_models.clinical_risk_models",
        "HypertensionControlPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "HeartFailure30DRisk": "backend.ml_library.predictive_models.clinical_risk_models",
        "StrokeRiskPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "COPDExacerbationPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "AKIRiskPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "AdverseDrugEventPredictor": "backend.ml_library.predictive_models.clinical_risk_models",
        "NoShowAppointmentPredictor": "backend.ml_library.predictive_models.clinical_risk_models",

        # Regression models
        "LengthOfStayRegressor": "backend.ml_library.regression_models.clinical_regression_models",
        "CostOfCareRegressor": "backend.ml_library.regression_models.clinical_regression_models",
        "AnemiaSeverityRegressor": "backend.ml_library.regression_models.clinical_regression_models"
    }

    async def create_models_from_strategy(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        instances = {}
        for cfg in strategy.get("model_execution_plan", {}).get("primary_models", []):
            name = cfg["model_name"]
            params = cfg.get("parameters", {})
            module_path = self.MODEL_REGISTRY.get(name)
            if not module_path:
                instances[name] = {"instance": None, "config": cfg}
                continue
            module = importlib.import_module(module_path)
            cls = getattr(module, name)
            instances[name] = {"instance": cls(**params), "config": cfg}
        return instances
