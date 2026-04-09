import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="EE Vector Lab", layout="wide")

if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0
if 'running' not in st.session_state:
    st.session_state.running = False

# --- SIDEBAR ---
st.sidebar.header("Machine Parameters")
V_m = st.sidebar.slider("Voltage ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current ($I_m$)", 1.0, 10.0, 6.0)
phi_deg = st.sidebar.slider("Phase Shift (φ°)", -180, 180, -45)
speed = st.sidebar.slider("Speed", 0.5, 10.0, 2.0)

# --- ANIMATION FRAGMENT ---
@st.fragment(run_every=0.01 if st.session_state.running else None)
def render_phasor():
    c1, c2, _ = st.columns([1, 1, 8])
    if c1.button("▶️ Play", use_container_width=True):
        st.session_state.running = True
        st.rerun()
    if c2.button("⏸️ Pause", use_container_width=True):
        st.session_state.running = False
        st.rerun()

    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    t_deg = st.session_state.theta_step
    # Angle for current is Voltage Angle + Phase Shift
    i_deg = t_deg + phi_deg

    fig = go.Figure()

    # 1. Voltage Vector (Red)
    fig.add_trace(go.Scatterpolar(
        r=[0, V_m], theta=[0, t_deg],
        mode='lines', line=dict(color='red', width=4), name='V'
    ))
    
    # 2. Current Vector (Blue)
    fig.add_trace(go.Scatterpolar(
        r=[0, I_m], theta=[0, i_deg],
        mode='lines', line=dict(color='blue', width=4), name='I'
    ))

    # 3. ADDING THE ARROWHEADS (Annotations)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(range=[0, 10], visible=True),
            angularaxis=dict(direction="counterclockwise")
        ),
        annotations=[
            # Voltage Arrowhead
            dict(
                xref="paper", yref="paper", x=0.5, y=0.5, # Center of polar plot
                axref="pixel", ayref="pixel",
                ax=V_m * 20 * np.cos(np.deg2rad(t_deg)), # Scale vector to pixels
                ay=-V_m * 20 * np.sin(np.deg2rad(t_deg)),
                showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=4, arrowcolor="red"
            ),
            # Current Arrowhead
            dict(
                xref="paper", yref="paper", x=0.5, y=0.5,
                axref="pixel", ayref="pixel",
                ax=I_m * 20 * np.cos(np.deg2rad(i_deg)),
                ay=-I_m * 20 * np.sin(np.deg2rad(i_deg)),
                showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=4, arrowcolor="blue"
            )
        ],
        showlegend=False, height=500, margin=dict(t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True, key="phasor_chart", config={'displayModeBar': False})

render_phasor()

st.markdown("---")
st.write("🔗 **Community:** [Follow my Facebook Page](https://www.facebook.com/your-page) for more updates.")
