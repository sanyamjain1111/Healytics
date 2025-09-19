from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class UploadResponse(BaseModel):
    dataset_id: str | int
    rows: int
    columns: int
    message: str


class AIAnalysisRequest(BaseModel):
    dataset_id: int
    analysis_goal: str = "auto"


class AIAnalysisResponse(BaseModel):
    analysis_id: str
    ai_strategy: Dict[str, Any]
    model_execution_results: Dict[str, Any]
    clinical_insights: Dict[str, Any]
    visualizations: Dict[str, Any]
    export_packages: Dict[str, str]


# ---- New schemas used by updated routes ----

class StrategyGenerateRequest(BaseModel):
    dataset_id: int
    preset_id: Optional[str] = None
    objective: Optional[str] = "Optimize clinical risk and anomaly detection with explainable outputs."


class StrategyGenerateResponse(BaseModel):
    strategy: Dict[str, Any]


class AnalysisRunRequest(BaseModel):
    dataset_id: int
    strategy_id: Optional[int] = None


class AnalysisRunResponse(BaseModel):
    risk_json: str
    anomaly_json: str
    summary: Dict[str, Any]


class AdhocPredictRequest(BaseModel):
    dataset_id: int
    patient_id: Optional[str] = None
    patient: Optional[Dict[str, Any]] = None
    strategy_id: Optional[int] = None


class AdhocPredictResponse(BaseModel):
    patient_id: str
    predictions: Dict[str, Any]
    strategy_id: Optional[int] = None
