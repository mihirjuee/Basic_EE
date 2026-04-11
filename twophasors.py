import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="AC V & I Analysis", layout="wide")

# --- 1. GLOBAL STATE INITIALIZATION ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

st.title("AC Fundamentals: Voltage vs. Current Analysis")

# --- 2. SIDEBAR (STATIC PARAMETERS) ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phase_diff_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)

st.sidebar.markdown("---")
st.sidebar.header("Motion Controls")
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# --- 3. THE ANIMATION FRAGMENT ---
# The 'run_every' must be a float/int to stay active. 
# We use a small value when running and a very large value (or None) when paused.
@st.fragment(run_every=0.01 if st.session_state.running else None)
def render_animation():
    # 1. CONTROLS
    cols = st.columns([1, 1, 8])
    
    # Use on_click or direct check to toggle state
    if cols[0].button("▶️ Play"):
        st.session_state.running = True
        st.rerun() # Force immediate update to trigger run_every
        
    if cols[1].button("⏸️ Pause"):
        st.session_state.running = False
        st.rerun() # Force immediate update to stop run_every

    # 2. LOGIC: Increment angle only if running
    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    # 3. CALCULATIONS
    current_theta_deg = st.session_state.theta_step
    current_theta_rad = np.deg2rad(current_theta_deg)
    v_phase_rad = 0 
    i_phase_rad = np.deg2rad(phase_diff_deg)

    # Waveform Data
    degrees_axis = np.linspace(0, 360, 500)
    rad_axis = np.deg2rad(degrees_axis)
    v_waveform = V_m * np.sin(rad_axis + v_phase_rad)
    i_waveform = I_m * np.sin(rad_axis + i_phase_rad)

    # Instantaneous Values
    v_inst = V_m * np.sin(current_theta_rad + v_phase_rad)
    i_inst = I_m * np.sin(current_theta_rad + i_phase_rad)

    st.latex(rf"v(\theta) = {V_m} \sin(\theta + 0^\circ) \quad | \quad i(\theta) = {I_m} \sin(\theta + {phase_diff_deg}^\circ)")

    # 4. PLOTTING
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1, 1.5]})

    # Phasor Plot
    ax1.remove()
    ax1 = fig.add_subplot(121, projection='polar')
    ax1.annotate('', xy=(current_theta_rad + v_phase_rad, V_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='crimson', edgecolor='crimson', width=3))
    ax1.annotate('', xy=(current_theta_rad + i_phase_rad, I_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', width=3))
    ax1.set_ylim(0, 10)
    ax1.set_title(f"Phasor Diagram ({current_theta_deg:.1f}°)")

    # Waveform Plot
    ax2.plot(degrees_axis, v_waveform, color='crimson', alpha=0.3, label='Voltage')
    ax2.plot(degrees_axis, i_waveform, color='dodgerblue', alpha=0.3, label='Current')
    ax2.scatter(current_theta_deg, v_inst, color='crimson', s=100)
    ax2.scatter(current_theta_deg, i_inst, color='dodgerblue', s=100)
    ax2.set_xlim(0, 360)
    ax2.set_ylim(-11, 11)
    ax2.legend()

    st.pyplot(fig)
    plt.close(fig)

# --- 4. RUN ---
render_animation()

st.markdown("---")
st.write("👨‍🏫 **Professor's Note:** The phasors rotate counter-clockwise to represent time progression.")
