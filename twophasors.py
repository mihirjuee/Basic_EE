import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Continuous Phasor Lab", layout="wide")

# Initialize the global angle if it doesn't exist
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0
if 'running' not in st.session_state:
    st.session_state.running = False

st.title("⚡ Continuous Phasor & Waveform Analysis")

# --- Sidebar for Parameters (Static) ---
st.sidebar.header("Machine Settings")
V_m = st.sidebar.slider("Voltage Peak ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Peak ($I_m$)", 1.0, 10.0, 6.0)
phi_deg = st.sidebar.slider("Phase Angle (φ°)", -180, 180, -45)
speed = st.sidebar.slider("Rotation Speed", 1.0, 10.0, 5.0)

# --- The Animation Fragment ---
@st.fragment
def continuous_phasor_movement():
    # 1. Local UI Controls (Must be inside to avoid Errors)
    col1, col2, _ = st.columns([1, 1, 8])
    play = col1.button("▶️ Play")
    pause = col2.button("⏸️ Pause")

    if play:
        st.session_state.running = True
    if pause:
        st.session_state.running = False

    # Create a persistent placeholder for the plots
    plot_spot = st.empty()

    # 2. The Loop for Smooth Motion
    while st.session_state.running:
        # Increment the angle
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360
        
        # Prepare Data
        t_deg = st.session_state.theta_step
        t_rad = np.deg2rad(t_deg)
        p_rad = np.deg2rad(phi_deg)
        
        # Plotly is much faster than Matplotlib for this
        fig = go.Figure()
        
        # Add Phasors (Vectors)
        # Voltage Vector
        fig.add_trace(go.Scatterpolar(r=[0, V_m], theta=[0, t_deg], mode='lines+markers', 
                                     line=dict(color='red', width=4), name='V'))
        # Current Vector
        fig.add_trace(go.Scatterpolar(r=[0, I_m], theta=[0, t_deg + phi_deg], mode='lines+markers', 
                                     line=dict(color='blue', width=4), name='I'))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False, height=450, margin=dict(t=30, b=30)
        )

        # Update the placeholder instantly
        plot_spot.plotly_chart(fig, use_container_width=True, key=f"phasor_{t_deg}")
        
        # Micro-sleep to control frame rate and allow UI responsiveness
        time.sleep(0.01)

    # If not running, show the static state
    if not st.session_state.running:
        # (Same plotting logic as above but without the while loop)
        st.info("Click Play to start the machine rotation.")

# Execute the fragment
continuous_phasor_movement()

st.markdown("---")
st.write("🔗 **Professor's Community:** [Follow my Facebook Page](https://www.facebook.com/your-page) for more interactive EE models.")
