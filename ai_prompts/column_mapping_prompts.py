
COLUMN_MAPPING_PROMPT = """
Identify semantic types for each column in a hospital EHR-like CSV.
Map to: patient_id, age, sex, vitals (systolic_bp, diastolic_bp, heart_rate),
labs (glucose, cholesterol, hemoglobin), diagnosis, medication, procedure, outcome/label, and other.
Return JSON: {column_mappings:{col:{detected_type:str}}, data_quality_score:float}.
"""
