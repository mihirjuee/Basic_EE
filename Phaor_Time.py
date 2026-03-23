import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("AC Fundamentals: Fixed Waveform & Moving Tracer")

# --- Sidebar ---
V_m = st.sidebar.slider("Amplitude (Voltage)", 1.0, 10.0, 5.0)
f = st.sidebar.slider("Frequency (Hz)", 1.0, 60.0, 50.0)
phase_deg = st.sidebar.slider("Initial Phase (φ)", -180, 180, 0)

# Scrubber for the angle (0 to 360 degrees)
# This moves the tracer, NOT the wave
theta_scrub = st.sidebar.slider("Tracer Position (Degrees)", 0, 360, 0)

# --- Calculations ---
phase_rad = np.deg2rad(phase_deg)
theta_scrub_rad = np.deg2rad(theta_scrub)

# 1. The Fixed Waveform: v(θ) = Vm * sin(θ + φ)
# This stays put unless you change Vm or Phase
degrees_axis = np.linspace(0, 360, 500)
v_theta = V_m * np.sin(np.deg2rad(degrees_axis) + phase_rad)

# 2. The Moving Tracer: The height of the dot at the scrubbed position
# v_instant = Vm * sin(θ_scrub + φ)
v_instant = V_m * np.sin(theta_scrub_rad + phase_rad)

# --- Visualization ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1, 1.5]})

# Plot 1: Rotating Phasor (The Vector)
# Use polar projection
ax1.remove()
ax1 = fig.add_subplot(121, projection='polar')

# The phasor angle is the scrubbed position PLUS the initial phase
total_angle = theta_scrub_rad + phase_rad

ax1.annotate('', xy=(total_angle, V_m), xytext=(0, 0),
             arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', width=2))
ax1.set_ylim(0, 10)
ax1.set_title("Phasor Representation")

# Plot 2: Time/Degree Domain (The Path)
ax2.plot(degrees_axis, v_theta, color='crimson', alpha=0.5, label='Signal Path')

# The Tracer (The Moving Dot)
ax2.plot(theta_scrub, v_instant, marker='o', markersize=10, color='dodgerblue', label='Tracer')
# Vertical guide line
ax2.axvline(x=theta_scrub, color='dodgerblue', linestyle='--', alpha=0.3)

# Formatting
ax2.set_xlim(0, 360)
ax2.set_xticks([0, 90, 180, 270, 360])
ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
ax2.set_ylim(-10.5, 10.5)
ax2.set_xlabel("Angle (Degrees)")
ax2.set_ylabel("Voltage (V)")
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

st.pyplot(fig)
