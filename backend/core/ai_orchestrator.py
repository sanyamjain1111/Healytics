
import uuid, time
from typing import Dict, Any
import pandas as pd
from ..ai_services.column_mapper import IntelligentColumnMapper
from ..ai_services.gemini_strategist import GeminiStrategist
from ..ai_services.insight_generator import AIInsightGenerator
from ..ai_services.visualization_ai import VisualizationAI
from ..ml_library.model_factory import DynamicModelFactory

class AIOrchestrator:
    def __init__(self):
        self.column_mapper = IntelligentColumnMapper()
        self.gemini = GeminiStrategist()
        self.model_factory = DynamicModelFactory()
        self.insights = AIInsightGenerator()
        self.vis_ai = VisualizationAI()

    def _analyze_dataset_characteristics(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "rows": len(df),
            "cols": len(df.columns),
            "null_fraction": float(df.isna().mean().mean())
        }

    async def process_dataset(self, df: pd.DataFrame, medical_context: Dict[str, Any]) -> Dict[str, Any]:
        t0 = time.time()
        column_analysis = await self.column_mapper.analyze_medical_data(df)
        data_char = self._analyze_dataset_characteristics(df)

        strategy = await self.gemini.generate_comprehensive_strategy({
            "column_mapping": column_analysis,
            "dataset_characteristics": data_char,
            "medical_context": medical_context
        })

        models = await self.model_factory.create_models_from_strategy(strategy)
        model_results = {}
        target_col = None
        # naive selection for demo: pick first 'outcome'-like column
        for col, meta in column_analysis.get("column_mappings", {}).items():
            if "outcome" in str(meta).lower() or "label" in str(meta).lower():
                target_col = col
                break

        if target_col and target_col in df.columns:
            X = df.drop(columns=[target_col])
            y = df[target_col]
            for name, pack in models.items():
                if pack["instance"] is None:
                    continue
                res = await pack["instance"].fit_and_evaluate(X, y)
                model_results[name] = res
        else:
            model_results["note"] = "No outcome/label detected; ran unsupervised summary."
            model_results["summary"] = df.describe(include="all").to_dict()

        clinical = await self.insights.create_comprehensive_report({
            "model_results": model_results,
            "ai_strategy": strategy,
            "medical_context": medical_context
        })

        viz = await self.vis_ai.generate_medical_charts({
            "results": model_results,
            "strategy": strategy
        })

        return {
            "analysis_id": str(uuid.uuid4()),
            "ai_strategy": strategy,
            "model_execution_results": model_results,
            "clinical_insights": clinical,
            "visualizations": viz,
            "execution_metadata": {
                "seconds": round(time.time() - t0, 3)
            }
        }
