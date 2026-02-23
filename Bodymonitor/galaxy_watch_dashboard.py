import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Unified Dashboard")

# =========================================
# SINGLE CSV UPLOAD
# =========================================

st.sidebar.header("Upload Galaxy Watch Master CSV")

uploaded_file = st.sidebar.file_uploader("Upload Master CSV", type="csv")

if uploaded_file is None:
    st.warning("Please upload your Galaxy Watch CSV file.")
    st.stop()

df = pd.read_csv(uploaded_file)

if "datetime" not in df.columns:
    st.error("CSV must contain a 'datetime' column.")
    st.stop()

df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

# =========================================
# ROLE SELECTOR
# =========================================

role = st.sidebar.selectbox(
    "Select Dashboard Role",
    ["Coach", "Trainer", "Team Doctor", "Athlete"]
)

# =========================================
# HELPER FUNCTIONS
# =========================================

def show_line(column, title):
    if column in df.columns:
        fig = px.line(df, x="datetime", y=column, title=title, markers=True)
        st.plotly_chart(fig, use_container_width=True)

def show_bar(column, title):
    if column in df.columns:
        fig = px.bar(df, x="datetime", y=column, title=title)
        st.plotly_chart(fig, use_container_width=True)

def show_metric(column, label):
    if column in df.columns:
        st.metric(label, round(df[column].sum(), 2))

def show_latest_metric(column, label):
    if column in df.columns:
        st.metric(label, round(df[column].iloc[-1], 2))

def show_sleep_area():
    if "deep_sleep" in df.columns and "rem_sleep" in df.columns:
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

# =========================================
# DASHBOARDS
# =========================================

if role == "Coach":
    st.header("Coach Dashboard – Performance Overview")

    show_metric("steps", "Total Steps")
    show_line("steps", "Steps Over Time")
    show_line("heart_rate", "Heart Rate Trend")
    show_line("energy_score", "Energy Score")
    show_sleep_area()

elif role == "Trainer":
    st.header("Trainer Dashboard – Conditioning & Body Metrics")

    show_line("body_fat_percent", "Body Fat %")
    show_line("muscle_mass", "Muscle Mass")
    show_bar("calories", "Calories Burned")
    show_line("stress_level", "Stress Levels")
    show_sleep_area()

elif role == "Team Doctor":
    st.header("Team Doctor Dashboard – Clinical Metrics")

    show_line("ecg_signal", "ECG Signal")
    show_line("systolic", "Systolic Blood Pressure")
    show_line("diastolic", "Diastolic Blood Pressure")
    show_line("spo2", "Blood Oxygen (SpO2)")
    show_bar("apnea_events", "Sleep Apnea Events")
    show_bar("fall_detected", "Fall Detection Events")
    show_line("cycle_day", "Menstrual Cycle")
    show_line("carotenoids", "Antioxidant Index")

elif role == "Athlete":
    st.header("Athlete Dashboard – Daily Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric("steps", "Total Steps")

    with col2:
        show_metric("calories", "Total Calories")

    with col3:
        show_metric("active_minutes", "Active Minutes")

    show_bar("total_sleep_minutes", "Total Sleep")
    show_line("stress_level", "Stress Trend")
    show_line("energy_score", "Energy Score")

st.success("Dashboard Loaded Successfully")

