import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="AC V & I Analysis", layout="wide")

if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

st.title("AC Fundamentals: Voltage vs. Current Analysis")

# --- 2. SIDEBAR (STATIC INPUTS) ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phase_diff_deg = st.sidebar.slider("Phase Shift (φ°)", -180, 180, -90)

st.sidebar.markdown("---")
st.sidebar.header("Motion Controls")
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# --- 3. THE ANIMATION FRAGMENT ---
@st.fragment(run_every=0.01 if st.session_state.running else None)
def render_animation():
    # BUTTONS MUST BE INSIDE THE FRAGMENT
    # We use a container to keep them together
    with st.container():
        ctrl_col1, ctrl_col2, _ = st.columns([1, 1, 8])
        if ctrl_col1.button("▶️ Play", use_container_width=True):
            st.session_state.running = True
        if ctrl_col2.button("⏸️ Pause", use_container_width=True):
            st.session_state.running = False

    # Logic to increment angle
    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    # Math Logic
    current_theta_deg = st.session_state.theta_step
    current_theta_rad = np.deg2rad(current_theta_deg)
    v_phase_rad = 0 
    i_phase_rad = np.deg2rad(phase_diff_deg)

    degrees_axis = np.linspace(0, 360, 500)
    rad_axis = np.deg2rad(degrees_axis)
    
    # Calculate Waves
    v_waveform = V_m * np.sin(rad_axis + v_phase_rad)
    i_waveform = I_m * np.sin(rad_axis + i_phase_rad)
    v_inst = V_m * np.sin(current_theta_rad + v_phase_rad)
    i_inst = I_m * np.sin(current_theta_rad + i_phase_rad)

    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), 
                                   gridspec_kw={'width_ratios': [1, 1.5]})

    # 1. Phasor Diagram
    ax1.remove()
    ax1 = fig.add_subplot(121, projection='polar')
    ax1.annotate('', xy=(current_theta_rad + v_phase_rad, V_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='crimson', edgecolor='crimson', width=2))
    ax1.annotate('', xy=(current_theta_rad + i_phase_rad, I_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', width=2))
    ax1.set_ylim(0, 11)
    ax1.set_title(f"$\theta = {current_theta_deg:.0f}^\circ$")

    # 2. Time Domain
    ax2.plot(degrees_axis, v_waveform, color='crimson', alpha=0.2)
    ax2.plot(degrees_axis, i_waveform, color='dodgerblue', alpha=0.2)
    ax2.plot(current_theta_deg, v_inst, 'o', color='crimson')
    ax2.plot(current_theta_deg, i_inst, 'o', color='dodgerblue')
    ax2.set_xlim(0, 360)
    ax2.set_ylim(-11, 11)
    ax2.grid(True, alpha=0.3)

    # CRITICAL: Ensures the app fits the display width
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Call the fragment
render_animation()

# --- 4. STATIC FOOTER ---
st.markdown("---")
st.write("🔗 [Visit my Facebook Page for Electrical Engineering Tutorials](https://www.facebook.com/your-page-link)")
