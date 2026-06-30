from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

model = joblib.load("student_retention_model.joblib") 

class StudentInput(BaseModel):[cite: 2]
    student_id: str = Field(alias="Student_ID", default="Unknown")
    marital_status: int = Field(alias="Marital status")[cite: 2]
    application_mode: int = Field(alias="Application mode")[cite: 2]
    course: int = Field(alias="Course")
    attendance: int = Field(alias="Daytime/evening attendance")
    prev_qual: int = Field(alias="Previous qualification")
    father_qual: int = Field(alias="Father's qualification")
    father_occ: int = Field(alias="Father's occupation")
    displaced: int = Field(alias="Displaced")
    debtor: int = Field(alias="Debtor")
    tuition: int = Field(alias="Tuition fees up to date")
    gender: int = Field(alias="Gender")
    scholarship: int = Field(alias="Scholarship holder")
    grade_1: float = Field(alias="Curricular units 1st sem (grade)")
    grade_2: float = Field(alias="Curricular units 2nd sem (grade)")
    approved_1: int = Field(alias="Curricular units 1st sem (approved)")
    approved_2: int = Field(alias="Curricular units 2nd sem (approved)")
    age: int = Field(alias="Age at enrollment")
    unemployment: float = Field(alias="Unemployment rate")
    inflation: float = Field(alias="Inflation rate")
    gdp: float = Field(alias="GDP")
    grade_change: float = Field(alias="Grade_Change")
    total_approved: int = Field(alias="Total_Approved_Units")
    approved_change: int = Field(alias="Approved_Units_Change")
    efficiency: float = Field(alias="Academic_Efficiency")
    fin_risk: int = Field(alias="Financial_Risk_Score")
    non_trad: int = Field(alias="Non_Traditional_Student")
    father_higher: int = Field(alias="Father_Higher_Ed")

@app.post("/predict")
def predict(data: StudentInput):
    features_dict = data.dict(by_alias=True) # Extract JSON data using actual column names
    df = pd.DataFrame([features_dict])
    expected_cols = model.feature_names_in_ # Model alignment
    df = df.reindex(columns=expected_cols, fill_value=0)
    
    pred = model.predict(df)[0]
    probas = model.predict_proba(df)[0] # Probabilities, since Random Forest model is trained 
                                        # to classify students into three categories 
                                        # (Enrolled, Dropout, Graduate)
    
    return {
        "prediction": str(pred),
        "confidence_percent": round(float(np.max(probas)) * 100, 2),
        "agent_context": {
            "dropout_risk": round(float(probas[0]) * 100, 1),
            "enrolled_prob": round(float(probas[1]) * 100, 1),
            "graduate_prob": round(float(probas[2]) * 100, 1)
        }
    }