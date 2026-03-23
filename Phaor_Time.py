import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AC Phasor & Tracer", layout="wide")
st.title("AC Fundamentals: Moving Tracer & Vector")

# --- Session State for Animation ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

# --- Sidebar Controls ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Amplitude (V_m)", 1.0, 10.0, 5.0)
phase_deg = st.sidebar.slider("Initial Phase (φ)", -180, 180, 0)

st.sidebar.markdown("---")
st.sidebar.header("Motion Controls")
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

# Manual Slider - Linked to session state
manual_theta = st.sidebar.slider("Manual Angle Scrub", 0.0, 360.0, 
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
phase_rad = np.deg2rad(phase_deg)
current_theta_deg = st.session_state.theta_step % 360
current_theta_rad = np.deg2rad(current_theta_deg)

# 1. FIXED WAVEFORM 
degrees_axis = np.linspace(0, 360, 500)
v_waveform = V_m * np.sin(np.deg2rad(degrees_axis) + phase_rad)

# 2. MOVING TRACER & VECTOR
v_instant = V_m * np.sin(current_theta_rad + phase_rad)
total_vector_angle = current_theta_rad + phase_rad

# --- Visualization ---
plot_placeholder = st.empty()

with plot_placeholder.container():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), 
                                   gridspec_kw={'width_ratios': [1, 1.5]})

    # --- Plot 1: The Vector (Phasor) ---
    ax1.remove()
    ax1 = fig.add_subplot(121, projection='polar')
    ax1.annotate('', xy=(total_vector_angle, V_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', 
                                 width=3, headwidth=10))
    ax1.set_ylim(0, 10)
    ax1.set_title(f"Rotating Vector: {current_theta_deg:.1f}°", pad=20)

    # --- Plot 2: The Tracer (Time Domain) ---
    # The Magnitude Zero Axis (Solid black line)
    ax2.axhline(0, color='black', linewidth=1.5, alpha=0.8)
    
    # Draw the static waveform 
    ax2.plot(degrees_axis, v_waveform, color='crimson', linewidth=2, alpha=0.4, label='Signal Path')
    
    # Draw the moving tracer (The Dot)
    ax2.plot(current_theta_deg, v_instant, marker='o', markersize=12, 
             color='dodgerblue', label='Tracer')
    
    # Visual cues: Vertical tracking line
    ax2.axvline(x=current_theta_deg, color='dodgerblue', linestyle='--', alpha=0.3)
    
    # Formatting
    ax2.set_xlim(0, 360)
    ax2.set_ylim(-10.5, 10.5)
    ax2.set_xticks([0, 90, 180, 270, 360])
    ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
    ax2.set_xlabel("Cycle Angle (Degrees)")
    ax2.set_ylabel("Voltage (V)")
    ax2.set_title("Waveform Tracer")
    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.legend(loc='upper right')

    st.pyplot(fig)
    plt.close(fig)

# --- Animation Loop Logic ---
if st.session_state.running:
    st.session_state.theta_step += speed
    time.sleep(0.01)
    st.rerun()
