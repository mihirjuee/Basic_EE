import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AC Phasor Animation", layout="wide")
st.title("AC Fundamentals: Rotating Phasor & Fixed Waveform")

# --- Session State Initialization ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

# --- Sidebar Controls ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Amplitude (V_m)", 1.0, 10.0, 5.0)
phase_deg = st.sidebar.slider("Initial Phase (φ)", -180, 180, 0)
speed = st.sidebar.slider("Animation Speed", 1, 20, 5)

# Play/Pause Buttons
col1, col2, col3 = st.sidebar.columns(3)
if col1.button("Play"):
    st.session_state.running = True
if col2.button("Pause"):
    st.session_state.running = False
if col3.button("Reset"):
    st.session_state.theta_step = 0.0
    st.session_state.running = False

# --- Calculations ---
phase_rad = np.deg2rad(phase_deg)
# The static waveform (0 to 360 degrees)
degrees_axis = np.linspace(0, 360, 500)
v_theta = V_m * np.sin(np.deg2rad(degrees_axis) + phase_rad)

# Create a placeholder for the plot so it stays in one spot during animation
plot_placeholder = st.empty()

# --- Animation Loop ---
while True:
    # Current angle for the tracer
    current_theta_deg = st.session_state.theta_step % 360
    current_theta_rad = np.deg2rad(current_theta_deg)
    
    # Calculate tracer height and phasor total angle
    v_instant = V_m * np.sin(current_theta_rad + phase_rad)
    total_phasor_angle = current_theta_rad + phase_rad

    # --- Plotting ---
    fig = plt.figure(figsize=(12, 5))
    
    # Plot 1: Polar Phasor (Moving Arrow)
    ax1 = plt.subplot(121, projection='polar')
    ax1.annotate('', xy=(total_phasor_angle, V_m), xytext=(0, 0),
                 arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', width=2, headwidth=8))
    ax1.plot(total_phasor_angle, V_m, marker='o', color='dodgerblue', markersize=4)
    ax1.set_ylim(0, 10)
    ax1.set_title(f"Phasor Angle: {current_theta_deg:.1f}°", pad=20)

    # Plot 2: Degree Domain (Moving Tracer)
    ax2 = plt.subplot(122)
    ax2.plot(degrees_axis, v_theta, color='crimson', alpha=0.4, label='Fixed Waveform')
    # The moving dot (The Tracer)
    ax2.plot(current_theta_deg, v_instant, marker='o', markersize=10, color='dodgerblue', label='Tracer')
    ax2.axvline(x=current_theta_deg, color='dodgerblue', linestyle='--', alpha=0.3)
    
    # Formatting Plot 2
    ax2.set_xlim(0, 360)
    ax2.set_xticks([0, 90, 180, 270, 360])
    ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
    ax2.set_ylim(-10.5, 10.5)
    ax2.set_title("Time Domain Tracer")
    ax2.set_xlabel("Angle (Degrees)")
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')

    # Render inside the placeholder
    plot_placeholder.pyplot(fig)
    plt.close(fig) # Prevent memory buildup

    # Handle animation timing
    if st.session_state.running:
        st.session_state.theta_step += speed
        time.sleep(0.05)
        st.rerun() # Refresh the app to show next frame
    else:
        break # Exit loop if paused
