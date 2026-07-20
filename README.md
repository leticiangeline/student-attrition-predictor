# 🎓 Student Retention Classifier

## Overview
The **Student Retention Classifier** is a full-stack machine learning web application designed to predict university student outcomes. By analyzing a student's personal background, academic performance, financial standing, and current macroeconomic factors, the system classifies the student into one of three categories: **Dropout**, **Enrolled**, or **Graduate**. 

The application pairs a fast, responsive API with an interactive frontend to deliver real-time risk assessments, confidence metrics, and dynamically generated AI counselor interventions.

---

## 🛠 Tech Stack
*   **Frontend Interface:** Streamlit (with Plotly Express for data visualization).
*   **Backend API:** FastAPI (using Pydantic for data validation).
*   **Machine Learning Engine:** Scikit-Learn (`RandomForestClassifier`), Pandas, NumPy, and Joblib.
*   **AI Integration:** n8n Webhook architecture triggering Gemini API for personalized counselor recommendations.

---

## ✨ Core Features
*   **Comprehensive Assessment Form:** Collects detailed student metrics categorized into Personal & Academic, Family Background, Financial & Units, and Macroeconomics (GDP, Inflation, Unemployment).
*   **Automated Feature Engineering:** The frontend automatically calculates complex metrics before prediction, including `Academic_Efficiency`, `Financial_Risk_Score`, `Grade_Change`, and custom flags for non-traditional students.
*   **Real-Time Model Inference:** A serialized Scikit-Learn Random Forest model evaluates the structured payload to return the predicted outcome and exact probability distributions for all three potential statuses.
*   **AI Counselor Suggestions:** Upon receiving a prediction, the app hits an n8n webhook with the student's risk profile to generate actionable, dynamic intervention advice (e.g., "⚠️ Urgent Intervention Required" for dropouts).
*   **Visual Data Summary:** Generates an interactive pie chart representing the specific dropout, enrollment, and graduation probabilities, alongside a clean tabular breakdown of the user's input.

---

## 📂 Project Structure (Inferred)

```text
├── app.py                            # Streamlit frontend application
├── api.py                            # FastAPI backend server
├── student_retention_model.joblib    # Trained Scikit-Learn Random Forest model
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
