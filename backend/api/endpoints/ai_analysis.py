
from fastapi import APIRouter, HTTPException, Body
from ...models.analysis_schemas import AIAnalysisRequest
from ...core.ai_orchestrator import AIOrchestrator
import pandas as pd

router = APIRouter(prefix="/ai-analysis", tags=["AI Analysis"])

@router.post("")
async def run_ai_analysis(payload: AIAnalysisRequest = Body(...)):
    # For demo, load a sample already on disk (join of patients + outcomes)
    try:
        df = pd.read_csv("/mnt/data/medical-intellianalytics-pro/data/joined_training_sample.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sample data not found: {e}")
    result = await AIOrchestrator().process_dataset(df, {"specialty": "general"})
    return result
