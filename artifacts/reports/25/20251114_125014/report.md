# Clinical Analysis Report – Dataset 25
_Generated: 20251114_125014_

## Executive Summary
This clinical analytics report summarizes the initial evaluation of a suite of predictive models across a dataset comprising 5,000 patient records. The primary objective was to identify high-risk patients for various critical conditions and operational challenges, supporting more proactive clinical interventions and optimized resource allocation. A robust preprocessing strategy was employed, including StandardScaler for numerical features, one-hot encoding for categorical variables (excluding patient_id and dataset_id), IQR-based outlier capping, and median/mode imputation, alongside JSON parsing of the 'payload' column to extract nested features. Key findings reveal significant risk signals in several areas. The highest prevalence of identified positive cases was for Diabetes Complication Risk (2.54%, 127 patients), followed closely by AKI Risk (2.08%, 104 patients), Sepsis Early Warning (1.88%, 94 patients), and ICU Admission Prediction (1.86%, 93 patients). These areas represent immediate priorities for clinical teams, indicating a substantial cohort of patients who could benefit from targeted early intervention programs, enhanced monitoring protocols, and resource pre-allocation. For instance, the high AKI and Sepsis signals necessitate rapid response team activations and protocolized care bundles to mitigate adverse outcomes. Conversely, several critical models, including ReadmissionPredictor (30-day and 90-day), HypertensionControlPredictor, COPDExacerbationPredictor, AdverseDrugEventPredictor, and NoShowAppointmentPredictor, reported zero positive cases (0.0% prevalence). This absence of identified risk needs urgent investigation. While it could indicate extremely low incidence in this specific patient cohort, it more likely points to potential data quality issues, misconfiguration of model thresholds, or a disconnect between the model's training data and the characteristics of the current dataset. If these conditions are prevalent in the real-world population served, the current model outputs fail to provide actionable insights for these pathways, leading to missed opportunities for preventive care and operational efficiency gains in areas like appointment scheduling and chronic disease management. Furthermore, a significant data quality concern was identified with the regression models (LengthOfStayRegressor, CostOfCareRegressor, AnemiaSeverityRegressor), which showed zero processed records (n=0) despite being listed as 'classification' types in the results, an inconsistency with their intended 'regression' task type as defined in the strategy. This indicates a potential pipeline failure or data incompatibility, rendering these critical operational and resource planning models inoperable in the current analysis. Anomaly detection identified 449 anomalous records out of the 5,000 total, representing approximately 9% of the dataset. This notable proportion of anomalies warrants further investigation as it can introduce bias and reduce the reliability of model predictions. Addressing these data and model execution issues is paramount to fully leverage the predictive capabilities across the entire suite of clinical and operational models.

## Key Findings
- A total of 5,000 patient records were analyzed across various clinical and operational risk models.
- The highest prevalence of identified risk was for Diabetes Complication Risk (2.54%, affecting 127 patients), followed by AKI Risk (2.08%, 104 patients), and Sepsis Early Warning (1.88%, 94 patients).
- Five high-priority classification models, including ReadmissionPredictor (30D & 90D), HypertensionControlPredictor, COPDExacerbationPredictor, AdverseDrugEventPredictor, and NoShowAppointmentPredictor, reported zero positive cases (0.0% prevalence), indicating a critical gap in risk identification for these conditions or potential data issues.
- All three regression models (LengthOfStayRegressor, CostOfCareRegressor, AnemiaSeverityRegressor) failed to process any records (n=0) and were incorrectly labeled as 'classification' types in the results, pointing to a significant data pipeline or configuration error.
- A substantial proportion of the dataset, 449 out of 5,000 records (approximately 9%), was flagged as anomalous, which could impact the reliability and generalizability of the model predictions.
- MortalityRiskModel identified 46 patients (0.92% prevalence), ICUAdmissionPredictor identified 93 patients (1.86% prevalence), and HeartFailure30DRisk identified 32 patients (0.64% prevalence) requiring heightened clinical attention.

## Recommendations
- Immediately investigate the models showing zero positive predictions (ReadmissionPredictor, HypertensionControlPredictor, COPDExacerbationPredictor, AdverseDrugEventPredictor, NoShowAppointmentPredictor). This includes reviewing data quality for relevant features, model thresholds, and ensuring model suitability for the target population.
- Prioritize the development or enhancement of care pathways for patients identified with high prevalence risks: Diabetes Complications, AKI, Sepsis, and ICU Admission. This should include standardized protocols for early detection, rapid response, and proactive management.
- Resolve the data processing and configuration issues preventing the LengthOfStayRegressor, CostOfCareRegressor, and AnemiaSeverityRegressor from operating. Confirm their output type is correctly handled as regression and ensure data is being fed into them.
- Conduct a deep dive into the 449 identified anomalous records to understand their nature and impact. Determine if these represent data entry errors, legitimate but unusual clinical profiles, or system issues, and implement strategies for data cleansing or robust anomaly handling.
- Implement continuous data validation checks for incoming data streams to prevent future occurrences of zero-processed models or widespread anomalies, ensuring data integrity before model inference.
- Given the low prevalence for several critical models (e.g., Mortality, Heart Failure, Stroke), consider reviewing and potentially optimizing the prediction thresholds (currently 0.5) to balance sensitivity and specificity for clinical utility, especially if false negatives are highly undesirable.

## Cohorts of Interest
- **High-Risk Diabetes Complication Cohort** – Patients identified by the DiabetesComplicationRisk model, comprising 127 individuals (2.54% of the dataset). — This cohort represents the largest group identified with a specific clinical risk. Proactive management, education, and tighter glycemic control interventions could significantly reduce morbidity and improve quality of life, aligning with population health goals and reducing long-term healthcare burdens.
- **Acute Life-Threatening Event Risk Cohort** – Patients identified by the AKIRiskPredictor (104 individuals, 2.08%) and SepsisEarlyWarning (94 individuals, 1.88%). — Acute Kidney Injury and Sepsis are rapidly progressing, life-threatening conditions requiring immediate medical attention. Early identification allows for rapid response team activation, initiation of protocolized care bundles, and potential ICU transfer to prevent severe outcomes, reduce mortality, and improve patient safety.
- **Unidentified Operational Risk Cohort (Readmissions & No-Shows)** – The entire dataset of 5,000 patients for whom ReadmissionPredictor (30D & 90D) and NoShowAppointmentPredictor models reported zero positive cases. — Readmissions and no-show appointments significantly impact operational efficiency, resource utilization, and patient outcomes. The current models' inability to identify any at-risk patients for these areas is a critical gap. This cohort requires urgent investigation into underlying data quality or model configuration to ensure these vital operational risks can be effectively managed.
- **Anomalous Data Cohort** – The 449 patients flagged with data anomalies (approximately 9% of the dataset). — The data integrity for this cohort is questionable. Understanding the nature and source of these anomalies is crucial to ensure that model predictions are reliable and unbiased, and to prevent future data quality issues from impacting clinical decision-making or operational planning.

## Appendix – Model Snapshot
```json
[
  {
    "model": "DiabetesComplicationRisk",
    "positives": 127,
    "total": 5000,
    "rate": 0.0254
  },
  {
    "model": "AKIRiskPredictor",
    "positives": 104,
    "total": 5000,
    "rate": 0.0208
  },
  {
    "model": "SepsisEarlyWarning",
    "positives": 94,
    "total": 5000,
    "rate": 0.0188
  },
  {
    "model": "ICUAdmissionPredictor",
    "positives": 93,
    "total": 5000,
    "rate": 0.0186
  },
  {
    "model": "MortalityRiskModel",
    "positives": 46,
    "total": 5000,
    "rate": 0.0092
  },
  {
    "model": "HeartFailure30DRisk",
    "positives": 32,
    "total": 5000,
    "rate": 0.0064
  },
  {
    "model": "StrokeRiskPredictor",
    "positives": 9,
    "total": 5000,
    "rate": 0.0018
  },
  {
    "model": "ReadmissionPredictor",
    "positives": 0,
    "total": 5000,
    "rate": 0.0
  },
  {
    "model": "Readmission90DPredictor",
    "positives": 0,
    "total": 5000,
    "rate": 0.0
  },
  {
    "model": "HypertensionControlPredictor",
    "positives": 0,
    "total": 5000,
    "rate": 0.0
  },
  {
    "model": "COPDExacerbationPredictor",
    "positives": 0,
    "total": 5000,
    "rate": 0.0
  },
  {
    "model": "AdverseDrugEventPredictor",
    "positives": 0,
    "total": 5000,
    "rate": 0.0
  },
  {
    "model": "NoShowAppointmentPredictor",
    "positives": 0,
    "total": 5000,
    "rate": 0.0
  },
  {
    "model": "LengthOfStayRegressor",
    "positives": 0,
    "total": 0,
    "rate": 0.0
  },
  {
    "model": "CostOfCareRegressor",
    "positives": 0,
    "total": 0,
    "rate": 0.0
  },
  {
    "model": "AnemiaSeverityRegressor",
    "positives": 0,
    "total": 0,
    "rate": 0.0
  }
]
```

## Appendix – High-risk Patients
_Definition: ≥2 positive model(s) **or** avg score ≥0.80_
```json
[
  {
    "patient_id": "900141",
    "positive_models": 5,
    "avg_score": 0.4225,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17174242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17174242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7590444684028625,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8723475337028503,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.6338834166526794,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8793798089027405,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.26467118805895445,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.12655790150165558,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.2856941223144531,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.10524627936697413,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8666081428527832,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1963802716048825,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15966232451945928,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.227779931521535
      },
      "CostOfCareRegressor": {
        "prediction": 9373.3408203125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.118443914086274
      }
    }
  },
  {
    "patient_id": "902404",
    "positive_models": 5,
    "avg_score": 0.4205,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.24340909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.24340909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.19243304431438446,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.41956666111946106,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5549457669258118,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7861200571060181,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.23289681516312563,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.7229782342910767,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6997544765472412,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.11207763174346726,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9633616209030151,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.12185417390502191,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17415582533701965,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.484328227718294
      },
      "CostOfCareRegressor": {
        "prediction": 9058.1630859375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.2859073509117445
      }
    }
  },
  {
    "patient_id": "900063",
    "positive_models": 5,
    "avg_score": 0.3138,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.1434090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.1434090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.05529174581170082,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.5501992106437683,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.573493242263794,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6566749811172485,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.24626652989042278,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.5506536960601807,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.16770364344120026,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.0828054869348392,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.6189659833908081,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.0925789784501359,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1984850700880572,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.676719491247633
      },
      "CostOfCareRegressor": {
        "prediction": 8908.0546875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.8635170952781346
      }
    }
  },
  {
    "patient_id": "903436",
    "positive_models": 4,
    "avg_score": 0.4279,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.24333333333333335,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.24333333333333335,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9286806583404541,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.5980725884437561,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.20045039057731628,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9112243056297302,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2760342689138392,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.272331178188324,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.4934226870536804,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.11253586521863007,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9033734202384949,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20693521011940072,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17347607660074654,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.766873572860579
      },
      "CostOfCareRegressor": {
        "prediction": 9452.052734375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.340804523462358
      }
    }
  },
  {
    "patient_id": "900168",
    "positive_models": 4,
    "avg_score": 0.4165,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.24333333333333335,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.24333333333333335,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9299221038818359,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7516398429870605,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.3236660063266754,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.829404354095459,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2837289589622778,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.31008046865463257,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.3273799419403076,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09779514693874307,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.699377715587616,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20912669322534375,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16620372494639546,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.7484852360778484
      },
      "CostOfCareRegressor": {
        "prediction": 10036.8173828125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.473739829729457
      }
    }
  },
  {
    "patient_id": "904089",
    "positive_models": 4,
    "avg_score": 0.3932,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.26,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.26,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.6361835598945618,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.3420509994029999,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.3701073229312897,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7791730165481567,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2616352185882276,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.2921141982078552,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6298956871032715,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.10459910089320479,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.7995306849479675,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.21497818076671651,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16109615223059962,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.817490986479936
      },
      "CostOfCareRegressor": {
        "prediction": 9822.9111328125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.754459138595721
      }
    }
  },
  {
    "patient_id": "901629",
    "positive_models": 4,
    "avg_score": 0.3907,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.22674242424242427,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.22674242424242427,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.08858691900968552,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8046995997428894,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8419625759124756,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.545341968536377,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.24946256879707981,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.440945029258728,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.26208919286727905,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.13416998686884626,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9348134398460388,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.14900406254004295,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17481137247273967,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.753411600349502
      },
      "CostOfCareRegressor": {
        "prediction": 9010.4423828125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.413142902245493
      }
    }
  },
  {
    "patient_id": "900397",
    "positive_models": 4,
    "avg_score": 0.3748,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.20674242424242426,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.20674242424242426,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.22120708227157593,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7528072595596313,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.27637049555778503,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8209437727928162,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.22956000669688642,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.7250682711601257,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.09102785587310791,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09002828555991226,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9350746273994446,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.14965523650854878,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16714860400643364,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.502111372748277
      },
      "CostOfCareRegressor": {
        "prediction": 9057.884765625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.4724900514334855
      }
    }
  },
  {
    "patient_id": "901305",
    "positive_models": 4,
    "avg_score": 0.3569,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.16007575757575757,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.16007575757575757,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.18207626044750214,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7024484872817993,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.7790482640266418,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8789902925491333,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.25636582071846153,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.05011257529258728,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.17895622551441193,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.10912989062776496,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8582574129104614,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1379693658790358,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.18619355327431047,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.479592232238676
      },
      "CostOfCareRegressor": {
        "prediction": 8869.7470703125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 8.099193023490523
      }
    }
  },
  {
    "patient_id": "902600",
    "positive_models": 4,
    "avg_score": 0.3527,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.27666666666666667,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.27666666666666667,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.5971603989601135,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7236612439155579,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.6180447936058044,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7990482449531555,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2647415103029628,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.022778315469622612,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.22250615060329437,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.11663255887520893,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.2223643958568573,
        "pred": 0,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.26892849834809074,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1753905935269702,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.514395248642179
      },
      "CostOfCareRegressor": {
        "prediction": 9666.89453125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 9.536682215747218
      }
    }
  },
  {
    "patient_id": "900372",
    "positive_models": 4,
    "avg_score": 0.3459,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.18375,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.18375,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9843473434448242,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.06355548650026321,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.698587954044342,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6549577713012695,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.21951530568224695,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.05699014291167259,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.1270555704832077,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09048305422542256,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8793991804122925,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1922492286442095,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16176451960279703,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.772716355291404
      },
      "CostOfCareRegressor": {
        "prediction": 9626.2646484375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.1425589120717468
      }
    }
  },
  {
    "patient_id": "900502",
    "positive_models": 4,
    "avg_score": 0.3448,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.1784090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.1784090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.37360623478889465,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.842030942440033,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.6870881915092468,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6884576678276062,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2649283005761801,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.08070003241300583,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.20676599442958832,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09867181547871612,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.5288955569267273,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1971761518271824,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15781009306381139,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.353223434908108
      },
      "CostOfCareRegressor": {
        "prediction": 9417.9296875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.826377258198476
      }
    }
  },
  {
    "patient_id": "902930",
    "positive_models": 4,
    "avg_score": 0.2737,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.12333333333333334,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.12333333333333334,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.012673907913267612,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.5805160403251648,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5949611067771912,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6175895929336548,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2155155512990988,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.24990665912628174,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.022458696737885475,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1073976901472568,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.5978173017501831,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1565238346166149,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15556504987656086,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.491653296550982
      },
      "CostOfCareRegressor": {
        "prediction": 9273.72265625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.5743243202267365
      }
    }
  },
  {
    "patient_id": "904478",
    "positive_models": 3,
    "avg_score": 0.36,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.26666666666666666,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.26666666666666666,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.48723188042640686,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.3670472204685211,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.6867847442626953,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7732006907463074,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.24509917565480113,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.030683686956763268,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5321895480155945,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.12616310870905909,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.4655723571777344,
        "pred": 0,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.2532459007370621,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17977886770965806,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.759516516468079
      },
      "CostOfCareRegressor": {
        "prediction": 9922.6005859375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 8.700434609127107
      }
    }
  },
  {
    "patient_id": "904043",
    "positive_models": 3,
    "avg_score": 0.343,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17876182033096927,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17876182033096927,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.25321218371391296,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.3107932507991791,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.2884002923965454,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6876343488693237,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.21233105436218416,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.22890669107437134,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7506241798400879,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.12175254815728906,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8987515568733215,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.19512899104655,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15407961376281437,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.5796297233486065
      },
      "CostOfCareRegressor": {
        "prediction": 9518.267578125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.805153255680407
      }
    }
  },
  {
    "patient_id": "904736",
    "positive_models": 3,
    "avg_score": 0.337,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17174242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17174242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.04756384715437889,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.3959701955318451,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.24648363888263702,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8073549866676331,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2390824190321197,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.3561338186264038,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6338258981704712,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.08679286360605844,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9011368155479431,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.16471340006810947,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1586486610822066,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.056456635857282
      },
      "CostOfCareRegressor": {
        "prediction": 9241.583984375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.955876811614641
      }
    }
  },
  {
    "patient_id": "900238",
    "positive_models": 3,
    "avg_score": 0.3337,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.20674242424242426,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.20674242424242426,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.21197757124900818,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9307499527931213,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5754116177558899,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.5345736742019653,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.3106101086150251,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.21096831560134888,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.33265700936317444,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1381266691325307,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.29050561785697937,
        "pred": 0,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.18276694318734202,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.2068162197015311,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.7886085652043615
      },
      "CostOfCareRegressor": {
        "prediction": 8702.1826171875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 9.02013025143975
      }
    }
  },
  {
    "patient_id": "903556",
    "positive_models": 3,
    "avg_score": 0.3141,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.1534090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.1534090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.09632844477891922,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.6099516749382019,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.3306574821472168,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6538699865341187,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.22636876018608562,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.46182724833488464,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.22733311355113983,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.08435441734634332,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.7700485587120056,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.09901448307147186,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.21633789297530864,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.7703517750981606
      },
      "CostOfCareRegressor": {
        "prediction": 9110.673828125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.041536749379494
      }
    }
  },
  {
    "patient_id": "902291",
    "positive_models": 3,
    "avg_score": 0.312,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.19674242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.19674242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.014566607773303986,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.11679932475090027,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.6069194078445435,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7252886891365051,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.22740443983784472,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.467896431684494,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.18759256601333618,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.07805473737877505,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9154475927352905,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.15049205402554092,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17181986085395615,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.387121519658966
      },
      "CostOfCareRegressor": {
        "prediction": 9394.7998046875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.860322367053166
      }
    }
  },
  {
    "patient_id": "904918",
    "positive_models": 3,
    "avg_score": 0.3076,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17674242424242426,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17674242424242426,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.25151312351226807,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.5137331485748291,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.4441428780555725,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.743510365486145,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2774323165143883,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.14488549530506134,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.11479739099740982,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09412971240716819,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.7149721384048462,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.16642577852766952,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17939499183095187,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.607939821083712
      },
      "CostOfCareRegressor": {
        "prediction": 8888.1201171875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.960029316809701
      }
    }
  }
]
```

## Appendix – Top Anomalies
```json
[
  {
    "patient_id": "904478",
    "anomaly_flag": 1,
    "anomaly_score": 0.10947419714458106
  },
  {
    "patient_id": "901629",
    "anomaly_flag": 1,
    "anomaly_score": 0.09491330998623759
  },
  {
    "patient_id": "902070",
    "anomaly_flag": 1,
    "anomaly_score": 0.08999993816333507
  },
  {
    "patient_id": "904294",
    "anomaly_flag": 1,
    "anomaly_score": 0.08925103974986237
  },
  {
    "patient_id": "904640",
    "anomaly_flag": 1,
    "anomaly_score": 0.08091876576608703
  },
  {
    "patient_id": "902382",
    "anomaly_flag": 1,
    "anomaly_score": 0.07913814964035726
  },
  {
    "patient_id": "903633",
    "anomaly_flag": 1,
    "anomaly_score": 0.06523645185861116
  },
  {
    "patient_id": "900781",
    "anomaly_flag": 1,
    "anomaly_score": 0.06522768141061464
  },
  {
    "patient_id": "902505",
    "anomaly_flag": 1,
    "anomaly_score": 0.0639404314380646
  },
  {
    "patient_id": "904558",
    "anomaly_flag": 1,
    "anomaly_score": 0.06159507262480113
  },
  {
    "patient_id": "900052",
    "anomaly_flag": 1,
    "anomaly_score": 0.059671859465019406
  },
  {
    "patient_id": "900747",
    "anomaly_flag": 1,
    "anomaly_score": 0.05720226564084607
  },
  {
    "patient_id": "903955",
    "anomaly_flag": 1,
    "anomaly_score": 0.0569761351644853
  },
  {
    "patient_id": "900605",
    "anomaly_flag": 1,
    "anomaly_score": 0.05605671872996254
  },
  {
    "patient_id": "900932",
    "anomaly_flag": 1,
    "anomaly_score": 0.05514646047301608
  },
  {
    "patient_id": "900503",
    "anomaly_flag": 1,
    "anomaly_score": 0.054906275569697294
  },
  {
    "patient_id": "904503",
    "anomaly_flag": 1,
    "anomaly_score": 0.05390651333121954
  },
  {
    "patient_id": "901875",
    "anomaly_flag": 1,
    "anomaly_score": 0.05302694924451834
  },
  {
    "patient_id": "900415",
    "anomaly_flag": 1,
    "anomaly_score": 0.052741863054442284
  },
  {
    "patient_id": "902600",
    "anomaly_flag": 1,
    "anomaly_score": 0.05190848489177169
  }
]
```