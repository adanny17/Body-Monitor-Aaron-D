# galaxy_watch_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Performance System")

# ===============================
# DATA LOADING
# ===============================

@st.cache_data
def load_data(folder_path):
    dataframes = {}
    
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(folder_path, file))
            
            # Standardize datetime if exists
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            
            dataframes[name] = df
    
    return dataframes


folder = st.text_input("Enter folder path of Galaxy Watch CSV files:")

if folder and os.path.exists(folder):
    data = load_data(folder)
else:
    st.warning("Enter a valid folder path.")
    st.stop()

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
    st.metric(label, f"{round(value,2)}")

# ===============================
# COACH DASHBOARD
# ===============================

if role == "Coach":
    st.header("Coach Dashboard – Performance & Readiness")

    if "steps" in data:
        total_steps = data["steps"]["steps"].sum()
        show_metric("Total Steps", total_steps)
        show_line_chart(data["steps"], "datetime", "steps", "Steps Over Time")

    if "active_minutes" in data:
        show_metric("Total Active Minutes", data["active_minutes"]["active_minutes"].sum())
        show_line_chart(data["active_minutes"], "datetime", "active_minutes", "Active Minutes")

    if "heart_rate" in data:
        show_line_chart(data["heart_rate"], "datetime", "heart_rate", "Heart Rate Trend")

    if "sleep" in data:
        show_bar_chart(data["sleep"], "datetime", "total_sleep_minutes", "Sleep Duration")

    if "energy_score" in data:
        show_line_chart(data["energy_score"], "datetime", "energy_score", "Energy Score")

# ===============================
# TRAINER DASHBOARD
# ===============================

elif role == "Trainer":
    st.header("Trainer Dashboard – Conditioning & Recovery")

    if "body_composition" in data:
        show_line_chart(data["body_composition"], "datetime", "body_fat_percent", "Body Fat %")
        show_line_chart(data["body_composition"], "datetime", "muscle_mass", "Muscle Mass")

    if "calories" in data:
        show_line_chart(data["calories"], "datetime", "calories", "Calories Burned")

    if "stress" in data:
        show_line_chart(data["stress"], "datetime", "stress_level", "Stress Levels")

    if "sleep" in data:
        show_line_chart(data["sleep"], "datetime", "deep_sleep", "Deep Sleep")
        show_line_chart(data["sleep"], "datetime", "rem_sleep", "REM Sleep")

# ===============================
# TEAM DOCTOR DASHBOARD
# ===============================

elif role == "Team Doctor":
    st.header("Team Doctor Dashboard – Clinical Monitoring")

    if "ecg" in data:
        show_line_chart(data["ecg"], "datetime", "ecg_signal", "ECG Signal")

    if "blood_pressure" in data:
        show_line_chart(data["blood_pressure"], "datetime", "systolic", "Systolic BP")
        show_line_chart(data["blood_pressure"], "datetime", "diastolic", "Diastolic BP")

    if "spo2" in data:
        show_line_chart(data["spo2"], "datetime", "spo2", "Blood Oxygen (SpO2)")

    if "sleep_apnea" in data:
        show_bar_chart(data["sleep_apnea"], "datetime", "apnea_events", "Sleep Apnea Events")

    if "fall_detection" in data:
        show_bar_chart(data["fall_detection"], "datetime", "fall_detected", "Fall Events")

    if "menstrual_cycle" in data:
        show_line_chart(data["menstrual_cycle"], "datetime", "cycle_day", "Menstrual Cycle Tracking")

    if "antioxidant_index" in data:
        show_line_chart(data["antioxidant_index"], "datetime", "carotenoids", "Antioxidant Index")

# ===============================
# ATHLETE DASHBOARD
# ===============================

elif role == "Athlete":
    st.header("Athlete Dashboard – Daily Overview")

    col1, col2, col3 = st.columns(3)

    if "steps" in data:
        with col1:
            show_metric("Steps", data["steps"]["steps"].sum())

    if "calories" in data:
        with col2:
            show_metric("Calories", data["calories"]["calories"].sum())

    if "active_minutes" in data:
        with col3:
            show_metric("Active Minutes", data["active_minutes"]["active_minutes"].sum())

    if "sleep" in data:
        show_bar_chart(data["sleep"], "datetime", "total_sleep_minutes", "Sleep Summary")

    if "stress" in data:
        show_line_chart(data["stress"], "datetime", "stress_level", "Stress Trend")

    if "energy_score" in data:
        show_line_chart(data["energy_score"], "datetime", "energy_score", "Energy Score")

st.success("Dashboard Loaded Successfully")
