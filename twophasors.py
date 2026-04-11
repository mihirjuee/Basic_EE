import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="AC V & I Analysis", layout="wide")

# --- 1. STATE MANAGEMENT ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

st.title("⚡ AC Fundamentals: Instantaneous Analysis")

# --- 2. SIDEBAR ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Voltage ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current ($I_m$)", 1.0, 10.0, 5.0)
phi_deg = st.sidebar.slider("Phase Shift (φ°)", -180, 180, -90)
speed = st.sidebar.slider("Speed", 1, 20, 5)

# --- 3. ANIMATION FRAGMENT ---
@st.fragment(run_every=0.01 if st.session_state.running else None)
def render_animation():
    # PLAY/PAUSE
    btn_cols = st.columns([1, 1, 8])
    if btn_cols[0].button("▶️ Play"):
        st.session_state.running = True
        st.rerun()
    if btn_cols[1].button("⏸️ Pause"):
        st.session_state.running = False
        st.rerun()

    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    # Math
    theta_deg = st.session_state.theta_step
    theta_rad = np.deg2rad(theta_deg)
    phi_rad = np.deg2rad(phi_deg)
    
    t_axis = np.linspace(0, 360, 400)
    v_wave = V_m * np.sin(np.deg2rad(t_axis))
    i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)
    
    v_inst = V_m * np.sin(theta_rad)
    i_inst = I_m * np.sin(theta_rad + phi_rad)

    # --- PLOTLY FIGURE (FASTER RENDERING) ---
    fig = make_subplots(
        rows=1, cols=2, 
        specs=[[{'type': 'polar'}, {'type': 'xy'}]],
        column_widths=[0.4, 0.6]
    )

    # Phasor: Voltage
    fig.add_trace(go.Scatterpolar(r=[0, V_m], theta=[0, theta_deg], mode='lines+markers', 
                                 line=dict(color='crimson', width=4), name='Voltage'), row=1, col=1)
    # Phasor: Current
    fig.add_trace(go.Scatterpolar(r=[0, I_m], theta=[0, theta_deg + phi_deg], mode='lines+markers', 
                                 line=dict(color='dodgerblue', width=4), name='Current'), row=1, col=1)

    # Waveform: Voltage
    fig.add_trace(go.Scatter(x=t_axis, y=v_wave, line=dict(color='crimson', width=1), opacity=0.3, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[v_inst], mode='markers', marker=dict(size=12, color='crimson'), showlegend=False), row=1, col=2)

    # Waveform: Current
    fig.add_trace(go.Scatter(x=t_axis, y=i_wave, line=dict(color='dodgerblue', width=1), opacity=0.3, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[i_inst], mode='markers', marker=dict(size=12, color='dodgerblue'), showlegend=False), row=1, col=2)

    fig.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20), polar=dict(radialaxis=dict(range=[0, 10])))
    fig.update_xaxes(title="Degrees", range=[0, 360], row=1, col=2)
    fig.update_yaxes(range=[-11, 11], row=1, col=2)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

render_animation()
