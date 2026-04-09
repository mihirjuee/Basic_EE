import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Fluid AC Analysis", layout="wide")

# Initialize global state
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0
if 'running' not in st.session_state:
    st.session_state.running = False

st.title("⚡ Continuous Phasor Analysis")

# --- SIDEBAR (Static) ---
st.sidebar.header("Machine Parameters")
V_m = st.sidebar.slider("Voltage ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current ($I_m$)", 1.0, 10.0, 6.0)
phi_deg = st.sidebar.slider("Phase Shift (φ°)", -180, 180, -45)
speed = st.sidebar.slider("Rotation Speed", 0.5, 10.0, 2.0)

# --- THE ANIMATION FRAGMENT ---
# run_every=0.01 creates the 'Play' effect automatically
@st.fragment(run_every=0.01 if st.session_state.running else None)
def render_phasor():
    # Buttons inside fragment to control local state
    c1, c2, _ = st.columns([1, 1, 8])
    if c1.button("▶️ Play", use_container_width=True):
        st.session_state.running = True
        st.rerun() # Refresh to start the 'run_every' timer
    if c2.button("⏸️ Pause", use_container_width=True):
        st.session_state.running = False
        st.rerun() # Refresh to stop the timer

    # Increment angle locally
    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    t_deg = st.session_state.theta_step
    p_rad = np.deg2rad(phi_deg)

    # Creating the Polar Plot
    fig = go.Figure()
    
    # Voltage Phasor
    fig.add_trace(go.Scatterpolar(
        r=[0, V_m], theta=[0, t_deg], 
        mode='lines+markers', line=dict(color='red', width=4), name='V'
    ))
    
    # Current Phasor
    fig.add_trace(go.Scatterpolar(
        r=[0, I_m], theta=[0, t_deg + phi_deg], 
        mode='lines+markers', line=dict(color='blue', width=4), name='I'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 10], visible=True)),
        showlegend=False, height=450, margin=dict(t=20, b=20)
    )

    # IMPORTANT: Use a STATIC key so it reuses the same element
    st.plotly_chart(fig, use_container_width=True, key="phasor_chart", config={'displayModeBar': False})

render_phasor()

st.markdown("---")
st.write("🔗 **Community:** [Follow my Facebook Page](https://www.facebook.com/your-page) for more updates.")
