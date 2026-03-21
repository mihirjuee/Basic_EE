import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("AC Fundamentals: Phasor & Time Domain")

# Sidebar controls for the student to interact with
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Amplitude (Voltage)", 1.0, 10.0, 5.0)
f = st.sidebar.slider("Frequency (Hz)", 0.0, 60.0, 50.0)
phase_deg = st.sidebar.slider("Phase Angle (degrees)", -180, 180, 0)

# The time scrubber allows manual animation
t_snapshot = st.sidebar.slider("Scrub Time (seconds)", 0.0, 0.04, 0.0, 0.01)

# Mathematical calculations
omega = 2 * np.pi * f
phase_rad = np.deg2rad(phase_deg)
t = np.linspace(0, 0.04, 500)
v_t = V_m * np.sin(omega * t + phase_rad)

# Calculate the exact angle of the phasor at the chosen time snapshot
current_angle = omega * t_snapshot + phase_rad

# Set up the visualization side-by-side
fig = plt.figure(figsize=(12, 5))

# Plot 1: Polar plot representing the rotating Phasor
ax1 = plt.subplot(121, projection='polar')
ax1.plot([0, current_angle], [0, V_m], marker='o', color='dodgerblue', linewidth=3)
ax1.set_ylim(0, 10)
ax1.set_title(f"Phasor Position at t = {t_snapshot:.2f}s", pad=20)

# Plot 2: Cartesian plot representing the Time Domain
ax2 = plt.subplot(122)
ax2.plot(t, v_t, color='crimson', label='$v(t)$')
# Draw a vertical line to show where we are in time
ax2.axvline(x=t_snapshot, color='dodgerblue', linestyle='--', alpha=0.7)
# Mark the exact point on the wave
ax2.plot(t_snapshot, V_m * np.sin(current_angle), marker='o', markersize=8, color='dodgerblue')

ax2.set_ylim(-10.5, 10.5)
ax2.set_title("Time Domain Waveform")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Voltage (V)")
ax2.axhline(0, color='black', linewidth=0.5)
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

# Render the plot in Streamlit
st.pyplot(fig)
