import streamlit as st
import joblib
import numpy as np

model = joblib.load("strength_model.pkl")

st.title("AI Structural Health Assessment System")

upv = st.number_input(
    "UPV (km/s)",
    min_value=2.0,
    max_value=6.0,
    value=4.0)

rebound = st.number_input(
    "Rebound Number",
    min_value=10.0,
    max_value=60.0,
    value=30.0)

rca = st.selectbox(
    "RCA Percentage",
    [0,10,20,30])

if st.button("Predict"):

    strength = model.predict(
        [[upv,rebound,rca]])[0]

    if strength < 30:
        grade = "M20"
    elif strength < 40:
        grade = "M30"
    else:
        grade = "M40"

    if upv > 4.5:
        quality = "Excellent"
    elif upv > 3.5:
        quality = "Good"
    else:
        quality = "Fair"

    design_strength = float(
        grade.replace("M",""))

    shi = (
        strength/design_strength
    )*100

    if shi > 90:
        status = "HEALTHY"
    elif shi > 75:
        status = "MODERATE"
    elif shi > 50:
        status = "WARNING"
    else:
        status = "CRITICAL"

    st.success(
        f"Predicted Strength = {strength:.2f} MPa")

    st.write("Concrete Grade:",grade)
    st.write("Quality:",quality)
    st.write("Structural Health Index:",f"{shi:.2f}%")
    st.write("Status:",status)