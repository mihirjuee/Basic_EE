import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AC V & I Analysis", layout="wide")
st.title("AC Fundamentals: Voltage vs. Current Analysis")

# --- Session State for Animation ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

# --- Sidebar Controls ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
# Current relative to Voltage
phase_diff_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)

st.sidebar.markdown("---")
st.sidebar.header("Motion Controls")
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# Manual Slider - Linked to session state
manual_theta = st.sidebar.slider("Manual Angle Scrub (θ)", 0.0, 360.0, 
                                  float(st.session_state.theta_step % 360), 
                                  step=1.0)
st.session_state.theta_step = manual_theta

# Play/Pause Buttons
col1, col2 = st.sidebar.columns(2)
if col1.button("▶️ Play"):
    st.session_state.running = True
if col2.button("⏸️ Pause"):
    st.session_state.running = False

# --- Mathematical Logic ---
v_phase_rad = 0 
i_phase_rad = np.deg2rad(phase_diff_deg)

current_theta_deg = st.session_state.theta_step % 360
current_theta_rad = np.deg2rad(current_theta_deg)

# 1. FIXED WAVEFORMS
degrees_axis = np.linspace(0, 360, 500)
rad_axis = np.deg2rad(degrees_axis)
v_waveform = V_m * np.sin(rad_axis + v_phase_rad)
i_waveform = I_m * np.sin(rad_axis + i_phase_rad)

# 2. MOVING TRACERS & VECTORS
v_inst = V_m * np.sin(current_theta_rad + v_phase_rad)
v_vec_angle = current_theta_rad + v_phase_rad

i_inst = I_m * np.sin(current_theta_rad + i_phase_rad)
i_vec_angle = current_theta_rad + i_phase_rad

# --- Displaying the Equations ---
st.markdown("### Instantaneous Equations")
st.latex(rf"v(\theta) = {V_m} \sin(\theta + 0^\circ)")
st.latex(rf"i(\theta) = {I_m} \sin(\theta + {phase_diff_deg}^\circ)")

# --- Visualization ---
plot_placeholder = st.empty()

with plot_placeholder.container():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), 
                                   gridspec_kw={'width_ratios': [1, 1.5]})

    # --- Plot 1: Dual Phasors (The Vectors) ---
    ax1.remove()
    ax1 = fig.add_subplot(121, projection='polar')
    
    # Voltage Vector (Red Arrow)
    ax1.annotate('', xy=(v_vec_angle, V_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='crimson', edgecolor='crimson', width=3, headwidth=10))
    # Current Vector (Blue Arrow)
    ax1.annotate('', xy=(i_vec_angle, I_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', width=3, headwidth=10))
    
    ax1.set_ylim(0, 10)
    ax1.set_title(f"Phasor Diagram\n$\theta = {current_theta_deg:.1f}^\circ$", pad=20)

    # --- Plot 2: Waveform Tracers (The Sine Waves) ---
    # Magnitude Zero Axis
    ax2.axhline(0, color='black', linewidth=1.5, alpha=0.8)
    
    # Static Waveforms (Path)
    ax2.plot(degrees_axis, v_waveform, color='crimson', alpha=0.3, label='Voltage $v(\\theta)$')
    ax2.plot(degrees_axis, i_waveform, color='dodgerblue', alpha=0.3, label='Current $i(\\theta)$')
    
    # Moving Tracers (Dots)
    ax2.plot(current_theta_deg, v_inst, 'o', color='crimson', markersize=10)
    ax2.plot(current_theta_deg, i_inst, 'o', color='dodgerblue', markersize=10)
    
    # Vertical Tracker Line
    ax2.axvline(x=current_theta_deg, color='gray', linestyle='--', alpha=0.3)
    
    # Formatting
    ax2.set_xlim(0, 360)
    ax2.set_ylim(-10.5, 10.5)
    ax2.set_xticks([0, 90, 180, 270, 360])
    ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
    ax2.set_xlabel("Angle (Degrees)")
    ax2.set_ylabel("Amplitude")
    ax2.set_title("Time Domain Comparison")
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.5)

    st.pyplot(fig)
    plt.close(fig)

# --- Animation Loop Logic ---
if st.session_state.running:
    st.session_state.theta_step += speed
    time.sleep(0.01)
    st.rerun()
