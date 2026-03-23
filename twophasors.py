import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AC V & I Comparison", layout="wide")
st.title("AC Fundamentals: Voltage vs. Current Phasors")

# --- Session State for Animation ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

# --- Sidebar Controls ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Voltage Amplitude (V_p)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude (I_p)", 1.0, 10.0, 5.0)
# This is the shift between V and I
phase_diff_deg = st.sidebar.slider("Phase Difference (Current relative to V)", -180, 180, -90)

st.sidebar.markdown("---")
st.sidebar.header("Motion Controls")
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)
manual_theta = st.sidebar.slider("Manual Angle Scrub", 0.0, 360.0, 
                                  float(st.session_state.theta_step % 360), 
                                  step=1.0)
st.session_state.theta_step = manual_theta

col1, col2 = st.sidebar.columns(2)
if col1.button("▶️ Play"):
    st.session_state.running = True
if col2.button("⏸️ Pause"):
    st.session_state.running = False

# --- Mathematical Logic ---
# We treat Voltage as the reference (0 degrees)
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
# Voltage position
v_inst = V_m * np.sin(current_theta_rad + v_phase_rad)
v_vec_angle = current_theta_rad + v_phase_rad

# Current position
i_inst = I_m * np.sin(current_theta_rad + i_phase_rad)
i_vec_angle = current_theta_rad + i_phase_rad

# --- Visualization ---
plot_placeholder = st.empty()

with plot_placeholder.container():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), 
                                   gridspec_kw={'width_ratios': [1, 1.5]})

    # --- Plot 1: Dual Phasors ---
    ax1.remove()
    ax1 = fig.add_subplot(121, projection='polar')
    
    # Voltage Vector (Red)
    ax1.annotate('', xy=(v_vec_angle, V_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='crimson', edgecolor='crimson', width=3))
    # Current Vector (Blue)
    ax1.annotate('', xy=(i_vec_angle, I_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', width=3))
    
    ax1.set_ylim(0, 10)
    ax1.set_title("Phasor Diagram (V in Red, I in Blue)")

    # --- Plot 2: Waveform Tracers ---
    ax2.axhline(0, color='black', linewidth=1, alpha=0.7) # Zero Axis
    
    # Static Waveforms
    ax2.plot(degrees_axis, v_waveform, color='crimson', alpha=0.3, label='Voltage $v(t)$')
    ax2.plot(degrees_axis, i_waveform, color='dodgerblue', alpha=0.3, label='Current $i(t)$')
    
    # Moving Tracers
    ax2.plot(current_theta_deg, v_inst, 'o', color='crimson', markersize=10)
    ax2.plot(current_theta_deg, i_inst, 'o', color='dodgerblue', markersize=10)
    
    # Vertical Tracker
    ax2.axvline(x=current_theta_deg, color='gray', linestyle='--', alpha=0.3)
    
    # Formatting
    ax2.set_xlim(0, 360)
    ax2.set_ylim(-10.5, 10.5)
    ax2.set_xticks([0, 90, 180, 270, 360])
    ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
    ax2.set_title("Waveform Comparison")
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.5)

    st.pyplot(fig)
    plt.close(fig)

# --- Animation Loop ---
if st.session_state.running:
    st.session_state.theta_step += speed
    time.sleep(0.01)
    st.rerun()
