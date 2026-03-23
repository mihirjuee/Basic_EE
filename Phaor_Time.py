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
t_snapshot = st.sidebar.slider("Scrub Time (seconds)", 0.0, 0.02, 0.0, 0.01)

# Mathematical calculations
omega = 2 * np.pi * f
phase_rad = np.deg2rad(phase_deg)
t = np.linspace(0, 0.02, 500)
v_t = V_m * np.sin(omega * t + phase_rad)

# Calculate the exact angle of the phasor at the chosen time snapshot
current_angle = omega * t_snapshot + phase_rad

# Set up the visualization side-by-side
fig = plt.figure(figsize=(12, 5))

# Plot 1: Polar plot representing the rotating Phasor
ax1 = plt.subplot(121, projection='polar')

# Use annotate to draw an arrow from (0,0) to (angle, radius)
ax1.annotate('', xy=(current_angle, V_m), xytext=(0, 0),
             arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', 
                             shrink=0, width=2, headwidth=8))

# Add a point at the tip for extra emphasis
ax1.plot(current_angle, V_m, marker='o', color='dodgerblue', markersize=4)

ax1.set_ylim(0, 10)
ax1.set_title(f"Phasor Position at t = {t_snapshot:.2f}s", pad=20)

# Plot 2: Cartesian plot representing the Time Domain
ax2 = plt.subplot(122)
ax2.plot(degrees, v_theta, color='crimson', label='$v(\\theta)$', linewidth=2)

# Highlight the current position based on the scrubber
current_v = V_m * np.sin(current_theta_rad + phase_rad)
ax2.axvline(x=current_theta_deg, color='dodgerblue', linestyle='--', alpha=0.7)
ax2.plot(current_theta_deg, current_v, marker='o', markersize=8, color='dodgerblue')

# Formatting the X-axis for Degrees
ax2.set_xlim(0, 360)
ax2.set_xticks([0, 90, 180, 270, 360])
ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])

ax2.set_title("Waveform in Degree Domain")
ax2.set_xlabel("Angle (Degrees)")
ax2.set_ylabel("Voltage (V)")
ax2.grid(True, linestyle=':', alpha=0.6)

# Render the plot in Streamlit
st.pyplot(fig)
