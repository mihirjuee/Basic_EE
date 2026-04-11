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
st.sidebar.header("Signal Parameters")

V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phi_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# --- CONTROL BUTTONS ---
col1, col2, col3 = st.columns(3)

if col1.button("▶️ Play"):
    st.session_state.running = True

if col2.button("⏸️ Pause"):
    st.session_state.running = False

if col3.button("🔄 Reset"):
    st.session_state.theta_step = 0

# --- COMPUTATION ---
theta_deg = st.session_state.theta_step
theta_rad = np.deg2rad(theta_deg)
phi_rad = np.deg2rad(phi_deg)

# Waveform data
t_axis = np.linspace(0, 360, 500)
v_wave = V_m * np.sin(np.deg2rad(t_axis))
i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)

# Instantaneous values
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

# --- EQUATIONS ---
st.latex(r"v(t) = V_m \sin(\omega t)")
st.latex(r"i(t) = I_m \sin(\omega t + \phi)")

# --- PLOT ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'polar'}, {'type': 'xy'}]],
    column_widths=[0.4, 0.6]
)

# --- Voltage Vector (Arrow) ---
fig.add_trace(go.Scatterpolar(
    r=[0, V_m],
    theta=[0, theta_deg],
    mode='lines',
    line=dict(color='crimson', width=2),
    showlegend=False
), row=1, col=1)

fig.add_annotation(
    x=theta_deg,
    y=V_m,
    ax=0,
    ay=0,
    xref='x1',
    yref='y1',
    axref='x1',
    ayref='y1',
    text="V",
    showarrow=True,
    arrowhead=3,
    arrowsize=1.5,
    arrowwidth=3,
    arrowcolor='crimson'
)

# --- Current Vector (Arrow) ---
fig.add_trace(go.Scatterpolar(
    r=[0, I_m],
    theta=[0, theta_deg + phi_deg],
    mode='lines',
    line=dict(color='dodgerblue', width=2),
    showlegend=False
), row=1, col=1)

fig.add_annotation(
    x=theta_deg + phi_deg,
    y=I_m,
    ax=0,
    ay=0,
    xref='x1',
    yref='y1',
    axref='x1',
    ayref='y1',
    text="I",
    showarrow=True,
    arrowhead=3,
    arrowsize=1.5,
    arrowwidth=3,
    arrowcolor='dodgerblue'
)

# --- Waveforms ---
fig.add_trace(go.Scatter(
    x=t_axis, y=v_wave,
    line=dict(color='crimson'),
    opacity=0.3,
    name='Voltage Wave'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=t_axis, y=i_wave,
    line=dict(color='dodgerblue'),
    opacity=0.3,
    name='Current Wave'
), row=1, col=2)

# --- Instantaneous Points ---
fig.add_trace(go.Scatter(
    x=[theta_deg], y=[v_inst],
    mode='markers',
    marker=dict(size=12, color='crimson'),
    name='V(t)'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=[theta_deg], y=[i_inst],
    mode='markers',
    marker=dict(size=12, color='dodgerblue'),
    name='I(t)'
), row=1, col=2)

# --- Layout ---
fig.update_layout(
    height=500,
    margin=dict(t=30, b=30),
    polar=dict(radialaxis=dict(range=[0, 11]))
)

fig.update_xaxes(title="Phase Angle (Degrees)", range=[0, 360], row=1, col=2)
fig.update_yaxes(range=[-11, 11], row=1, col=2)

# --- Display ---
st.plotly_chart(fig, use_container_width=True)

# --- ANIMATION LOOP ---
if st.session_state.running:
    st.session_state.theta_step = (st.session_state.theta_step + speed * 0.5) % 360
    time.sleep(0.05)
    st.rerun()
