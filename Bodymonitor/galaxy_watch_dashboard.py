import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Performance System")

# ===============================
# FILE UPLOADER (Works in Cloud)
# ===============================

uploaded_files = st.file_uploader(
    "Upload Galaxy Watch CSV Files",
    type="csv",
    accept_multiple_files=True
)

if not uploaded_files:
    st.warning("Upload your CSV files to continue.")
    st.stop()

# ===============================
# LOAD DATA
# ===============================

data = {}

for file in uploaded_files:
    name = file.name.replace(".csv", "").lower()
    df = pd.read_csv(file)

    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    data[name] = df

# ===============================
# ROLE SELECTOR
# ===============================

role = st.sidebar.selectbox(
    "Select Dashboard Role",
    ["Coach", "Trainer", "Team Doctor", "Athlete"]
)

st.sidebar.markdown("---")

# ===============================
# HELPER FUNCTIONS
# ===============================

def show_line_chart(df, x, y, title):
    if x in df.columns and y in df.columns:
        fig = px.line(df, x=x, y=y, title=title)
        st.plotly_chart(fig, use_container_width=True)

def show_bar_chart(df, x, y, title):
    if x in df.columns and y in df.columns:
        fig = px.bar(df, x=x, y=y, title=title)
        st.plotly_chart(fig, use_container_width=True)

def show_metric(label, value):
    st.metric(label, round(float(value), 2))

# ===============================
# COACH DASHBOARD
# ===============================

if role == "Coach":
    st.header("Coach Dashboard – Performance")

    if "steps" in data and "steps" in data["steps"].columns:
        show_metric("Total Steps", data["steps"]["steps"].sum())
        show_line_chart(data["steps"], "datetime", "steps", "Steps Over Time")

    if "active_minutes" in data and "active_minutes" in data["active_minutes"].columns:
        show_metric("Active Minutes", data["active_minutes"]["active_minutes"].sum())
        show_line_chart(data["active_minutes"], "datetime", "active_minutes", "Active Minutes")

    if "heart_rate" in data and "heart_rate" in data["heart_rate"].columns:
        show_line_chart(data["heart_rate"], "datetime", "heart_rate", "Heart Rate Trend")

    if "sleep" in data and "total_sleep_minutes" in data["sleep"].columns:
        show_bar_chart(data["sleep"], "datetime", "total_sleep_minutes", "Sleep Duration")

    if "energy_score" in data and "energy_score" in data["energy_score"].columns:
        show_line_chart(data["energy_score"], "datetime", "energy_score", "Energy Score")

# ===============================
# TRAINER DASHBOARD
# ===============================

elif role == "Trainer":
    st.header("Trainer Dashboard – Conditioning")

    if "body_composition" in data:
        if "body_fat_percent" in data["body_composition"].columns:
            show_line_chart(data["body_composition"], "datetime", "body_fat_percent", "Body Fat %")
        if "muscle_mass" in data["body_composition"].columns:
            show_line_chart(data["body_composition"], "datetime", "muscle_mass", "Muscle Mass")

    if "calories" in data and "calories" in data["calories"].columns:
        show_line_chart(data["calories"], "datetime", "calories", "Calories Burned")

    if "stress" in data and "stress_level" in data["stress"].columns:
        show_line_chart(data["stress"], "datetime", "stress_level", "Stress Levels")

    if "sleep" in data:
        if "deep_sleep" in data["sleep"].columns:
            show_line_chart(data["sleep"], "datetime", "deep_sleep", "Deep Sleep")
        if "rem_sleep" in data["sleep"].columns:
            show_line_chart(data["sleep"], "datetime", "rem_sleep", "REM Sleep")

# ===============================
# TEAM DOCTOR DASHBOARD
# ===============================

elif role == "Team Doctor":
    st.header("Team Doctor Dashboard – Clinical Monitoring")

    if "ecg" in data and "ecg_signal" in data["ecg"].columns:
        show_line_chart(data["ecg"], "datetime", "ecg_signal", "ECG Signal")

    if "blood_pressure" in data:
        if "systolic" in data["blood_pressure"].columns:
            show_line_chart(data["blood_pressure"], "datetime", "systolic", "Systolic BP")
        if "diastolic" in data["blood_pressure"].columns:
            show_line_chart(data["blood_pressure"], "datetime", "diastolic", "Diastolic BP")

    if "spo2" in data and "spo2" in data["spo2"].columns:
        show_line_chart(data["spo2"], "datetime", "spo2", "Blood Oxygen (SpO2)")

    if "sleep_apnea" in data and "apnea_events" in data["sleep_apnea"].columns:
        show_bar_chart(data["sleep_apnea"], "datetime", "apnea_events", "Sleep Apnea Events")

    if "fall_detection" in data and "fall_detected" in data["fall_detection"].columns:
        show_bar_chart(data["fall_detection"], "datetime", "fall_detected", "Fall Events")

    if "menstrual_cycle" in data and "cycle_day" in data["menstrual_cycle"].columns:
        show_line_chart(data["menstrual_cycle"], "datetime", "cycle_day", "Menstrual Cycle")

    if "antioxidant_index" in data and "carotenoids" in data["antioxidant_index"].columns:
        show_line_chart(data["antioxidant_index"], "datetime", "carotenoids", "Antioxidant Index")

# ===============================
# ATHLETE DASHBOARD
# ===============================

elif role == "Athlete":
    st.header("Athlete Dashboard – Daily Overview")

    col1, col2, col3 = st.columns(3)

    if "steps" in data and "steps" in data["steps"].columns:
        with col1:
            show_metric("Steps", data["steps"]["steps"].sum())

    if "calories" in data and "calories" in data["calories"].columns:
        with col2:
            show_metric("Calories", data["calories"]["calories"].sum())

    if "active_minutes" in data and "active_minutes" in data["active_minutes"].columns:
        with col3:
            show_metric("Active Minutes", data["active_minutes"]["active_minutes"].sum())

    if "sleep" in data and "total_sleep_minutes" in data["sleep"].columns:
        show_bar_chart(data["sleep"], "datetime", "total_sleep_minutes", "Sleep Summary")

    if "stress" in data and "stress_level" in data["stress"].columns:
        show_line_chart(data["stress"], "datetime", "stress_level", "Stress Trend")

    if "energy_score" in data and "energy_score" in data["energy_score"].columns:
        show_line_chart(data["energy_score"], "datetime", "energy_score", "Energy Score")

st.success("Dashboard Loaded Successfully")
