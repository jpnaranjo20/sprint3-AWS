import streamlit as st
import requests

st.title("Prediction Form")

gender = st.selectbox(
    "Gender:",
    ["Female", "Male", "Other"]
)

age = st.number_input(
    "Age:",
    min_value=0,
    max_value=120,
    step=1
)

hypertension = st.selectbox(
    "Hypertension:",
    ["Yes", "No"]
)
hypertension = 1 if hypertension == "Yes" else 0

heart_disease = st.selectbox(
    "Heart Disease:",
    ["Yes", "No"]
)
heart_disease = 1 if heart_disease == "Yes" else 0

smoking_history = st.selectbox(
    "Smoking History:",
    ["never", "current", "former", "ever", "not current"]
)

bmi = st.number_input(
    "BMI:",
    step=0.01
)

hba1c_level = st.number_input(
    "HbA1c Level:",
    step=0.01
)

blood_glucose_level = st.number_input(
    "Blood Glucose Level:"
)

if st.button("Submit"):
    form_data = {
        "gender": gender,
        "age": age,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_history": smoking_history,
        "bmi": bmi,
        "HbA1c_level": hba1c_level,
        "blood_glucose_level": blood_glucose_level,
    }

    response = requests.post("http://ml_app:8000/predict", json=form_data)

    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"Prediction: {prediction}")
    else:
        st.error(f"Error: {response.json()}")
