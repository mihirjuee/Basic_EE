import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AC V & I Analysis", layout="wide")

# --- SESSION STATE ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

# --- TITLE ---
st.title("⚡ AC Fundamentals: Voltage & Current Visualization")

# --- SIDEBAR ---
V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phi_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# --- BUTTONS ---
col1, col2, col3 = st.columns(3)

if col1.button("▶️ Play"):
    st.session_state.running = True

if col2.button("⏸️ Pause"):
    st.session_state.running = False

if col3.button("🔄 Reset"):
    st.session_state.theta_step = 0

# --- CALCULATIONS ---
theta_deg = st.session_state.theta_step
theta_rad = np.deg2rad(theta_deg)
phi_rad = np.deg2rad(phi_deg)

# Waveforms
t_axis = np.linspace(0, 360, 500)
v_wave = V_m * np.sin(np.deg2rad(t_axis))
i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)

v_inst = V_m * np.sin(theta_rad)
i_inst = I_m * np.sin(theta_rad + phi_rad)

# --- METRICS ---
pf = np.cos(phi_rad)

m1, m2 = st.columns(2)
m1.metric("Power Factor", f"{pf:.2f}")

if phi_deg > 0:
    m2.info("Current is Leading ⚡")
elif phi_deg < 0:
    m2.info("Current is Lagging ⚡")
else:
    m2.success("Unity Power Factor")

# --- PLOT PLACEHOLDER ---
plot_area = st.empty()

# --- CREATE FIGURE ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'polar'}, {'type': 'xy'}]],
    column_widths=[0.4, 0.6]
)

# --- VECTOR WITH ARROWS ---
fig.add_trace(go.Scatterpolar(
    r=[0, V_m],
    theta=[0, theta_deg],
    mode='lines',
    line=dict(color='crimson', width=4)
), row=1, col=1)

fig.add_trace(go.Scatterpolar(
    r=[V_m],
    theta=[theta_deg],
    mode='markers',
    marker=dict(size=12, color='crimson', symbol='triangle-up')
), row=1, col=1)

fig.add_trace(go.Scatterpolar(
    r=[0, I_m],
    theta=[0, theta_deg + phi_deg],
    mode='lines',
    line=dict(color='dodgerblue', width=4)
), row=1, col=1)

fig.add_trace(go.Scatterpolar(
    r=[I_m],
    theta=[theta_deg + phi_deg],
    mode='markers',
    marker=dict(size=12, color='dodgerblue', symbol='triangle-up')
), row=1, col=1)

# --- WAVEFORMS ---
fig.add_trace(go.Scatter(x=t_axis, y=v_wave,
                         line=dict(color='crimson'), opacity=0.3), row=1, col=2)

fig.add_trace(go.Scatter(x=t_axis, y=i_wave,
                         line=dict(color='dodgerblue'), opacity=0.3), row=1, col=2)

fig.add_trace(go.Scatter(x=[theta_deg], y=[v_inst],
                         mode='markers', marker=dict(size=10, color='crimson')), row=1, col=2)

fig.add_trace(go.Scatter(x=[theta_deg], y=[i_inst],
                         mode='markers', marker=dict(size=10, color='dodgerblue')), row=1, col=2)

fig.update_layout(height=500, polar=dict(radialaxis=dict(range=[0, 11])))

# --- DISPLAY ---
plot_area.plotly_chart(fig, use_container_width=True)

# --- ANIMATION CONTROL ---
if st.session_state.running:
    time.sleep(0.05)
    st.session_state.theta_step = (st.session_state.theta_step + speed * 0.5) % 360
    st.rerun()
