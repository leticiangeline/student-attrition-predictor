import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Student Retention Classifier", layout="wide")

st.title("🎓 Student Retention Classifier")
st.markdown("Enter **real** student data to get an accurate prediction.")

# Assign dropdown choices to variables for mapping
marital_map = {'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4, 'Facto Union': 5, 'Separated': 6}

app_mode_map = {
    '1st Phase (SPM/STPM)': 1, 'Ord 612/93': 2, '1st Phase (Sabah)': 3, 'Private Institution': 4, 
    'Ord 854-B/99': 5, 'International Student': 6, '1st Phase (Sarawak)': 7, '2nd Phase (SPM/STPM)': 8, 
    '3rd Phase (SPM/STPM)': 9, 'Ord 533-A (Diff)': 10, 'Ord 533-A (Other)': 11, 'Age 23+ (PJJ)': 12, 
    'Transfer (Internal)': 13, 'Course Change': 14, 'Technical Diploma (DKM/DLKM)': 15, 'Institutional Change': 16, 
    'Short Cycle Diploma': 17, 'International Change': 18
}

course_map = {
    'Biofuel Prod': 1, 'Animation Design': 2, 'Social Service (Eve)': 3, 'Agronomy': 4, 
    'Comm Design': 5, 'Vet Nursing': 6, 'Informatics Eng': 7, 'Equiniculture': 8, 
    'Management': 9, 'Social Service': 10, 'Tourism': 11, 'Nursing': 12, 'Oral Hygiene': 13, 
    'Advertising': 14, 'Journalism': 15, 'Basic Ed': 16, 'Management (Eve)': 17
}

prev_qual_map = {
    'Secondary Ed': 1, "Bachelor's": 2, 'Higher Ed Degree': 3, "Master's": 4, 'Doctorate': 5, 
    'Partial Higher Ed': 6, 'Inc 12th Year': 7, 'Inc 11th Year': 8, '11th Year (Other)': 9, 
    '10th Year': 10, 'Inc 10th Year': 11, 'Basic Ed (3rd Cycle)': 12, 'Basic Ed (2nd Cycle)': 13, 
    'Tech Specialization': 14, '1st Cycle Degree': 15, 'Prof Tech Course': 16, "2nd Cycle Master's": 17
}

fathers_qualification_map = {
    'Secondary Ed': 1, "Bachelor's": 2, 'Higher Ed Degree': 3, "Master's": 4, 'Doctorate': 5, 
    'Partial Higher Ed': 6, 'Inc 12th Year': 7, 'Inc 11th Year': 8, '7th Year (Old)': 9, 
    '11th Year (Other)': 10, 'Comp High School': 11, '10th Year': 12, 'Commerce Course': 13, 
    'Basic Ed (3rd Cycle)': 14, 'Tech-Prof Course': 16, 'Inc Comp High School': 17, '7th Year': 18, 
    'Gen High School': 19, 'Inc 9th Year': 20, '8th Year': 21, 'Admin/Commerce': 22, 'Accounting/Admin': 23, 
    'Unknown': 24, 'No Literacy': 25, 'Basic Literacy': 26, 'Basic Ed (1st Cycle)': 27, 
    'Basic Ed (2nd Cycle)': 28, 'Tech Specialization': 29, '1st Cycle Degree': 30, 'Specialized Higher Ed': 31, 
    'Prof Tech Course': 32, "2nd Cycle Master's": 33, '3rd Cycle Doctorate': 34
}

fathers_occupation_map = {
    'Student': 1, 'Legislators & Execs': 2, 'Intellectual/Sci Specialists': 3, 'Mid-Level Techs': 4, 
    'Admin Staff': 5, 'Service & Sales Workers': 6, 'Agri & Forestry Workers': 7, 'Skilled Industry Workers': 8, 
    'Machine Ops & Assemblers': 9, 'Unskilled Workers': 10, 'Armed Forces': 11, 'Other Situation': 12, 
    'Unknown/Blank': 13, 'Military Officers': 14, 'Military Sergeants': 15, 'Other Military': 16, 
    'Admin/Comm Directors': 17, 'Hospitality/Trade Directors': 18, 'STEM Specialists': 19, 'Health Professionals': 20, 
    'Teachers': 21, 'Finance/Admin Specialists': 22, 'Mid-Level STEM Techs': 23, 'Mid-Level Health Techs': 24, 
    'Mid-Level Legal/Social Techs': 25, 'ICT Technicians': 26, 'Office & Data Workers': 27, 'Finance/Data Operators': 28, 
    'Other Admin Support': 29, 'Personal Service Workers': 30, 'Sales Workers': 31, 'Personal Care Workers': 32, 
    'Security Personnel': 33, 'Skilled Agri Workers': 34, 'Subsistence Agri Workers': 35, 'Skilled Construction': 36, 
    'Metallurgy Workers': 37, 'Electrical Workers': 38, 'Manufacturing/Crafts': 39, 'Plant/Machine Operators': 40, 
    'Assembly Workers': 41, 'Drivers & Operators': 42, 'Unskilled Agri': 43, 'Unskilled Ind/Const': 44, 
    'Meal Prep Assistants': 45, 'Street Vendors': 46
}

yes_no_map = {"No": 0, "Yes": 1}
attendance_map = {"Daytime": 1, "Evening": 0}
gender_map = {"Female": 0, "Male": 1}

# Input Form
with st.form("student_data_form"):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.subheader("Personal & Academic")[cite: 1]
        student_id = st.text_input("Student ID", placeholder="e.g., STU-12345")
        m_status = st.selectbox("Marital Status", list(marital_map.keys()))[cite: 1]
        st.subheader("Personal & Academic")
        m_status = st.selectbox("Marital Status", list(marital_map.keys()))
        app_mode = st.selectbox("Application Mode", list(app_mode_map.keys()))
        course = st.selectbox("Course", list(course_map.keys()))
        attendance = st.selectbox("Attendance (Mode of Study)", list(attendance_map.keys()))
        gender = st.selectbox("Gender", list(gender_map.keys()))
        age = st.number_input("Age at Enrollment", 17, 70, 22)
        
    with c2:
        st.subheader("Family Background")
        prev_qual = st.selectbox("Student's Previous Educational Qualification", list(prev_qual_map.keys()))
        father_qual = st.selectbox("Father's Educational Qualification", list(fathers_qualification_map.keys()))
        father_occ = st.selectbox("Father's Occupation", list(fathers_occupation_map.keys()))
        displaced = st.selectbox("Displaced? (Referring to Residential Status)", list(yes_no_map.keys()))
        
    with c3:
        st.subheader("Financial & Units")
        debtor = st.selectbox("In Debt?", list(yes_no_map.keys()))
        tuition = st.selectbox("Tuition Up to Date?", list(yes_no_map.keys()))
        scholarship = st.selectbox("Scholarship Holder?", list(yes_no_map.keys()))
        grade_1 = st.number_input("1st Semester Grade", 0.0, 20.0, 0.0)
        grade_2 = st.number_input("2nd Semester Grade", 0.0, 20.0, 0.0)
        approved_1 = st.number_input("1st Semester Approved Units", 0, 20, 0)
        approved_2 = st.number_input("2nd Semester Approved Units", 0, 20, 0)

        st.markdown("---")
        st.subheader("Macroeconomics")
        unemployment = st.number_input("Unemployment Rate", -10.0, 30.0, 10.8)
        inflation = st.number_input("Inflation Rate", -10.0, 20.0, 1.4)
        gdp = st.number_input("GDP", -10.0, 10.0, 1.74)

    submit_button = st.form_submit_button("🚀 Predict Outcome")

# Prediction logic
if submit_button:
    # Conditional logic based on selection
    non_trad = 1 if age >= 25 else 0
    father_higher = 1 if fathers_qualification_map[father_qual] >= 3 else 0 # Example assumption

    payload = {
        "Student_ID": student_id,
        "Marital status": marital_map[m_status],
        "Application mode": app_mode_map[app_mode],
        "Course": course_map[course],
        "Daytime/evening attendance": attendance_map[attendance], 
        "Previous qualification": prev_qual_map[prev_qual],
        "Father's qualification": fathers_qualification_map[father_qual], 
        "Father's occupation": fathers_occupation_map[father_occ],
        "Displaced": yes_no_map[displaced], 
        "Debtor": yes_no_map[debtor], 
        "Tuition fees up to date": yes_no_map[tuition],
        "Gender": gender_map[gender], 
        "Scholarship holder": yes_no_map[scholarship],
        "Curricular units 1st sem (grade)": grade_1, 
        "Curricular units 2nd sem (grade)": grade_2,
        "Curricular units 1st sem (approved)": approved_1, 
        "Curricular units 2nd sem (approved)": approved_2,
        "Age at enrollment": age,
        "Unemployment rate": unemployment,
        "Inflation rate": inflation,
        "GDP": gdp,
        "Grade_Change": grade_2 - grade_1,
        "Total_Approved_Units": approved_1 + approved_2,
        "Approved_Units_Change": approved_2 - approved_1,
        "Academic_Efficiency": (grade_1 + grade_2) / ((approved_1 + approved_2) + 1e-5),
        "Financial_Risk_Score": yes_no_map[debtor] + (1 - yes_no_map[tuition]) - yes_no_map[scholarship],
        "Non_Traditional_Student": non_trad,
        "Father_Higher_Ed": father_higher
    }
    
    try:
        res = requests.post("https://student-attrition-api.onrender.com/predict", json=payload)
        if res.status_code == 200:
            result = res.json()
            st.success(f"Result: {result['prediction']}")
            st.metric("Confidence", f"{result['confidence_percent']}%")
            
            display_payload = payload.copy()
            
            # Reverse mappings for binary/categorical fields
            rev_yes_no = {1: "Yes", 0: "No"}
            rev_gender = {0: "Female", 1: "Male"}
            rev_attendance = {1: "Daytime", 0: "Evening"}
            rev_marital = {v: k for k, v in marital_map.items()}
            rev_app_mode = {v: k for k, v in app_mode_map.items()}
            rev_course = {v: k for k, v in course_map.items()}
            rev_prev_qual = {v: k for k, v in prev_qual_map.items()}
            rev_father_qual = {v: k for k, v in fathers_qualification_map.items()}
            rev_father_occ = {v: k for k, v in fathers_occupation_map.items()}
            
            # Convert the appropriate fields
            display_payload["Displaced"] = rev_yes_no[display_payload["Displaced"]]
            display_payload["Debtor"] = rev_yes_no[display_payload["Debtor"]]
            display_payload["Tuition fees up to date"] = rev_yes_no[display_payload["Tuition fees up to date"]]
            display_payload["Scholarship holder"] = rev_yes_no[display_payload["Scholarship holder"]]
            display_payload["Gender"] = rev_gender[display_payload["Gender"]]
            display_payload["Daytime/evening attendance"] = rev_attendance[display_payload["Daytime/evening attendance"]]
            display_payload["Non_Traditional_Student"] = rev_yes_no[display_payload["Non_Traditional_Student"]]
            display_payload["Father_Higher_Ed"] = rev_yes_no[display_payload["Father_Higher_Ed"]]
            
            # Convert categorical fields
            display_payload["Marital status"] = rev_marital[display_payload["Marital status"]]
            display_payload["Application mode"] = rev_app_mode[display_payload["Application mode"]]
            display_payload["Course"] = rev_course[display_payload["Course"]]
            display_payload["Previous qualification"] = rev_prev_qual[display_payload["Previous qualification"]]
            display_payload["Father's qualification"] = rev_father_qual[display_payload["Father's qualification"]]
            display_payload["Father's occupation"] = rev_father_occ[display_payload["Father's occupation"]]

            display_df = pd.DataFrame([display_payload]).T.rename(columns={0: "Value"})
            display_df.index = [idx.replace('_', ' ') for idx in display_df.index]
            st.dataframe(display_df, use_container_width=True)
            
            prob_data = pd.DataFrame({
                "Status": ["Dropout", "Enrolled", "Graduate"],
                "Probability": [result['agent_context']['dropout_risk'], result['agent_context']['enrolled_prob'], result['agent_context']['graduate_prob']]
            })
            st.plotly_chart(px.pie(prob_data, values="Probability", names="Status", hole=0.4))
        else:
            st.error("API Error: Check if FastAPI is running!")
    except Exception as e:
        st.error(f"Could not connect: {e}")
