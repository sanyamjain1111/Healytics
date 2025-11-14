# Clinical Analysis Report – Dataset 24
_Generated: 20251113_071807_

## Executive Summary
This clinical analytics assessment involved the deployment and evaluation of a comprehensive suite of 17 predictive models across a dataset comprising 12,000 patient records. The preprocessing strategy included standard scaling for numerical features like age, BMI, and lab values, one-hot encoding for nominal categoricals, IQR-based outlier handling, and median/mode imputation for missing data, notably parsing a nested 'payload' JSON field for feature extraction. The most prominent risk signal identified was a high general Disease Risk, affecting approximately 29.18% of the patient cohort, indicating a significant portion of the population with elevated health concerns potentially linked to conditions like CKD or liver disease, as suggested by the model's target signals. Other critical areas of elevated risk include Diabetes Complications (3.83% prevalence), Acute Kidney Injury (AKI) Risk (3.17% prevalence), and the need for ICU Admission (2.62% prevalence), alongside Sepsis Early Warning signals (2.07% prevalence). These findings necessitate targeted clinical pathways and proactive interventions, particularly for chronic disease management and acute care escalation. A notable observation within the model results is the complete absence of positive predictions, or zero prevalence, for several crucial clinical outcomes, specifically 30-day and 90-day Readmissions, Hypertension Control, COPD Exacerbations, Adverse Drug Events, and No-Show Appointments. This zeroes out implies either a remarkably healthy cohort for these specific indicators within the observed period, or more likely, significant data completeness issues or misidentification of target signals during data extraction and model training for these specific outcomes. Furthermore, the designated regression models—LengthOfStayRegressor, CostOfCareRegressor, and AnemiaSeverityRegressor—were reported with 'n=0' and 'positives=0', indicating a failure to evaluate these models or process their respective target variables effectively. Operationally, this means vital insights into resource allocation and financial planning are currently unavailable. An anomaly detection process identified 991 anomalous records (approximately 8.26% of the dataset), which could influence model accuracy and reliability. Addressing these anomalies and investigating the zero-prevalence models is crucial for enhancing the integrity and utility of the analytical framework, allowing for more precise operational triage and patient care optimization.

## Key Findings
- A significant portion of the dataset (29.18%) is flagged with a high general Disease Risk, indicating a broad need for comprehensive health management across the patient population.
- Several critical clinical outcomes, including 30-day and 90-day Readmissions, Hypertension Control, COPD Exacerbations, Adverse Drug Events, and No-Show Appointments, showed zero prevalence, suggesting potential data acquisition issues or an absence of these events in the analyzed dataset.
- Patients at risk for Diabetes Complications represent 3.83% of the cohort, highlighting a substantial population requiring focused intervention for chronic disease management.
- Acute Kidney Injury (AKI) Risk affects 3.17% of patients, pointing to a critical area for early detection and medical management.
- Regression models for Length of Stay, Cost of Care, and Anemia Severity were not evaluated (n=0), rendering them currently non-operational for clinical and financial planning, despite their high priority in the strategy.
- Approximately 8.26% of the patient records contain identified anomalies (991 out of 12,000), which may impact the reliability and generalization of model predictions.
- ICU Admission Risk (2.62%) and Sepsis Early Warning (2.07%) indicate persistent acute care challenges requiring proactive monitoring and rapid response protocols.

## Recommendations
- Initiate an immediate investigation into the target variable data quality and extraction process for models showing zero prevalence (e.g., ReadmissionPredictor, HypertensionControlPredictor) to confirm the true absence of events or identify data gaps.
- Prioritize clinical interventions and educational programs for patients identified with high general Disease Risk, focusing on comprehensive chronic disease management and preventive care.
- Develop and deploy targeted care pathways for the 3.83% of patients at risk for Diabetes Complications, emphasizing glycemic control, lifestyle modifications, and regular screening for early detection.
- Implement enhanced monitoring protocols and clinical decision support tools for patients identified with AKI Risk (3.17% prevalence) to facilitate prompt intervention and prevent kidney deterioration.
- Address the 991 identified data anomalies by implementing data cleaning and validation routines to improve the overall data quality and ensure robust model performance.
- Review and rectify the data availability or processing issues for regression models (LengthOfStayRegressor, CostOfCareRegressor, AnemiaSeverityRegressor) to enable their evaluation and provide crucial insights for resource allocation and patient management.
- Establish rapid response teams or escalation protocols for patients flagged by the ICU Admission Predictor and Sepsis Early Warning models to ensure timely and effective acute care management.

## Cohorts of Interest
- **High Disease Risk Patients** – Patients predicted to be at high general disease risk by the DiseaseRiskPredictor model (prevalence 29.18%). — This is the largest identified risk cohort, indicating a systemic need for proactive health management, potentially encompassing chronic conditions like CKD or liver disease. Comprehensive care coordination for these patients can significantly impact population health outcomes.
- **Patients at Risk for Diabetes Complications** – Patients identified by the DiabetesComplicationRisk model (prevalence 3.83%). — Targeting this group allows for early intervention and focused management strategies to prevent severe diabetes-related complications, improve quality of life, and reduce hospitalizations.
- **Patients with Acute Kidney Injury (AKI) Risk** – Patients flagged by the AKIRiskPredictor model (prevalence 3.17%). — Early identification of AKI risk is critical for prompt medical management, including fluid balance adjustments and medication review, to prevent kidney damage and improve patient outcomes.
- **Patients Requiring Acute Care Intervention (ICU/Sepsis)** – Patients identified by the ICUAdmissionPredictor (prevalence 2.62%) or SepsisEarlyWarning (prevalence 2.07%) models. — These cohorts represent patients at high risk of acute, life-threatening conditions where early warning and rapid clinical response are paramount for survival and reducing morbidity and mortality.

## Appendix – Model Snapshot
```json
[
  {
    "model": "DiseaseRiskPredictor",
    "positives": 3501,
    "total": 12000,
    "rate": 0.2918
  },
  {
    "model": "DiabetesComplicationRisk",
    "positives": 460,
    "total": 12000,
    "rate": 0.0383
  },
  {
    "model": "AKIRiskPredictor",
    "positives": 380,
    "total": 12000,
    "rate": 0.0317
  },
  {
    "model": "ICUAdmissionPredictor",
    "positives": 314,
    "total": 12000,
    "rate": 0.0262
  },
  {
    "model": "MortalityRiskModel",
    "positives": 255,
    "total": 12000,
    "rate": 0.0213
  },
  {
    "model": "SepsisEarlyWarning",
    "positives": 248,
    "total": 12000,
    "rate": 0.0207
  },
  {
    "model": "HeartFailure30DRisk",
    "positives": 109,
    "total": 12000,
    "rate": 0.0091
  },
  {
    "model": "StrokeRiskPredictor",
    "positives": 35,
    "total": 12000,
    "rate": 0.0029
  },
  {
    "model": "ReadmissionPredictor",
    "positives": 0,
    "total": 12000,
    "rate": 0.0
  },
  {
    "model": "Readmission90DPredictor",
    "positives": 0,
    "total": 12000,
    "rate": 0.0
  },
  {
    "model": "HypertensionControlPredictor",
    "positives": 0,
    "total": 12000,
    "rate": 0.0
  },
  {
    "model": "COPDExacerbationPredictor",
    "positives": 0,
    "total": 12000,
    "rate": 0.0
  },
  {
    "model": "AdverseDrugEventPredictor",
    "positives": 0,
    "total": 12000,
    "rate": 0.0
  },
  {
    "model": "NoShowAppointmentPredictor",
    "positives": 0,
    "total": 12000,
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
    "patient_id": "804179",
    "positive_models": 7,
    "avg_score": 0.4732,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.21840909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.21840909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.5369605422019958,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.28977471590042114,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5566990375518799,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8171085715293884,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2796404261813944,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.5309118628501892,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7312999963760376,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1380191142454554,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9347266554832458,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20602769704096677,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16960904251271317,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9976820945739746,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.682519877546461
      },
      "CostOfCareRegressor": {
        "prediction": 9967.84765625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.069172929865751
      }
    }
  },
  {
    "patient_id": "806961",
    "positive_models": 7,
    "avg_score": 0.4128,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.155,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.155,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.5058093070983887,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.587367832660675,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.6785337924957275,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.552639365196228,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.20256960830604098,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.08935361355543137,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.8405610918998718,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.10421801028140892,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.5778982639312744,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.18459477387893142,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.14986475468298802,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9958382844924927,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.425250858519976
      },
      "CostOfCareRegressor": {
        "prediction": 9382.1474609375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.8722261828846705
      }
    }
  },
  {
    "patient_id": "803129",
    "positive_models": 6,
    "avg_score": 0.4465,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.21340909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.21340909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.04578312858939171,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.6710902452468872,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.801537811756134,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8067927360534668,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2172866240683334,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.27944502234458923,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6289377808570862,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.12044803703524404,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.962841808795929,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.12966982077457728,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16626426528094437,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9943022727966309,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.450417987775147
      },
      "CostOfCareRegressor": {
        "prediction": 9320.513671875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.360669172215869
      }
    }
  },
  {
    "patient_id": "801638",
    "positive_models": 6,
    "avg_score": 0.4383,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.2083451536643026,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.2083451536643026,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.1488495022058487,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9013368487358093,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5328158140182495,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6998094916343689,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.25080852747039445,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.6082383394241333,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.2723451852798462,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.12839773720482597,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8690882921218872,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.16157175183942463,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16109982369595116,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9856473207473755,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.913027922356616
      },
      "CostOfCareRegressor": {
        "prediction": 9116.76171875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.4226649293441587
      }
    }
  },
  {
    "patient_id": "800614",
    "positive_models": 6,
    "avg_score": 0.4216,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.18333333333333332,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.18333333333333332,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.054456815123558044,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.0026390121784061193,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.7377312779426575,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9348974823951721,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.19684717015546546,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.5116481184959412,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6861972808837891,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1358256741766687,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8663284182548523,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.2453483909963802,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1757179800274943,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9887930750846863,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.122431852889407
      },
      "CostOfCareRegressor": {
        "prediction": 9801.76953125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 0.9301927443755139
      }
    }
  },
  {
    "patient_id": "804453",
    "positive_models": 6,
    "avg_score": 0.4172,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.25,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.25,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7615060806274414,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.6674425005912781,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5767931938171387,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.640302300453186,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.23570500104689576,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.06641630083322525,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.33251404762268066,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.11932405371734917,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.5666938424110413,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.2128649113027952,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1630554812684362,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9982187151908875,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.708263057173995
      },
      "CostOfCareRegressor": {
        "prediction": 9543.0966796875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.603558059872946
      }
    }
  },
  {
    "patient_id": "811227",
    "positive_models": 6,
    "avg_score": 0.3929,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.15875,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.15875,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.6917012929916382,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.532535195350647,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.3146112859249115,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6510704755783081,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.20122001321211896,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.1270834505558014,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6060209274291992,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09713885214106596,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.6199632883071899,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1905018496802542,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1531049338986588,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9982444047927856,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.531074466066033
      },
      "CostOfCareRegressor": {
        "prediction": 9368.828125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.039037993947421
      }
    }
  },
  {
    "patient_id": "800825",
    "positive_models": 5,
    "avg_score": 0.4513,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.2034090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.2034090909090909,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.1794293224811554,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7992079257965088,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.7052691578865051,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8997867107391357,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.24365819245675335,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.29883912205696106,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.42597097158432007,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.0980594712480352,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9197801947593689,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.18413322359749995,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16252901061836217,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9944223761558533,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.516149760482519
      },
      "CostOfCareRegressor": {
        "prediction": 9185.4541015625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.1018766040306796
      }
    }
  },
  {
    "patient_id": "807690",
    "positive_models": 5,
    "avg_score": 0.4499,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.21174242424242423,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.21174242424242423,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.37859201431274414,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.763340175151825,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8163672089576721,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8116956949234009,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2882096038311594,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.28591468930244446,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.26456567645072937,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1212753089086726,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.7863491773605347,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.2039436467022982,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15903763039265814,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.995598554611206,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.344452150750344
      },
      "CostOfCareRegressor": {
        "prediction": 9603.90234375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.755703710003334
      }
    }
  },
  {
    "patient_id": "807335",
    "positive_models": 5,
    "avg_score": 0.4385,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.21007575757575758,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.21007575757575758,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7905781269073486,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.38618147373199463,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.15284810960292816,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8559598922729492,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.3329587769279287,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.19723357260227203,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.603579580783844,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.10765248612904213,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8884978890419006,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.2091691510573684,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.19406252076878477,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9996294975280762,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.610161577507666
      },
      "CostOfCareRegressor": {
        "prediction": 9368.1103515625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.669768655285022
      }
    }
  },
  {
    "patient_id": "810558",
    "positive_models": 5,
    "avg_score": 0.4375,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17007575757575757,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17007575757575757,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.2736116945743561,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.5329586863517761,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.8578694462776184,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8540253043174744,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.24290164055278107,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.41256678104400635,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.2612110376358032,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.08990301383136191,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9357361793518066,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.16196698077220234,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16821707147867507,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9932988882064819,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.4995919666751805
      },
      "CostOfCareRegressor": {
        "prediction": 9032.748046875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.9432579904451153
      }
    }
  },
  {
    "patient_id": "801654",
    "positive_models": 5,
    "avg_score": 0.435,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.21840909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.21840909090909094,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.6577094793319702,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9460018277168274,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.3054940402507782,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8006523847579956,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2987841897593808,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.16332900524139404,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.14367589354515076,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.11912161530800161,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8625325560569763,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20219129133821634,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16016873229733222,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9929453730583191,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.301297425414431
      },
      "CostOfCareRegressor": {
        "prediction": 9490.837890625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.879932799685176
      }
    }
  },
  {
    "patient_id": "807970",
    "positive_models": 5,
    "avg_score": 0.4349,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.25674242424242427,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.25674242424242427,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.699661910533905,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.4148740768432617,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.7049565315246582,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8526080846786499,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.21954378254740128,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.14510729908943176,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.34473466873168945,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1298361047083827,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.7066035866737366,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20198849537909236,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15874812341093214,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9962484240531921,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.645429781786054
      },
      "CostOfCareRegressor": {
        "prediction": 9947.171875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.936993249456242
      }
    }
  },
  {
    "patient_id": "808717",
    "positive_models": 5,
    "avg_score": 0.4315,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.21507575757575761,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.21507575757575761,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7948291897773743,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.3780158758163452,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.5335078835487366,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7344844341278076,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2653351015487992,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.0920814648270607,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.42001497745513916,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.09768203246725589,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9429904222488403,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.19296345104821103,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16127831391853178,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9975995421409607,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.741795737067377
      },
      "CostOfCareRegressor": {
        "prediction": 9351.7021484375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.768701203504999
      }
    }
  },
  {
    "patient_id": "811147",
    "positive_models": 5,
    "avg_score": 0.4299,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.20666666666666667,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.20666666666666667,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.5787428021430969,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.31822749972343445,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.313193678855896,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9112057089805603,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.26491389390635545,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.19903253018856049,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.631616473197937,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.1124539520076606,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8874505162239075,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.22892136728330761,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.16279779606229028,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.997282862663269,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.757260465070792
      },
      "CostOfCareRegressor": {
        "prediction": 9492.98046875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.462083151503557
      }
    }
  },
  {
    "patient_id": "801298",
    "positive_models": 5,
    "avg_score": 0.424,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.20174242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.20174242424242425,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8126618266105652,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7120189666748047,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.20337934792041779,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.821199893951416,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.26328218469349807,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.3125312626361847,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.41496536135673523,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.08196823908683344,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.5663479566574097,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.18481392153830928,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.161104288582167,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9975460171699524,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.516218251184649
      },
      "CostOfCareRegressor": {
        "prediction": 9689.466796875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.3094120084028305
      }
    }
  },
  {
    "patient_id": "809606",
    "positive_models": 5,
    "avg_score": 0.4196,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.18167848699763595,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.18167848699763595,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.05103014409542084,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.741395115852356,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9085776805877686,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.8658684492111206,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.24684083807132345,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.28241825103759766,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.27060288190841675,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.12093933767481464,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.6904345750808716,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.17644157273883618,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.1648942020850927,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9922145009040833,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.49357599797367
      },
      "CostOfCareRegressor": {
        "prediction": 9366.603515625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.840088605825028
      }
    }
  },
  {
    "patient_id": "805331",
    "positive_models": 5,
    "avg_score": 0.417,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17708333333333334,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17708333333333334,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8054342865943909,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.33584949374198914,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.325121134519577,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6586064696311951,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.21676024054836077,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.22126659750938416,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6830270290374756,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.10190297301627957,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.7777228355407715,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20569378457469664,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15343135813110492,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9991533756256104,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.682515364726694
      },
      "CostOfCareRegressor": {
        "prediction": 9721.32421875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.281883419580397
      }
    }
  },
  {
    "patient_id": "808287",
    "positive_models": 5,
    "avg_score": 0.4146,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.17007575757575757,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.17007575757575757,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.32834121584892273,
        "pred": 0,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.6351943612098694,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.38642576336860657,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.7583079934120178,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2755292263940317,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.7033300995826721,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.13027538359165192,
        "pred": 0,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.08227517251412866,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.8325955271720886,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.1652602056280601,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.17143965881066375,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9954102635383606,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.622906923550138
      },
      "CostOfCareRegressor": {
        "prediction": 8991.0712890625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.827017528542434
      }
    }
  },
  {
    "patient_id": "804295",
    "positive_models": 5,
    "avg_score": 0.4143,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.18666666666666668,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.18666666666666668,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7738897800445557,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.3828321099281311,
        "pred": 0,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.42825981974601746,
        "pred": 0,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.736160397529602,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.2817668090984388,
        "pred": 0,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.15844574570655823,
        "pred": 0,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6977190375328064,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.090062197374951,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.5160696506500244,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.20998558214829327,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.15289905439843837,
        "pred": 0,
        "threshold": 0.5
      },
      "DiseaseRiskPredictor": {
        "score": 0.9991255402565002,
        "pred": 1,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.625218508514337
      },
      "CostOfCareRegressor": {
        "prediction": 9655.6220703125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.4376906321195553
      }
    }
  }
]
```

## Appendix – Top Anomalies
```json
[
  {
    "patient_id": "803638",
    "anomaly_flag": 1,
    "anomaly_score": 0.10496487727187187
  },
  {
    "patient_id": "801696",
    "anomaly_flag": 1,
    "anomaly_score": 0.1018068939726523
  },
  {
    "patient_id": "808932",
    "anomaly_flag": 1,
    "anomaly_score": 0.08906780161600925
  },
  {
    "patient_id": "805832",
    "anomaly_flag": 1,
    "anomaly_score": 0.08096630221729895
  },
  {
    "patient_id": "810806",
    "anomaly_flag": 1,
    "anomaly_score": 0.0775186772417441
  },
  {
    "patient_id": "807870",
    "anomaly_flag": 1,
    "anomaly_score": 0.0744413688619614
  },
  {
    "patient_id": "800415",
    "anomaly_flag": 1,
    "anomaly_score": 0.07422673254000833
  },
  {
    "patient_id": "804421",
    "anomaly_flag": 1,
    "anomaly_score": 0.07300897514946192
  },
  {
    "patient_id": "811032",
    "anomaly_flag": 1,
    "anomaly_score": 0.07257813743255381
  },
  {
    "patient_id": "803633",
    "anomaly_flag": 1,
    "anomaly_score": 0.07008134252252685
  },
  {
    "patient_id": "809851",
    "anomaly_flag": 1,
    "anomaly_score": 0.06931262629488832
  },
  {
    "patient_id": "804503",
    "anomaly_flag": 1,
    "anomaly_score": 0.06841552119866712
  },
  {
    "patient_id": "807065",
    "anomaly_flag": 1,
    "anomaly_score": 0.06820421766197338
  },
  {
    "patient_id": "802970",
    "anomaly_flag": 1,
    "anomaly_score": 0.06720033170593531
  },
  {
    "patient_id": "810011",
    "anomaly_flag": 1,
    "anomaly_score": 0.06692567219141665
  },
  {
    "patient_id": "805874",
    "anomaly_flag": 1,
    "anomaly_score": 0.06378804470269295
  },
  {
    "patient_id": "809562",
    "anomaly_flag": 1,
    "anomaly_score": 0.06374827847643627
  },
  {
    "patient_id": "809167",
    "anomaly_flag": 1,
    "anomaly_score": 0.0634768391288103
  },
  {
    "patient_id": "811503",
    "anomaly_flag": 1,
    "anomaly_score": 0.06249358865779242
  },
  {
    "patient_id": "806855",
    "anomaly_flag": 1,
    "anomaly_score": 0.062440515193906476
  }
]
```