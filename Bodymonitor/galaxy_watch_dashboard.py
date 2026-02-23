import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Performance Dashboard")

# =====================================
# FILE UPLOAD SECTION
# =====================================

st.sidebar.header("Upload Galaxy Watch CSV Files")

def load_csv(label):
    file = st.sidebar.file_uploader(label, type="csv")
    if file:
        df = pd.read_csv(file)
        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])
        return df
    return None

data = {
    "steps": load_csv("Upload Steps CSV"),
    "active_minutes": load_csv("Upload Active Minutes CSV"),
    "calories": load_csv("Upload Calories CSV"),
    "heart_rate": load_csv("Upload Heart Rate CSV"),
    "sleep": load_csv("Upload Sleep CSV"),
    "ecg": load_csv("Upload ECG CSV"),
    "spo2": load_csv("Upload SpO2 CSV"),
    "blood_pressure": load_csv("Upload Blood Pressure CSV"),
    "stress": load_csv("Upload Stress CSV"),
    "body_composition": load_csv("Upload Body Composition CSV"),
    "sleep_apnea": load_csv("Upload Sleep Apnea CSV"),
    "fall_detection": load_csv("Upload Fall Detection CSV"),
    "menstrual_cycle": load_csv("Upload Menstrual Cycle CSV"),
    "energy_score": load_csv("Upload Energy Score CSV"),
    "antioxidant_index": load_csv("Upload Antioxidant Index CSV"),
}

# =====================================
# ROLE SELECTOR
# =====================================

role = st.sidebar.selectbox(
    "Select Dashboard Role",
    ["Coach", "Trainer", "Team Doctor", "Athlete"]
)

# =====================================
# HELPER FUNCTIONS
# =====================================

def show_line(df, column, title):
    if df is not None and column in df.columns:
        fig = px.line(df, x="datetime", y=column, title=title, markers=True)
        st.plotly_chart(fig, use_container_width=True)

def show_bar(df, column, title):
    if df is not None and column in df.columns:
        fig = px.bar(df, x="datetime", y=column, title=title)
        st.plotly_chart(fig, use_container_width=True)

def show_metric(df, column, label):
    if df is not None and column in df.columns:
        st.metric(label, round(df[column].sum(), 2))

def show_area_sleep(df):
    if df is not None and "deep_sleep" in df.columns and "rem_sleep" in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["datetime"],
            y=df["deep_sleep"],
            fill='tozeroy',
            mode='none',
            name="Deep Sleep"
        ))
        fig.add_trace(go.Scatter(
            x=df["datetime"],
            y=df["rem_sleep"],
            fill='tozeroy',
            mode='none',
            name="REM Sleep"
        ))
        fig.update_layout(title="Sleep Stages")
        st.plotly_chart(fig, use_container_width=True)

# =====================================
# DASHBOARDS
# =====================================

if role == "Coach":
    st.header("Coach Dashboard – Performance Overview")

    show_metric(data["steps"], "steps", "Total Steps")
    show_line(data["steps"], "steps", "Steps Over Time")
    show_line(data["heart_rate"], "heart_rate", "Heart Rate Trend")
    show_line(data["energy_score"], "energy_score", "Energy Score")
    show_area_sleep(data["sleep"])

elif role == "Trainer":
    st.header("Trainer Dashboard – Conditioning & Body Metrics")

    show_line(data["body_composition"], "body_fat_percent", "Body Fat %")
    show_line(data["body_composition"], "muscle_mass", "Muscle Mass")
    show_bar(data["calories"], "calories", "Calories Burned")
    show_line(data["stress"], "stress_level", "Stress Levels")
    show_area_sleep(data["sleep"])

elif role == "Team Doctor":
    st.header("Team Doctor Dashboard – Clinical Metrics")

    show_line(data["ecg"], "ecg_signal", "ECG Signal")
    show_line(data["blood_pressure"], "systolic", "Systolic Blood Pressure")
    show_line(data["blood_pressure"], "diastolic", "Diastolic Blood Pressure")
    show_line(data["spo2"], "spo2", "Blood Oxygen (SpO2)")
    show_bar(data["sleep_apnea"], "apnea_events", "Sleep Apnea Events")
    show_bar(data["fall_detection"], "fall_detected", "Fall Detection Events")
    show_line(data["menstrual_cycle"], "cycle_day", "Menstrual Cycle")
    show_line(data["antioxidant_index"], "carotenoids", "Antioxidant Index")

elif role == "Athlete":
    st.header("Athlete Dashboard – Daily Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric(data["steps"], "steps", "Total Steps")
    with col2:
        show_metric(data["calories"], "calories", "Total Calories")
    with col3:
        show_metric(data["active_minutes"], "active_minutes", "Active Minutes")

    show_bar(data["sleep"], "total_sleep_minutes", "Total Sleep")
    show_line(data["stress"], "stress_level", "Stress Trend")
    show_line(data["energy_score"], "energy_score", "Energy Score")

st.success("Upload CSV files in the sidebar to populate dashboard.")

