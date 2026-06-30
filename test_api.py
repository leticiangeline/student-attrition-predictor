import requests
import json

url = "http://127.0.0.1:8000/predict"

sample_student = {
    "Marital status": 1,
    "Application mode": 1,
    "Course": 9238,
    "Daytime/evening attendance": 1,
    "Previous qualification": 1,
    "Father's qualification": 3,
    "Father's occupation": 4,
    "Displaced": 1,
    "Debtor": 1,                  
    "Tuition fees up to date": 0, 
    "Gender": 0,
    "Scholarship holder": 0,      
    "Curricular units 1st sem (grade)": 13.5,
    "Curricular units 2nd sem (grade)": 10.0,
    "Curricular units 1st sem (approved)": 6,
    "Curricular units 2nd sem (approved)": 4,
    "Age at enrollment": 22,
    "Unemployment rate": 10.8,
    "Inflation rate": 1.4,
    "GDP": 1.74,
    "Grade_Change": -3.5,
    "Total_Approved_Units": 10,
    "Approved_Units_Change": -2,
    "Academic_Efficiency": 2.35,
    "Financial_Risk_Score": 2,
    "Non_Traditional_Student": 0,
    "Father_Higher_Ed": 0
}

r = requests.post(url, json=sample_student)

print(r.json())