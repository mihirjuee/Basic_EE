import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="AC V & I Analysis", layout="wide")

# --- 1. GLOBAL STATE INITIALIZATION (MUST BE AT THE TOP) ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

st.title("⚡ AC Fundamentals: Vector Rotation")

# --- 2. SIDEBAR PARAMETERS ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phi_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# --- 3. THE ANIMATION FRAGMENT ---
# Define the fragment AFTER session_state is guaranteed to exist
@st.fragment(run_every=0.01 if st.session_state.get('running', False) else None)
def render_animation():
    # Play/Pause Buttons
    cols = st.columns([1, 1, 8])
    if cols[0].button("▶️ Play"):
        st.session_state.running = True
        st.rerun()
    if cols[1].button("⏸️ Pause"):
        st.session_state.running = False
        st.rerun()

    # Increment logic
    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    theta_deg = st.session_state.theta_step
    theta_rad = np.deg2rad(theta_deg)
    phi_rad = np.deg2rad(phi_deg)

    # Math for Waveforms
    t_axis = np.linspace(0, 360, 500)
    v_wave = V_m * np.sin(np.deg2rad(t_axis))
    i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)
    v_inst = V_m * np.sin(theta_rad)
    i_inst = I_m * np.sin(theta_rad + phi_rad)

    # Plotly Figure
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'xy'}]], column_widths=[0.4, 0.6])

    # Voltage Vector & Arrow
    fig.add_trace(go.Scatterpolar(r=[0, V_m], theta=[0, theta_deg], mode='lines', line=dict(color='crimson', width=4), name='V'), row=1, col=1)
    fig.add_annotation(dict(ax=0, ay=0, axref='pixel', ayref='pixel', x=theta_deg, y=V_m, xref='x1', yref='y1', showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor='crimson'), row=1, col=1)

    # Current Vector & Arrow
    fig.add_trace(go.Scatterpolar(r=[0, I_m], theta=[0, theta_deg + phi_deg], mode='lines', line=dict(color='dodgerblue', width=4), name='I'), row=1, col=1)
    fig.add_annotation(dict(ax=0, ay=0, axref='pixel', ayref='pixel', x=theta_deg + phi_deg, y=I_m, xref='x1', yref='y1', showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=3, arrowcolor='dodgerblue'), row=1, col=1)

    # Waveform Plotting
    fig.add_trace(go.Scatter(x=t_axis, y=v_wave, line=dict(color='crimson'), opacity=0.2, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[v_inst], mode='markers', marker=dict(size=12, color='crimson'), name='V(t)'), row=1, col=2)
    fig.add_trace(go.Scatter(x=t_axis, y=i_wave, line=dict(color='dodgerblue'), opacity=0.2, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[i_inst], mode='markers', marker=dict(size=12, color='dodgerblue'), name='I(t)'), row=1, col=2)

    fig.update_layout(height=500, polar=dict(radialaxis=dict(range=[0, 11])), margin=dict(t=30, b=30))
    fig.update_xaxes(title="Phase Angle (Degrees)", range=[0, 360], row=1, col=2)
    fig.update_yaxes(range=[-11, 11], row=1, col=2)

    st.plotly_chart(fig, use_container_width=True)

# --- 4. EXECUTE ---
render_animation()
