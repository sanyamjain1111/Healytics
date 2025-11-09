# Clinical Analysis Report – Dataset 20
_Generated: 20250922_105003_

## Executive Summary
This analysis utilized 14 classification models and 2 regression models to predict various patient outcomes using a dataset comprising 5000 patient records.  The models incorporated preprocessing steps including standardization of numerical features, one-hot encoding of categorical features, outlier handling via Winsorization, and imputation using median/mode.  SepsisEarlyWarning showed the highest prevalence (33.08%), indicating a substantial portion of the population at risk for sepsis.  ICUAdmissionPredictor (14.66%) and MortalityRiskModel (11.92%) also demonstrated substantial prevalence, highlighting a significant number of patients requiring intensive care or facing mortality risk. ReadmissionPredictor and Readmission90DPredictor reported zero positives, suggesting either model deficiency or a very low base rate in the dataset.  The 449 anomalies identified within the dataset warrant further investigation to determine their nature and potential impact on model performance.  The prevalence of sepsis and critical care needs suggests that optimizing sepsis management protocols and ICU resource allocation may be key priorities. Early identification of high-risk patients enables targeted interventions and improved care pathways. The lack of positive predictions in readmission models requires further evaluation and validation.  This may highlight a problem with the model or with the data used to train the model. This underscores the importance of data quality and model validation for accurate risk stratification. Operational triage may benefit from prioritizing patients identified as high-risk by the SepsisEarlyWarning, ICUAdmissionPredictor, and MortalityRiskModel.  Integrating these model outputs into clinical workflows could facilitate more proactive patient management and improve resource allocation.

## Key Findings
- SepsisEarlyWarning had the highest prevalence (33.08%), indicating a significant number of patients at risk for sepsis.
- ICUAdmissionPredictor (14.66%) and MortalityRiskModel (11.92%) showed high prevalence, highlighting critical care needs.
- ReadmissionPredictor and Readmission90DPredictor showed zero positive predictions, requiring further investigation.
- 449 anomalies were identified, potentially impacting model accuracy and requiring further analysis.
- The dataset contained 5000 records with substantial variation in risk prediction across different models.

## Recommendations
- Prioritize improvement of readmission prediction models (ReadmissionPredictor and Readmission90DPredictor).
- Investigate the 449 data anomalies to assess their impact on model performance and correct accordingly.
- Develop workflows to integrate high-risk patient identification (from SepsisEarlyWarning, ICUAdmissionPredictor, and MortalityRiskModel) into clinical protocols.
- Optimize resource allocation for sepsis management and ICU care based on model predictions.
- Implement proactive intervention strategies for patients identified as high-risk by the top-performing models.

## Cohorts of Interest
- **Sepsis High-Risk Patients** – Patients with SepsisEarlyWarning score above 0.5 — This cohort represents a substantial portion of the population (33.08%) at risk for a potentially life-threatening condition requiring immediate attention.
- **Critical Care Patients** – Patients with ICUAdmissionPredictor or MortalityRiskModel score above 0.5 — This cohort identifies individuals requiring intensive care or facing high mortality risk, enabling proactive resource allocation and targeted interventions.

## Appendix – Model Snapshot
```json
[
  {
    "model": "SepsisEarlyWarning",
    "positives": 1654,
    "total": 5000,
    "rate": 0.3308
  },
  {
    "model": "DiabetesComplicationRisk",
    "positives": 1633,
    "total": 5000,
    "rate": 0.3266
  },
  {
    "model": "HypertensionControlPredictor",
    "positives": 1545,
    "total": 5000,
    "rate": 0.309
  },
  {
    "model": "AKIRiskPredictor",
    "positives": 1240,
    "total": 5000,
    "rate": 0.248
  },
  {
    "model": "ICUAdmissionPredictor",
    "positives": 733,
    "total": 5000,
    "rate": 0.1466
  },
  {
    "model": "HeartFailure30DRisk",
    "positives": 655,
    "total": 5000,
    "rate": 0.131
  },
  {
    "model": "MortalityRiskModel",
    "positives": 596,
    "total": 5000,
    "rate": 0.1192
  },
  {
    "model": "StrokeRiskPredictor",
    "positives": 102,
    "total": 5000,
    "rate": 0.0204
  },
  {
    "model": "NoShowAppointmentPredictor",
    "positives": 8,
    "total": 5000,
    "rate": 0.0016
  },
  {
    "model": "AdverseDrugEventPredictor",
    "positives": 1,
    "total": 5000,
    "rate": 0.0002
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
    "model": "COPDExacerbationPredictor",
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
    "patient_id": "901708",
    "positive_models": 9,
    "avg_score": 0.6418,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.07110754077416698,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.07110754077416699,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.7766645550727844,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9693441987037659,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.999885082244873,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999401569366455,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6107244791162627,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9198001027107239,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.642964243888855,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.33263426002358615,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9910001158714294,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.5095354668701565,
        "pred": 1,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4492151991442233,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.050940643873511
      },
      "CostOfCareRegressor": {
        "prediction": 9080.5703125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.857824784016828
      }
    }
  },
  {
    "patient_id": "904478",
    "positive_models": 8,
    "avg_score": 0.6849,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.1817715533141823,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.18177155331418227,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9947220087051392,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.993815541267395,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9999966621398926,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9995554089546204,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5646180858029523,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9940592050552368,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.673149585723877,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.351580296987609,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9997476935386658,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.49702471704355455,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4718662922890903,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.312267638028551
      },
      "CostOfCareRegressor": {
        "prediction": 9046.869140625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 8.360432012614808
      }
    }
  },
  {
    "patient_id": "904446",
    "positive_models": 8,
    "avg_score": 0.6675,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.1345954583841836,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.1345954583841836,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9986661672592163,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9491785168647766,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9995817542076111,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999947547912598,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.620964118120278,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9699953198432922,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5755126476287842,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3508912746829509,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9975743889808655,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4594364316921395,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.48671240310220654,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.12685855709309
      },
      "CostOfCareRegressor": {
        "prediction": 8646.5732421875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.577721527366041
      }
    }
  },
  {
    "patient_id": "902614",
    "positive_models": 8,
    "avg_score": 0.6672,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.08679810694397944,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.08679810694397944,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9872848391532898,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9503936767578125,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9997997879981995,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999511241912842,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6212207187464384,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9824728965759277,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6961304545402527,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.32822655586777905,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9994884729385376,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4526397701672054,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4818614786439221,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.220789189983314
      },
      "CostOfCareRegressor": {
        "prediction": 9323.8291015625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.4671898551913234
      }
    }
  },
  {
    "patient_id": "904741",
    "positive_models": 8,
    "avg_score": 0.6627,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0648616552728069,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0648616552728069,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8997639417648315,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.971169650554657,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9980529546737671,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9993492960929871,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6600650815524626,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9710818529129028,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.766150712966919,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.33687049989706513,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9931049942970276,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.42748345307424596,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.46271311103426077,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.393777681491017
      },
      "CostOfCareRegressor": {
        "prediction": 8988.99609375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.243280836451905
      }
    }
  },
  {
    "patient_id": "902701",
    "positive_models": 8,
    "avg_score": 0.6598,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0676583623235898,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0676583623235898,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9876148700714111,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9855327010154724,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9998503923416138,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999510049819946,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5225413019694066,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9940471649169922,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7451618909835815,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.30391818530634745,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9963297247886658,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.42416289306578026,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4827555708579302,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.197907254572995
      },
      "CostOfCareRegressor": {
        "prediction": 9424.4287109375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.13253907826186
      }
    }
  },
  {
    "patient_id": "904061",
    "positive_models": 8,
    "avg_score": 0.6586,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06956703079848903,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06956703079848901,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9169246554374695,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8890905976295471,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9997209906578064,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999819993972778,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6559282173428981,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9900842905044556,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7297107577323914,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3420754717758359,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9902861714363098,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4392113144319123,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.46960177582960183,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.583058846125632
      },
      "CostOfCareRegressor": {
        "prediction": 9176.220703125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.235598125497829
      }
    }
  },
  {
    "patient_id": "902600",
    "positive_models": 8,
    "avg_score": 0.6559,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.11018107868921295,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.11018107868921295,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9942355751991272,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9865216016769409,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9999573230743408,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999510049819946,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5811729843747777,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.998908519744873,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5130465626716614,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3308882607401024,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9995729327201843,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.44551885359898546,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4563362115673499,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 7.2416777705629105
      },
      "CostOfCareRegressor": {
        "prediction": 8912.5947265625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 9.924925762393443
      }
    }
  },
  {
    "patient_id": "901983",
    "positive_models": 8,
    "avg_score": 0.6538,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06078978742702213,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06078978742702213,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9078007340431213,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9781088829040527,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9986862540245056,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999368190765381,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.7014880302120514,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9482188820838928,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6177409291267395,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.34485527861589205,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9974676370620728,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.43323151113997277,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4503232957319971,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.291570322500223
      },
      "CostOfCareRegressor": {
        "prediction": 8894.37890625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.8443678302064264
      }
    }
  },
  {
    "patient_id": "903011",
    "positive_models": 8,
    "avg_score": 0.6516,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.061294279534937546,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.061294279534937546,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9707733392715454,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8319844603538513,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9985451698303223,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999799728393555,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6002424551789112,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9621134996414185,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.8482788801193237,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3079271700882491,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9917013049125671,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.3765441440142114,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4603191640612712,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.4445530086064196
      },
      "CostOfCareRegressor": {
        "prediction": 8988.0517578125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.573977409688375
      }
    }
  },
  {
    "patient_id": "900841",
    "positive_models": 8,
    "avg_score": 0.6439,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0717864667942594,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.0717864667942594,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.9624335169792175,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9300618171691895,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.999093770980835,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999810457229614,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5972298690929108,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9774002432823181,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6259503960609436,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.31750271644146244,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9871782064437866,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.36676869416293445,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4639342872800213,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.418961568211916
      },
      "CostOfCareRegressor": {
        "prediction": 9092.6455078125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.254213975091639
      }
    }
  },
  {
    "patient_id": "900371",
    "positive_models": 8,
    "avg_score": 0.6434,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06423480569932533,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06423480569932533,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8400111794471741,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.97651606798172,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9928038716316223,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9962838292121887,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.665725830804931,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9814941883087158,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5694954991340637,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.35493985366172354,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9698405861854553,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4267750471247422,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.46231025877312104,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.986855141991215
      },
      "CostOfCareRegressor": {
        "prediction": 9164.6416015625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.767099227484661
      }
    }
  },
  {
    "patient_id": "902140",
    "positive_models": 8,
    "avg_score": 0.643,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.0669709276179284,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06697092761792842,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8216380476951599,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9967683553695679,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9870263934135437,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.6407463550567627,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6978985906241295,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9851769208908081,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.8934406638145447,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3797368405494144,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9094416499137878,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4418012800627617,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.47192225274040167,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.776462912939345
      },
      "CostOfCareRegressor": {
        "prediction": 9232.3544921875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.548805840666986
      }
    }
  },
  {
    "patient_id": "900001",
    "positive_models": 8,
    "avg_score": 0.6351,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06467347773693714,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06467347773693716,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8190279603004456,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9669058322906494,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9815105199813843,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9913949370384216,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6618915448457311,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9675732851028442,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5861998796463013,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3432277905145277,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.932256817817688,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.424300049141081,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4524517287596986,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.033917815175547
      },
      "CostOfCareRegressor": {
        "prediction": 9176.4140625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.927851914813963
      }
    }
  },
  {
    "patient_id": "900514",
    "positive_models": 8,
    "avg_score": 0.6333,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06279858725552942,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.06279858725552942,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.836731493473053,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9436192512512207,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.987143337726593,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9826854467391968,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.7118074333838849,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9837672710418701,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.5093483924865723,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3600031342845601,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9631351828575134,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.3642359990594942,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4649982959914442,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.915741029619422
      },
      "CostOfCareRegressor": {
        "prediction": 9185.0302734375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.129969602552248
      }
    }
  },
  {
    "patient_id": "902652",
    "positive_models": 8,
    "avg_score": 0.6298,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.04110756950498038,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.04110756950498038,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8716514706611633,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9555936455726624,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9986263513565063,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9997987151145935,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5247878207200694,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8415949940681458,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.7676637768745422,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3037667150923722,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9950913190841675,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.39345495582844237,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.45267997628070994,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.509047213068069
      },
      "CostOfCareRegressor": {
        "prediction": 9098.228515625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.236422312192442
      }
    }
  },
  {
    "patient_id": "903979",
    "positive_models": 8,
    "avg_score": 0.6153,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.04998095991268423,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.04998095991268423,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.5104073882102966,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9715549945831299,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9890652894973755,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9921594858169556,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6712709335605219,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9724512100219727,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6331846714019775,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3316838064391062,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9670443534851074,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.3915009205881671,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4689549961757952,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.901063897586297
      },
      "CostOfCareRegressor": {
        "prediction": 9136.40625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.024902595133073
      }
    }
  },
  {
    "patient_id": "900197",
    "positive_models": 8,
    "avg_score": 0.6146,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05510482971465452,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05510482971465452,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.6209083199501038,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.9341083765029907,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9830650091171265,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.996310293674469,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6158543258610055,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.9492268562316895,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6011004447937012,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.34014279907291106,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9606321454048157,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.4071047422766639,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.47085198609860945,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.864278934990811
      },
      "CostOfCareRegressor": {
        "prediction": 9168.7802734375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.614921961137813
      }
    }
  },
  {
    "patient_id": "904553",
    "positive_models": 8,
    "avg_score": 0.6135,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05237309009937752,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05237309009937752,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8859542012214661,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.7865534424781799,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9997829794883728,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9999567270278931,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.6482608625367575,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8973551392555237,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.512286365032196,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.3203441040654604,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9969832301139832,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.36412714405722096,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4595834166128225,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.001393893383197
      },
      "CostOfCareRegressor": {
        "prediction": 8866.9677734375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 2.769246768055422
      }
    }
  },
  {
    "patient_id": "900673",
    "positive_models": 8,
    "avg_score": 0.605,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.043150114654277705,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.043150114654277705,
        "pred": 0,
        "threshold": 0.5
      },
      "MortalityRiskModel": {
        "score": 0.8007239103317261,
        "pred": 1,
        "threshold": 0.5
      },
      "ICUAdmissionPredictor": {
        "score": 0.8661659955978394,
        "pred": 1,
        "threshold": 0.5
      },
      "SepsisEarlyWarning": {
        "score": 0.9872610569000244,
        "pred": 1,
        "threshold": 0.5
      },
      "DiabetesComplicationRisk": {
        "score": 0.9997796416282654,
        "pred": 1,
        "threshold": 0.5
      },
      "HypertensionControlPredictor": {
        "score": 0.5643926759307055,
        "pred": 1,
        "threshold": 0.5
      },
      "HeartFailure30DRisk": {
        "score": 0.8377282619476318,
        "pred": 1,
        "threshold": 0.5
      },
      "StrokeRiskPredictor": {
        "score": 0.6291979551315308,
        "pred": 1,
        "threshold": 0.5
      },
      "COPDExacerbationPredictor": {
        "score": 0.28098072447653966,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9752214550971985,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.38070383188392426,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.45705716270598507,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.182801207655765
      },
      "CostOfCareRegressor": {
        "prediction": 9019.7109375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.026589441474036
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