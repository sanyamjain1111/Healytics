# Clinical Analysis Report – Dataset 8
_Generated: 20250920_012429_

## Overview
- **Strategy ID**: None
- **Risk JSON**: `artifacts/analysis/8/20250920_012118/risk_prediction.json`
- **Anomaly JSON**: `artifacts/analysis/8/20250920_012118/anomaly_detection.json`

## Executive Summary
Automated analysis completed.

## Narrative
In dataset 8, the strongest risk signals came from: SepsisEarlyWarning (39602/50000), DiabetesComplicationRisk (34278/50000), HeartFailure30DRisk (34278/50000). Overall, 225236 positive predictions were generated across 8 configured model(s).

20 patient(s) met high-risk criteria (≥2 positive model(s) or avg score ≥0.80). Examples include: 710388 (pos=8, avg=0.90), 711481 (pos=8, avg=0.90), 711577 (pos=8, avg=0.90), 711848 (pos=8, avg=0.90), 712859 (pos=8, avg=0.90). These patients should be prioritized for clinical review and potential intervention.

Unsupervised anomaly detection highlighted 20 notable patient(s). Top outliers include: 703284 (score=0.130), 703284 (score=0.130), 705383 (score=0.124), 705383 (score=0.124), 721056 (score=0.118). Anomalies may reflect rare physiology, data quality issues, or emergent risk patterns.

Recommended next steps: (1) review high-risk patients for confirmatory clinical signals; (2) adjust model thresholds if prevalence is misaligned; (3) audit outliers for data quality and clinical plausibility; (4) incorporate clinician feedback to refine the decision thresholds and follow-up workflows.

## Model Snapshot
```json
[
  {
    "model": "SepsisEarlyWarning",
    "positives": 39602,
    "total": 50000,
    "rate": 0.792
  },
  {
    "model": "DiabetesComplicationRisk",
    "positives": 34278,
    "total": 50000,
    "rate": 0.6856
  },
  {
    "model": "HeartFailure30DRisk",
    "positives": 34278,
    "total": 50000,
    "rate": 0.6856
  },
  {
    "model": "StrokeRiskPredictor",
    "positives": 28246,
    "total": 50000,
    "rate": 0.5649
  },
  {
    "model": "HypertensionControlPredictor",
    "positives": 22208,
    "total": 50000,
    "rate": 0.4442
  },
  {
    "model": "COPDExacerbationPredictor",
    "positives": 22208,
    "total": 50000,
    "rate": 0.4442
  },
  {
    "model": "AnemiaSeverityRegressor",
    "positives": 22208,
    "total": 50000,
    "rate": 0.4442
  },
  {
    "model": "ICUAdmissionPredictor",
    "positives": 22208,
    "total": 50000,
    "rate": 0.4442
  }
]
```

## High-risk Patients
_Definition: ≥2 positive model(s) **or** avg score ≥0.80_
```json
[
  {
    "patient_id": "710388",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "711481",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "711577",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "711848",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "712859",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "714089",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "714987",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "716975",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "717437",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "717844",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "718603",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "719345",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "719876",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "721271",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "721415",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "722219",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "722401",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "722602",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "723958",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  },
  {
    "patient_id": "723990",
    "positive_models": 8,
    "avg_score": 0.9,
    "models": {
      "DiabetesComplicationRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "HypertensionControlPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.4
      },
      "StrokeRiskPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.45
      },
      "COPDExacerbationPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "AnemiaSeverityRegressor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.35
      },
      "ICUAdmissionPredictor": {
        "score": 0.8999999999999999,
        "pred": 1,
        "threshold": 0.5
      }
    }
  }
]
```

## Top Anomalies
```json
[
  {
    "patient_id": "703284",
    "anomaly_flag": 1,
    "anomaly_score": 0.1298130570577778
  },
  {
    "patient_id": "703284",
    "anomaly_flag": 1,
    "anomaly_score": 0.1298130570577778
  },
  {
    "patient_id": "705383",
    "anomaly_flag": 1,
    "anomaly_score": 0.12413674461776569
  },
  {
    "patient_id": "705383",
    "anomaly_flag": 1,
    "anomaly_score": 0.12413674461776569
  },
  {
    "patient_id": "721056",
    "anomaly_flag": 1,
    "anomaly_score": 0.1183372039805699
  },
  {
    "patient_id": "721056",
    "anomaly_flag": 1,
    "anomaly_score": 0.1183372039805699
  },
  {
    "patient_id": "722219",
    "anomaly_flag": 1,
    "anomaly_score": 0.1108345075385726
  },
  {
    "patient_id": "722219",
    "anomaly_flag": 1,
    "anomaly_score": 0.1108345075385726
  },
  {
    "patient_id": "701507",
    "anomaly_flag": 1,
    "anomaly_score": 0.10090970512100483
  },
  {
    "patient_id": "701507",
    "anomaly_flag": 1,
    "anomaly_score": 0.10090970512100483
  },
  {
    "patient_id": "704471",
    "anomaly_flag": 1,
    "anomaly_score": 0.100263117113079
  },
  {
    "patient_id": "704471",
    "anomaly_flag": 1,
    "anomaly_score": 0.100263117113079
  },
  {
    "patient_id": "715255",
    "anomaly_flag": 1,
    "anomaly_score": 0.09811272034481067
  },
  {
    "patient_id": "715255",
    "anomaly_flag": 1,
    "anomaly_score": 0.09811272034481067
  },
  {
    "patient_id": "706821",
    "anomaly_flag": 1,
    "anomaly_score": 0.09787045877958245
  },
  {
    "patient_id": "706821",
    "anomaly_flag": 1,
    "anomaly_score": 0.09787045877958245
  },
  {
    "patient_id": "711544",
    "anomaly_flag": 1,
    "anomaly_score": 0.0964702225017926
  },
  {
    "patient_id": "711544",
    "anomaly_flag": 1,
    "anomaly_score": 0.0964702225017926
  },
  {
    "patient_id": "709094",
    "anomaly_flag": 1,
    "anomaly_score": 0.09535723736012713
  },
  {
    "patient_id": "709094",
    "anomaly_flag": 1,
    "anomaly_score": 0.09535723736012713
  }
]
```