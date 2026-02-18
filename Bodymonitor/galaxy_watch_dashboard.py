import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Dashboard (Diversified Charts)")

# ===============================
# REALISTIC DATA
# ===============================

np.random.seed(42)
days = 30
dates = pd.date_range(end=pd.Timestamp.today(), periods=days)

# Workout pattern
workout_days = [i % 7 in [1,3,5] for i in range(days)]

# Steps
steps = [int(max(3000, np.random.randint(5000,10000)+(np.random.randint(1000,4000) if workout_days[i] else 0))) for i in range(days)]
active_minutes = [int(s/100) for s in steps]
calories = [int(1800 + s*0.04 + np.random.normal(0,100)) for s in steps]

# Heart rate
heart_rate = [int(np.random.normal(140,10) if workout_days[i] else np.random.normal(65,5)) for i in range(days)]

# Sleep
total_sleep = []
deep_sleep = []
rem_sleep = []
for i in range(days):
    sleep_time = np.random.normal(420,30)
    if workout_days[i]: sleep_time += 15
    total_sleep.append(int(max(300,sleep_time)))
    deep_sleep.append(int(total_sleep[i]*np.random.uniform(0.18,0.25)))
    rem_sleep.append(int(total_sleep[i]*np.random.uniform(0.18,0.22)))

# Stress & energy
stress = [int(np.random.normal(70,5)) if total_sleep[i]<380 else int(np.random.normal(50,10)) for i in range(days)]
energy_score = [int(100-(stress[i]*0.5)+(total_sleep[i]-400)*0.1) for i in range(days)]

# Body composition
body_fat = np.linspace(18,17,days) + np.random.normal(0,0.3,days)
muscle_mass = np.linspace(72,73,days) + np.random.normal(0,0.5,days)

# ECG, BP, SpO2, Apnea, Fall, Menstrual, Antioxidant
ecg_signal = np.random.normal(0,0.5,days)
ecg_signal[np.random.randint(0,days)] += 3  # rare spike
systolic = np.random.normal(120,7,days)
diastolic = np.random.normal(78,5,days)
spo2 = np.random.normal(97,1,days)
apnea_events = np.random.poisson(1,days)
fall_detected = np.random.choice([0,1],size=days,p=[0.95,0.05])
cycle_day = [(i%28)+1 for i in range(days)]
carotenoids = np.random.normal(4.5,0.6,days)

# ===============================
# BUILD DATAFRAMES
# ===============================

data = {
    "steps": pd.DataFrame({"datetime":dates,"steps":steps}),
    "active_minutes": pd.DataFrame({"datetime":dates,"active_minutes":active_minutes}),
    "calories": pd.DataFrame({"datetime":dates,"calories":calories}),
    "heart_rate": pd.DataFrame({"datetime":dates,"heart_rate":heart_rate}),
    "sleep": pd.DataFrame({"datetime":dates,"total_sleep_minutes":total_sleep,"deep_sleep":deep_sleep,"rem_sleep":rem_sleep}),
    "energy_score": pd.DataFrame({"datetime":dates,"energy_score":energy_score}),
    "stress": pd.DataFrame({"datetime":dates,"stress_level":stress}),
    "body_composition": pd.DataFrame({"datetime":dates,"body_fat_percent":body_fat,"muscle_mass":muscle_mass}),
    "ecg": pd.DataFrame({"datetime":dates,"ecg_signal":ecg_signal}),
    "blood_pressure": pd.DataFrame({"datetime":dates,"systolic":systolic,"diastolic":diastolic}),
    "spo2": pd.DataFrame({"datetime":dates,"spo2":spo2}),
    "sleep_apnea": pd.DataFrame({"datetime":dates,"apnea_events":apnea_events}),
    "fall_detection": pd.DataFrame({"datetime":dates,"fall_detected":fall_detected}),
    "menstrual_cycle": pd.DataFrame({"datetime":dates,"cycle_day":cycle_day}),
    "antioxidant_index": pd.DataFrame({"datetime":dates,"carotenoids":carotenoids})
}

# ===============================
# ROLE SELECTOR
# ===============================

role = st.sidebar.selectbox(
    "Select Dashboard Role",
    ["Coach","Trainer","Team Doctor","Athlete"]
)

# ===============================
# HELPER FUNCTIONS
# ===============================

def line_chart(df, y, title):
    if df is not None and y in df.columns:
        fig = px.line(df, x="datetime", y=y, title=title, markers=True)
        st.plotly_chart(fig, use_container_width=True)

def bar_chart(df, y, title):
    if df is not None and y in df.columns:
        fig = px.bar(df, x="datetime", y=y, title=title, color=y, color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

def area_chart(df, y1, y2, title):
    if df is not None and y1 in df.columns and y2 in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["datetime"], y=df[y1], fill='tozeroy', mode='none', name=y1))
        fig.add_trace(go.Scatter(x=df["datetime"], y=df[y2], fill='tozeroy', mode='none', name=y2))
        fig.update_layout(title=title)
        st.plotly_chart(fig, use_container_width=True)

def metric(label, value):
    if value is not None:
        st.metric(label, round(float(value),2))

# ===============================
# DASHBOARDS
# ===============================

if role=="Coach":
    st.header("Coach Dashboard – Performance")
    metric("Total Steps (30 days)", sum(steps))
    line_chart(data["steps"], "steps","Daily Steps")
    line_chart(data["heart_rate"], "heart_rate","Heart Rate Trend")
    line_chart(data["energy_score"], "energy_score","Energy Score")
    area_chart(data["sleep"], "deep_sleep","rem_sleep","Sleep Stages (Deep & REM)")

elif role=="Trainer":
    st.header("Trainer Dashboard – Conditioning")
    line_chart(data["body_composition"], "body_fat_percent","Body Fat %")
    line_chart(data["body_composition"], "muscle_mass","Muscle Mass")
    bar_chart(data["calories"], "calories","Calories Burned")
    area_chart(data["sleep"], "deep_sleep","rem_sleep","Sleep Stages")
    line_chart(data["stress"], "stress_level","Stress Levels")

elif role=="Team Doctor":
    st.header("Team Doctor Dashboard – Clinical")
    line_chart(data["ecg"], "ecg_signal","ECG Signal")
    line_chart(data["blood_pressure"], "systolic","Systolic BP")
    line_chart(data["blood_pressure"], "diastolic","Diastolic BP")
    line_chart(data["spo2"], "spo2","SpO2")
    bar_chart(data["sleep_apnea"], "apnea_events","Sleep Apnea Events")
    bar_chart(data["fall_detection"], "fall_detected","Fall Events")
    line_chart(data["menstrual_cycle"], "cycle_day","Menstrual Cycle")
    line_chart(data["antioxidant_index"], "carotenoids","Antioxidant Index")

elif role=="Athlete":
    st.header("Athlete Dashboard – Daily Overview")
    col1,col2,col3 = st.columns(3)
    with col1: metric("Steps", sum(steps))
    with col2: metric("Calories", sum(calories))
    with col3: metric("Active Minutes", sum(active_minutes))
    bar_chart(data["sleep"], "total_sleep_minutes","Daily Sleep")
    line_chart(data["stress"], "stress_level","Stress Trend")
    line_chart(data["energy_score"], "energy_score","Energy Score")

st.success("Dashboard Loaded Successfully ✅")

