
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints.intelligent_upload import router as upload_router
from .api.endpoints.ai_analysis import router as analysis_router
from .api.endpoints.patient_search import router as patient_router
from .api.endpoints.report_generation import router as report_router
from .api.endpoints.models import router as models_router

app = FastAPI(title="Medical IntelliAnalytics Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from .api.routes.datasets import router as datasets_router
from .api.routes.patients import router as patients_router
from .api.routes.analytics import router as analytics_router
from .api.routes.strategies import router as strategies_router
from .api.routes.adhoc import router as adhoc_router
from .api.routes.reports import router as reports_router
# in your FastAPI app init (only once)
from fastapi.staticfiles import StaticFiles
from backend.api.routes import artifacts as artifacts_routes
app.include_router(artifacts_routes.router)

app.mount("/artifacts", StaticFiles(directory="artifacts"), name="artifacts")
app.include_router(reports_router)
app.include_router(adhoc_router,prefix="/adhoc", tags=["ad-hoc"])
app.include_router(datasets_router)
app.include_router(patients_router)
app.include_router(analytics_router)
app.include_router(strategies_router)

app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(patient_router)
app.include_router(report_router)
app.include_router(models_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
