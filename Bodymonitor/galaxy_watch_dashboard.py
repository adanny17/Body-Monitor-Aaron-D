import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Performance System (Demo Mode)")

# ===============================
# GENERATE RANDOM DATA
# ===============================

np.random.seed(42)
dates = pd.date_range(end=pd.Timestamp.today(), periods=30)

data = {}

data["steps"] = pd.DataFrame({
    "datetime": dates,
    "steps": np.random.randint(4000, 15000, 30)
})

data["active_minutes"] = pd.DataFrame({
    "datetime": dates,
    "active_minutes": np.random.randint(30, 120, 30)
})

data["calories"] = pd.DataFrame({
    "datetime": dates,
    "calories": np.random.randint(1800, 3500, 30)
})

data["heart_rate"] = pd.DataFrame({
    "datetime": dates,
    "heart_rate": np.random.randint(55, 180, 30)
})

data["sleep"] = pd.DataFrame({
    "datetime": dates,
    "total_sleep_minutes": np.random.randint(300, 540, 30),
    "deep_sleep": np.random.randint(60, 120, 30),
    "rem_sleep": np.random.randint(60, 120, 30)
})

data["energy_score"] = pd.DataFrame({
    "datetime": dates,
    "energy_score": np.random.randint(40, 100, 30)
})

data["stress"] = pd.DataFrame({
    "datetime": dates,
    "stress_level": np.random.randint(10, 90, 30)
})

data["body_composition"] = pd.DataFrame({
    "datetime": dates,
    "body_fat_percent": np.random.uniform(10, 25, 30),
    "muscle_mass": np.random.uniform(60, 90, 30)
})

data["ecg"] = pd.DataFrame({
    "datetime": dates,
    "ecg_signal": np.random.normal(0, 1, 30)
})

data["blood_pressure"] = pd.DataFrame({
    "datetime": dates,
    "systolic": np.random.randint(105, 140, 30),
    "diastolic": np.random.randint(65, 90, 30)
})

data["spo2"] = pd.DataFrame({
    "datetime": dates,
    "spo2": np.random.randint(94, 100, 30)
})

data["sleep_apnea"] = pd.DataFrame({
    "datetime": dates,
    "apnea_events": np.random.randint(0, 10, 30)
})

data["fall_detection"] = pd.DataFrame({
    "datetime": dates,
    "fall_detected": np.random.randint(0, 2, 30)
})

data["menstrual_cycle"] = pd.DataFrame({
    "datetime": dates,
    "cycle_day": np.random.randint(1, 28, 30)
})

data["antioxidant_index"] = pd.DataFrame({
    "datetime": dates,
    "carotenoids": np.random.uniform(2.0, 6.0, 30)
})

# ===============================
# ROLE SELECTOR
# ===============================

role = st.sidebar.selectbox(
    "Select Dashboard Role",
    ["Coach", "Trainer", "Team Doctor", "Athlete"]
)

# ===============================
# HELPER FUNCTIONS
# ===============================

def show_line_chart(df, y, title):
    fig = px.line(df, x="datetime", y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)

def show_bar_chart(df, y, title):
    fig = px.bar(df, x="datetime", y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)

def show_metric(label, value):
    st.metric(label, round(float(value), 2))

# ===============================
# COACH DASHBOARD
# ===============================

if role == "Coach":
    st.header("Coach Dashboard – Performance")

    show_metric("Total Steps", data["steps"]["steps"].sum())
    show_line_chart(data["steps"], "steps", "Steps Over Time")

    show_metric("Active Minutes", data["active_minutes"]["active_minutes"].sum())
    show_line_chart(data["active_minutes"], "active_minutes", "Active Minutes")

    show_line_chart(data["heart_rate"], "heart_rate", "Heart Rate Trend")
    show_bar_chart(data["sleep"], "total_sleep_minutes", "Sleep Duration")
    show_line_chart(data["energy_score"], "energy_score", "Energy Score")

# ===============================
# TRAINER DASHBOARD
# ===============================

elif role == "Trainer":
    st.header("Trainer Dashboard – Conditioning")

    show_line_chart(data["body_composition"], "body_fat_percent", "Body Fat %")
    show_line_chart(data["body_composition"], "muscle_mass", "Muscle Mass")
    show_line_chart(data["calories"], "calories", "Calories Burned")
    show_line_chart(data["stress"], "stress_level", "Stress Levels")
    show_line_chart(data["sleep"], "deep_sleep", "Deep Sleep")
    show_line_chart(data["sleep"], "rem_sleep", "REM Sleep")

# ===============================
# TEAM DOCTOR DASHBOARD
# ===============================

elif role == "Team Doctor":
    st.header("Team Doctor Dashboard – Clinical Monitoring")

    show_line_chart(data["ecg"], "ecg_signal", "ECG Signal")
    show_line_chart(data["blood_pressure"], "systolic", "Systolic BP")
    show_line_chart(data["blood_pressure"], "diastolic", "Diastolic BP")
    show_line_chart(data["spo2"], "spo2", "Blood Oxygen (SpO2)")
    show_bar_chart(data["sleep_apnea"], "apnea_events", "Sleep Apnea Events")
    show_bar_chart(data["fall_detection"], "fall_detected", "Fall Events")
    show_line_chart(data["menstrual_cycle"], "cycle_day", "Menstrual Cycle")
    show_line_chart(data["antioxidant_index"], "carotenoids", "Antioxidant Index")

# ===============================
# ATHLETE DASHBOARD
# ===============================

elif role == "Athlete":
    st.header("Athlete Dashboard – Daily Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric("Steps", data["steps"]["steps"].sum())

    with col2:
        show_metric("Calories", data["calories"]["calories"].sum())

    with col3:
        show_metric("Active Minutes", data["active_minutes"]["active_minutes"].sum())

    show_bar_chart(data["sleep"], "total_sleep_minutes", "Sleep Summary")
    show_line_chart(data["stress"], "stress_level", "Stress Trend")
    show_line_chart(data["energy_score"], "energy_score", "Energy Score")

st.success("Demo Dashboard Loaded Successfully")

