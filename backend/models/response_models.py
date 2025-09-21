from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class PatientSearchResponse(BaseModel):
    patient_profile: Dict[str, Any]
    current_status: Dict[str, Any]
    historical_analyses: List[Dict[str, Any]] = []
    risk_predictions: List[Dict[str, Any]] = []
    clinical_recommendations: List[Dict[str, Any]] = []


# ---- Optional: small DTOs for UI convenience ----

class DatasetSummary(BaseModel):
    id: int
    name: str
    n_rows: int
    n_cols: int
    created_at: Optional[str] = None


class StrategyDTO(BaseModel):
    id: int
    dataset_id: int
    parsed: Dict[str, Any]
    raw_text: Optional[str] = None


class AnalysisArtifact(BaseModel):
    id: Optional[int] = None
    dataset_id: int
    strategy_id: Optional[int] = None
    kind: str  # 'risk' or 'anomaly'
    artifact_path: str
    summary: Dict[str, Any]
