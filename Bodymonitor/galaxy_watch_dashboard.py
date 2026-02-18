import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")
st.title("Galaxy Watch 8 Performance System (Realistic Simulation)")

# ===============================
# REALISTIC DATA GENERATION
# ===============================

np.random.seed(42)
days = 30
dates = pd.date_range(end=pd.Timestamp.today(), periods=days)

# Simulate weekly workout pattern
workout_days = [i % 7 in [1, 3, 5] for i in range(days)]

# Steps (higher on workout days)
steps = []
for i in range(days):
    base = np.random.normal(7000, 1200)
    if workout_days[i]:
        base += np.random.normal(4000, 800)
    steps.append(int(max(3000, base)))

# Active Minutes
active_minutes = [int(s / 120) for s in steps]

# Calories (based on activity)
calories = [int(1800 + s * 0.05 + np.random.normal(0, 150)) for s in steps]

# Heart Rate (rest + workout spikes)
heart_rate = []
for i in range(days):
    if workout_days[i]:
        heart_rate.append(int(np.random.normal(145, 10)))
    else:
        heart_rate.append(int(np.random.normal(68, 5)))

# Sleep (worse after workout days)
total_sleep = []
deep_sleep = []
rem_sleep = []

for i in range(days):
    sleep_time = np.random.normal(420, 40)
    if workout_days[i]:
        sleep_time += 20  # better recovery sleep
    total_sleep.append(int(max(300, sleep_time)))
    deep_sleep.append(int(total_sleep[i] * np.random.uniform(0.18, 0.25)))
    rem_sleep.append(int(total_sleep[i] * np.random.uniform(0.18, 0.22)))

# Stress (higher on low sleep days)
stress = []
for i in range(days):
    if total_sleep[i] < 380:
        stress.append(int(np.random.normal(75, 5)))
    else:
        stress.append(int(np.random.normal(45, 10)))

# Energy score (sleep + stress dependent)
energy_score = [
    int(100 - (stress[i] * 0.5) + (total_sleep[i] - 400) * 0.1)
    for i in range(days)
]

# Body Composition (slow change trend)
body_fat = np.li_


