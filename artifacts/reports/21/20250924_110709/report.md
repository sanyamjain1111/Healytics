# Clinical Analysis Report – Dataset 21
_Generated: 20250924_110709_

## Executive Summary
This analysis utilized 14 classification and 3 regression models to assess risk factors from a dataset of 25,000 patient records.  The dataset included 500 rows with a mix of numerical and categorical features, which were preprocessed using standardization for numerical features, one-hot encoding for categorical features, winsorization of outliers and imputation of missing values.  SepsisEarlyWarning showed the highest prevalence (25.3%), indicating a significant portion of the patient population may be at risk for sepsis.  DiabetesComplicationRisk and HypertensionControlPredictor also exhibited high prevalence rates at 26.3% and 23.5%, respectively, suggesting widespread diabetes complications and hypertension issues among the patients.  The MortalityRiskModel identified 1635 (6.5%) patients at risk of 30-day mortality, while ICUAdmissionPredictor flagged 1581 (6.3%). Notably, several models (ReadmissionPredictor, Readmission90DPredictor, COPDExacerbationPredictor, and AdverseDrugEventPredictor) reported zero positives, which warrants further investigation into either data quality issues or model performance.  Regression model results were unavailable due to zero patient records. The presence of 2481 anomalies (almost 10%) highlights the need for data cleaning. These findings underscore the need for improved triage strategies, prioritization of sepsis and diabetes care pathways, and a focused review of the underperforming models, potentially requiring model retraining or data correction.  Early detection of sepsis and hypertension management programs may offer significant improvements in patient care.

## Key Findings
- SepsisEarlyWarning showed the highest prevalence at 25.3%
- MortalityRiskModel predicted 6.5% of patients at risk of 30-day mortality
- ICUAdmissionPredictor predicted 6.3% of patients at risk of ICU admission
- Several models showed zero positive predictions, indicating potential issues.
- 2481 anomalies (9.9%) were detected in the dataset.

## Recommendations
- Prioritize patients flagged by SepsisEarlyWarning for immediate attention.
- Implement proactive interventions for patients at high risk of mortality and ICU admission.
- Investigate and address the reasons for zero positive predictions in certain models.
- Conduct a thorough data quality review and anomaly resolution.
- Develop targeted care pathways for patients with diabetes complications and uncontrolled hypertension.

## Cohorts of Interest
- **High Sepsis Risk** – Patients flagged by SepsisEarlyWarning above the defined threshold. — This cohort represents a large portion of the population (25.3%) at significant risk requiring prompt medical intervention.
- **High Mortality Risk** – Patients identified by MortalityRiskModel as high risk. — Early identification of this cohort (6.5%) allows for proactive measures to improve patient outcomes.

## Appendix – Model Snapshot
```json
[
  {
    "model": "DiabetesComplicationRisk",
    "positives": 6578,
    "total": 25000,
    "rate": 0.2631
  },
  {
    "model": "SepsisEarlyWarning",
    "positives": 6318,
    "total": 25000,
    "rate": 0.2527
  },
  {
    "model": "HypertensionControlPredictor",
    "positives": 5865,
    "total": 25000,
    "rate": 0.2346
  },
  {
    "model": "AKIRiskPredictor",
    "positives": 4362,
    "total": 25000,
    "rate": 0.1745
  },
  {
    "model": "MortalityRiskModel",
    "positives": 1635,
    "total": 25000,
    "rate": 0.0654
  },
  {
    "model": "ICUAdmissionPredictor",
    "positives": 1581,
    "total": 25000,
    "rate": 0.0632
  },
  {
    "model": "HeartFailure30DRisk",
    "positives": 1345,
    "total": 25000,
    "rate": 0.0538
  },
  {
    "model": "StrokeRiskPredictor",
    "positives": 112,
    "total": 25000,
    "rate": 0.0045
  },
  {
    "model": "NoShowAppointmentPredictor",
    "positives": 8,
    "total": 25000,
    "rate": 0.0003
  },
  {
    "model": "ReadmissionPredictor",
    "positives": 0,
    "total": 25000,
    "rate": 0.0
  },
  {
    "model": "Readmission90DPredictor",
    "positives": 0,
    "total": 25000,
    "rate": 0.0
  },
  {
    "model": "COPDExacerbationPredictor",
    "positives": 0,
    "total": 25000,
    "rate": 0.0
  },
  {
    "model": "AdverseDrugEventPredictor",
    "positives": 0,
    "total": 25000,
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
    "patient_id": "700794",
    "positive_models": 8,
    "avg_score": 0.6658,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0852650966393731,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0852650966393731,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9599173069000244,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9725525379180908,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9996908903121948,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9990999698638916,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6173113047125964,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9915346503257751,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6674649715423584,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.36746874925909195,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9982207417488098,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.43700684587964456,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4750630587068073,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.139861434850064
      },
      "CostOfCareRegressor": {
        "prediction": 8937.3271484375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.7121760681826617
      }
    }
  },
  {
    "patient_id": "703287",
    "positive_models": 8,
    "avg_score": 0.6471,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06518285823757825,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06518285823757825,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.970725417137146,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8661013245582581,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9998455047607422,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999533891677856,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6436066278299295,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9906773567199707,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5623235702514648,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.34096919802855646,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9987347722053528,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.43901956081585913,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4694716723070649,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.1315034697201725
      },
      "CostOfCareRegressor": {
        "prediction": 9475.9755859375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.2601290517919144
      }
    }
  },
  {
    "patient_id": "724634",
    "positive_models": 8,
    "avg_score": 0.6432,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06984824480088422,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06984824480088422,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9457762837409973,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9214869141578674,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9999706745147705,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9994564652442932,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6112729814549408,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9016133546829224,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6434189677238464,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3352012380142376,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.994633674621582,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.431781684690028,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.43763175247240915,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.136515847242896
      },
      "CostOfCareRegressor": {
        "prediction": 9208.4658203125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 7.522593345438736
      }
    }
  },
  {
    "patient_id": "709736",
    "positive_models": 8,
    "avg_score": 0.6431,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05891422895856258,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05891422895856258,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9482250213623047,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9422558546066284,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9963680505752563,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9989699125289917,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6380572420526867,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8571870923042297,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6820459961891174,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.33178200812790076,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9914351105690002,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4031069698243917,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.45279462473361803,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.29922740943946
      },
      "CostOfCareRegressor": {
        "prediction": 8955.1337890625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.113932007349477
      }
    }
  },
  {
    "patient_id": "715281",
    "positive_models": 8,
    "avg_score": 0.6424,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0616363799991608,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0616363799991608,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8100405335426331,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9919127225875854,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9888867735862732,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9995842576026917,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5211572373811583,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9573498964309692,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.8168537020683289,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.30373156910053334,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.986994206905365,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.37750596003174947,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4740245149857559,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.190774055103072
      },
      "CostOfCareRegressor": {
        "prediction": 9112.13671875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 7.081537408633985
      }
    }
  },
  {
    "patient_id": "702494",
    "positive_models": 8,
    "avg_score": 0.6416,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.08005543161099854,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.08005543161099857,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.6811802387237549,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.987396776676178,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9950849413871765,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9951255917549133,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6677732466918319,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9796372056007385,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6543460488319397,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3440184591668079,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9789415597915649,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4213558316262896,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.47647374371667117,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.031739957613282
      },
      "CostOfCareRegressor": {
        "prediction": 9202.998046875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.1561075523526916
      }
    }
  },
  {
    "patient_id": "704945",
    "positive_models": 8,
    "avg_score": 0.639,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05822968847789062,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05822968847789062,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8683813214302063,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9218722581863403,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9976760745048523,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9964146614074707,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6201769687938423,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9337974786758423,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6646972298622131,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.32452467180346134,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9708800911903381,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.40663148278521155,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4850877569082966,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.250970824249321
      },
      "CostOfCareRegressor": {
        "prediction": 9060.19140625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.3370506763926637
      }
    }
  },
  {
    "patient_id": "718931",
    "positive_models": 8,
    "avg_score": 0.6381,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.08250409255986993,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.08250409255986993,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.5215542316436768,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9999089241027832,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9988558292388916,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9994465708732605,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6535019205291481,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9981424808502197,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7275780439376831,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.36375283296692656,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.993748664855957,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4190336933468006,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4548499576174628,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.264350447341107
      },
      "CostOfCareRegressor": {
        "prediction": 8957.822265625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.271947084240197
      }
    }
  },
  {
    "patient_id": "712107",
    "positive_models": 8,
    "avg_score": 0.6374,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.04744705830588102,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.04744705830588102,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9759660959243774,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8250411748886108,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9986116886138916,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9995391368865967,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6313172928592813,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9423941969871521,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6072959303855896,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3442068122480258,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9985336065292358,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.422616241416302,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.44586613225130095,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.790958331909507
      },
      "CostOfCareRegressor": {
        "prediction": 9055.958984375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.571364964011606
      }
    }
  },
  {
    "patient_id": "705447",
    "positive_models": 8,
    "avg_score": 0.6327,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.07196879920037076,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.07196879920037076,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8951690793037415,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9026495814323425,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9951651096343994,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9968611001968384,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6774521469749174,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9771022200584412,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5378161668777466,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.31446313116366476,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9678792953491211,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.33916962533633893,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4780396331272387,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.940701611607022
      },
      "CostOfCareRegressor": {
        "prediction": 9399.7294921875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.616735951939847
      }
    }
  },
  {
    "patient_id": "704556",
    "positive_models": 8,
    "avg_score": 0.6322,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.07417065637621252,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.07417065637621252,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8912990689277649,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9866505861282349,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9960695505142212,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.999972939491272,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5416102661544916,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9583398103713989,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5389685034751892,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.30121115118925823,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9916231036186218,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4018125776045892,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.46308848925022317,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.2345539593270765
      },
      "CostOfCareRegressor": {
        "prediction": 8987.8388671875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.441672453611045
      }
    }
  },
  {
    "patient_id": "718470",
    "positive_models": 8,
    "avg_score": 0.6296,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05209631830008325,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05209631830008325,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7402060031890869,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9728639721870422,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9987561702728271,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9986023306846619,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6621042177731162,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9070113897323608,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6373658776283264,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3326232378828744,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9733198881149292,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.3993889449775608,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4580278402404169,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.956247583570216
      },
      "CostOfCareRegressor": {
        "prediction": 8790.0439453125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.7900353705740795
      }
    }
  },
  {
    "patient_id": "708427",
    "positive_models": 8,
    "avg_score": 0.6276,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05431939664383692,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05431939664383691,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9473901391029358,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7230660915374756,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9989758729934692,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999020099639893,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6628546679016355,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9136514067649841,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6821447610855103,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.32534061654423413,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9786024689674377,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.3860410822239125,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.43219874411745013,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.072547335250918
      },
      "CostOfCareRegressor": {
        "prediction": 8876.998046875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 7.465935108083994
      }
    }
  },
  {
    "patient_id": "720995",
    "positive_models": 8,
    "avg_score": 0.6263,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0620795633746639,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0620795633746639,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7393930554389954,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9836977124214172,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9983373880386353,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9998867511749268,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6379147640811513,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.884647786617279,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6006042957305908,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.33184535176130536,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9780685305595398,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.42364741331619366,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4395609532241999,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.338830713017274
      },
      "CostOfCareRegressor": {
        "prediction": 8927.6357421875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.669932793392637
      }
    }
  },
  {
    "patient_id": "721786",
    "positive_models": 8,
    "avg_score": 0.6253,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05011526900885951,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.050115269008859514,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7803305387496948,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8876441121101379,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9969263672828674,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999703168869019,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6024149726236862,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8733803629875183,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7697282433509827,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3059714804228344,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9803624749183655,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.36155564392314193,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.46987089703029045,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.263150858437678
      },
      "CostOfCareRegressor": {
        "prediction": 9032.8349609375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.595590258105282
      }
    }
  },
  {
    "patient_id": "715496",
    "positive_models": 8,
    "avg_score": 0.6232,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05688983845476718,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05688983845476718,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7756873965263367,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9445080757141113,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9989970326423645,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9998477697372437,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.634529275563548,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8743183612823486,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6443250179290771,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3328949977973192,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9365306496620178,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4160976469577464,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.430420585173666,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.008664991638967
      },
      "CostOfCareRegressor": {
        "prediction": 8817.5029296875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 7.280793495001547
      }
    }
  },
  {
    "patient_id": "720407",
    "positive_models": 8,
    "avg_score": 0.6228,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05372347306990735,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05372347306990735,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7704387307167053,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9570621848106384,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9980917572975159,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9996968507766724,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6232928460757524,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.925020158290863,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5461995601654053,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3457216545469487,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9688200950622559,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.41725894979944744,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.43723850969306766,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.90714028168484
      },
      "CostOfCareRegressor": {
        "prediction": 8906.1201171875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.446944591277782
      }
    }
  },
  {
    "patient_id": "707334",
    "positive_models": 8,
    "avg_score": 0.622,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.044826099737824913,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0448260997378249,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8880965113639832,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8234550952911377,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9998527765274048,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9998618364334106,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6422341760807861,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.7704805731773376,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6898917555809021,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.32996720925331635,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9959768652915955,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4114540155265135,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4455581014195119,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.114820931262873
      },
      "CostOfCareRegressor": {
        "prediction": 8851.6015625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.309640599059961
      }
    }
  },
  {
    "patient_id": "724606",
    "positive_models": 8,
    "avg_score": 0.6217,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06330082166869083,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06330082166869082,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7743557095527649,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9721968173980713,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9938932657241821,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9997001886367798,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5964416852749113,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9152306914329529,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5109589099884033,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.331317311192996,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9709621667861938,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.45113573215472497,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4393561961255134,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.367981371628857
      },
      "CostOfCareRegressor": {
        "prediction": 9186.6787109375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 7.753526115281369
      }
    }
  },
  {
    "patient_id": "706079",
    "positive_models": 8,
    "avg_score": 0.6202,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.04773432165745642,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.04773432165745641,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.956017792224884,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.871269166469574,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9980272650718689,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9998507499694824,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.55366386827704,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9360808730125427,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5210433006286621,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.29968042166716397,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9783017635345459,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.3862319488624192,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.46694224483188357,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.355221980224941
      },
      "CostOfCareRegressor": {
        "prediction": 8966.7705078125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.975706677663837
      }
    }
  }
]
```

## Appendix – Top Anomalies
```json
[
  {
    "patient_id": "703284",
    "anomaly_flag": 1,
    "anomaly_score": 0.12188862826320579
  },
  {
    "patient_id": "705383",
    "anomaly_flag": 1,
    "anomaly_score": 0.12074894891831267
  },
  {
    "patient_id": "721056",
    "anomaly_flag": 1,
    "anomaly_score": 0.11396205671992998
  },
  {
    "patient_id": "715255",
    "anomaly_flag": 1,
    "anomaly_score": 0.10910455286312937
  },
  {
    "patient_id": "722219",
    "anomaly_flag": 1,
    "anomaly_score": 0.10672841666801502
  },
  {
    "patient_id": "709094",
    "anomaly_flag": 1,
    "anomaly_score": 0.1060821403787503
  },
  {
    "patient_id": "706023",
    "anomaly_flag": 1,
    "anomaly_score": 0.10444476132190239
  },
  {
    "patient_id": "703130",
    "anomaly_flag": 1,
    "anomaly_score": 0.10131977785377888
  },
  {
    "patient_id": "701507",
    "anomaly_flag": 1,
    "anomaly_score": 0.09835400006699346
  },
  {
    "patient_id": "724312",
    "anomaly_flag": 1,
    "anomaly_score": 0.09602257354395827
  },
  {
    "patient_id": "705449",
    "anomaly_flag": 1,
    "anomaly_score": 0.09490379960200712
  },
  {
    "patient_id": "708359",
    "anomaly_flag": 1,
    "anomaly_score": 0.09412838059478434
  },
  {
    "patient_id": "722992",
    "anomaly_flag": 1,
    "anomaly_score": 0.09361510795758188
  },
  {
    "patient_id": "708173",
    "anomaly_flag": 1,
    "anomaly_score": 0.09303251744006691
  },
  {
    "patient_id": "701958",
    "anomaly_flag": 1,
    "anomaly_score": 0.09264186506181282
  },
  {
    "patient_id": "711544",
    "anomaly_flag": 1,
    "anomaly_score": 0.09143106177494431
  },
  {
    "patient_id": "717115",
    "anomaly_flag": 1,
    "anomaly_score": 0.09092091265748614
  },
  {
    "patient_id": "711598",
    "anomaly_flag": 1,
    "anomaly_score": 0.08961110265698802
  },
  {
    "patient_id": "701782",
    "anomaly_flag": 1,
    "anomaly_score": 0.08821395096929541
  },
  {
    "patient_id": "702728",
    "anomaly_flag": 1,
    "anomaly_score": 0.08789108737110973
  }
]
```