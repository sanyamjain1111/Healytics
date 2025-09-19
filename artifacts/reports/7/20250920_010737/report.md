# Clinical Analysis Report – Dataset 7
_Generated: 20250920_010737_

## Overview
- **Strategy ID**: 9
- **Risk JSON**: `artifacts/analysis/7/20250920_005247/risk_prediction.json`
- **Anomaly JSON**: `artifacts/analysis/7/20250920_005247/anomaly_detection.json`

## Risk Summary
```json
{
  "dataset_id": 7,
  "strategy_id": 9,
  "selected_models": [
    "DiabetesComplicationRisk",
    "HypertensionControlPredictor",
    "HeartFailure30DRisk",
    "StrokeRiskPredictor",
    "COPDExacerbationPredictor",
    "AnemiaSeverityRegressor",
    "SepsisEarlyWarning",
    "ICUAdmissionPredictor"
  ],
  "counts": {
    "DiabetesComplicationRisk": {
      "positives": 21050,
      "total": 24000
    },
    "HypertensionControlPredictor": {
      "positives": 17286,
      "total": 24000
    },
    "HeartFailure30DRisk": {
      "positives": 21050,
      "total": 24000
    },
    "StrokeRiskPredictor": {
      "positives": 19434,
      "total": 24000
    },
    "COPDExacerbationPredictor": {
      "positives": 17286,
      "total": 24000
    },
    "AnemiaSeverityRegressor": {
      "positives": 17286,
      "total": 24000
    },
    "SepsisEarlyWarning": {
      "positives": 22328,
      "total": 24000
    },
    "ICUAdmissionPredictor": {
      "positives": 17286,
      "total": 24000
    }
  }
}
```

## Anomaly Summary
```json
{
  "dataset_id": 7,
  "n_anomalies": 2308,
  "total": 24000
}
```

## Insights
```json
{
  "executive_summary": "Automated analysis completed.",
  "key_findings": [
    "Models executed; see detailed metrics."
  ],
  "recommendations": [
    "Review results with domain experts."
  ],
  "cohorts_of_interest": [],
  "visualization_titles": {
    "histograms": {
      "title": "Feature Distributions",
      "xlabel": "Value",
      "ylabel": "Frequency"
    },
    "risk_heatmap": {
      "title": "Patient Risk Heatmap",
      "xlabel": "Patients",
      "ylabel": "Models"
    },
    "feature_importance": {
      "title": "Top Predictors",
      "xlabel": "Importance",
      "ylabel": "Feature"
    },
    "calibration": {
      "title": "Calibration Curve",
      "xlabel": "Predicted Probability",
      "ylabel": "Observed Frequency"
    },
    "roc": {
      "title": "ROC Curve",
      "xlabel": "False Positive Rate",
      "ylabel": "True Positive Rate"
    }
  }
}
```