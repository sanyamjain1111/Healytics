# Clinical Analysis Report – Dataset 20
_Generated: 20250922_002752_

## Executive Summary
This analysis utilized 14 classification models and 3 regression models to assess risk factors within a dataset of 5000 patients.  The dataset, comprised of 500 rows and 27 columns, included demographic, clinical, and laboratory data.  Preprocessing steps involved standardization of numerical features, one-hot encoding of categorical features, outlier management via Winsorization, and imputation of missing values.  SepsisEarlyWarning exhibited the highest prevalence at 33.08%, indicating a substantial portion of the population at risk for sepsis.  ICUAdmissionPredictor (14.66% prevalence) and MortalityRiskModel (11.92% prevalence) also showed notable risk levels.  Conversely, ReadmissionPredictor and Readmission90DPredictor showed 0% prevalence, suggesting potential issues with these models or data deficiencies in capturing readmission events.  Furthermore, a significant number of anomalies (449 out of 5000) were detected, requiring further investigation to determine their impact on model performance and reliability.  These findings highlight the need for enhanced monitoring and triage of patients at high risk for sepsis, ICU admission, and mortality.  The observed anomalies warrant review to ensure data integrity, potentially influencing future model development and refinement.  Improving data quality and considering additional risk factors may improve model performance and inform more accurate risk stratification, leading to more effective resource allocation and improved patient outcomes.

## Key Findings
- SepsisEarlyWarning model showed the highest prevalence (33.08%) among all classification models.
- ICUAdmissionPredictor and MortalityRiskModel exhibited prevalences of 14.66% and 11.92%, respectively.
- ReadmissionPredictor and Readmission90DPredictor showed 0% prevalence, indicating potential model or data issues.
- A total of 449 anomalies were identified within the dataset of 5000 patients.
- Regression models (LengthOfStayRegressor, CostOfCareRegressor, AnemiaSeverityRegressor) had 0 observations.

## Recommendations
- Investigate the 0% prevalence in ReadmissionPredictor and Readmission90DPredictor; review data collection and model training.
- Prioritize patients identified as high-risk by SepsisEarlyWarning, ICUAdmissionPredictor, and MortalityRiskModel for prompt clinical intervention.
- Conduct a thorough investigation into the 449 identified dataset anomalies to assess their impact and implement corrective measures.
- Explore additional risk factors and refine model inputs to improve predictive accuracy for all models, particularly those with low prevalence.
- Develop and implement a standardized data quality control process to prevent future anomaly occurrences.

## Cohorts of Interest
- **High-Risk Sepsis Cohort** – Patients flagged as high-risk by the SepsisEarlyWarning model. — This cohort represents a substantial portion of the patient population (33.08%) at immediate risk of sepsis, necessitating focused clinical attention and intervention.
- **High-Risk ICU Admission Cohort** – Patients with high predicted probability of ICU admission according to the ICUAdmissionPredictor model. — Early identification of patients likely to require ICU admission allows for proactive resource allocation and optimized care pathways.

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
        "score": 0.07110754077416699,
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
        "score": 0.44921519914422325,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.05094064387351
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
        "score": 0.18177155331418227,
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
        "score": 0.4718662922890904,
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
        "score": 0.35089127468295084,
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
        "score": 0.4867124031022065,
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
        "prediction": 2.57772152736604
      }
    }
  },
  {
    "patient_id": "902614",
    "positive_models": 8,
    "avg_score": 0.6672,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.08679810694397942,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.08679810694397942,
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
        "score": 0.4818614786439222,
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
        "score": 0.4627131110342607,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.393777681491016
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
        "prediction": 6.1325390782618605
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
        "score": 0.34207547177583597,
        "pred": 0,
        "threshold": 0.5
      },
      "AKIRiskPredictor": {
        "score": 0.9902861714363098,
        "pred": 1,
        "threshold": 0.5
      },
      "AdverseDrugEventPredictor": {
        "score": 0.43921131443191236,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4696017758296018,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.583058846125631
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
        "prediction": 7.241677770562909
      },
      "CostOfCareRegressor": {
        "prediction": 8912.5947265625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 9.924925762393448
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
        "score": 0.4332315111399728,
        "pred": 0,
        "threshold": 0.5
      },
      "NoShowAppointmentPredictor": {
        "score": 0.4503232957319971,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.291570322500222
      },
      "CostOfCareRegressor": {
        "prediction": 8894.37890625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 3.844367830206427
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
        "score": 0.06129427953493756,
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
        "prediction": 6.444553008606419
      },
      "CostOfCareRegressor": {
        "prediction": 8988.0517578125
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.573977409688371
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
        "score": 0.46393428728002134,
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
        "prediction": 6.254213975091638
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
        "score": 0.462310258773121,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.986855141991214
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
        "score": 0.0669709276179284,
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
        "score": 0.4719222527404018,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.776462912939344
      },
      "CostOfCareRegressor": {
        "prediction": 9232.3544921875
      },
      "AnemiaSeverityRegressor": {
        "prediction": 5.548805840666985
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
        "score": 0.06467347773693714,
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
        "prediction": 5.9278519148139655
      }
    }
  },
  {
    "patient_id": "900514",
    "positive_models": 8,
    "avg_score": 0.6333,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.06279858725552943,
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
        "score": 0.46499829599144427,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.915741029619423
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
        "score": 0.5247878207200692,
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
        "score": 0.45267997628071,
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
        "score": 0.049980959912684225,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.049980959912684225,
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
        "score": 0.46895499617579517,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.901063897586296
      },
      "CostOfCareRegressor": {
        "prediction": 9136.40625
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.0249025951330735
      }
    }
  },
  {
    "patient_id": "900197",
    "positive_models": 8,
    "avg_score": 0.6146,
    "models": {
      "ReadmissionPredictor": {
        "score": 0.05510482971465451,
        "pred": 0,
        "threshold": 0.5
      },
      "Readmission90DPredictor": {
        "score": 0.05510482971465451,
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
        "score": 0.34014279907291095,
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
        "score": 0.4708519860986094,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 5.86427893499081
      },
      "CostOfCareRegressor": {
        "prediction": 9168.7802734375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 6.614921961137811
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
        "score": 0.45958341661282254,
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
        "score": 0.5643926759307056,
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
        "score": 0.457057162705985,
        "pred": 0,
        "threshold": 0.5
      },
      "LengthOfStayRegressor": {
        "prediction": 6.182801207655762
      },
      "CostOfCareRegressor": {
        "prediction": 9019.7109375
      },
      "AnemiaSeverityRegressor": {
        "prediction": 4.026589441474037
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