import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("AC Fundamentals: Phasor & Degree Domain")

# --- Sidebar controls ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Amplitude (Voltage)", 1.0, 10.0, 5.0)
f = st.sidebar.slider("Frequency (Hz)", 1.0, 60.0, 50.0) # Start at 1Hz to avoid div by zero
phase_deg = st.sidebar.slider("Phase Angle (degrees)", -180, 180, 0)

# Time scrubber: 0 to one full period (T = 1/f)
period = 1/f
t_snapshot = st.sidebar.slider("Scrub Time (seconds)", 0.0, period, 0.0, 0.0001, format="%.4f")

# --- Mathematical calculations ---
phase_rad = np.deg2rad(phase_deg)

# 1. Generate the Waveform (0 to 360 degrees)
degrees = np.linspace(0, 360, 500)
radians_array = np.deg2rad(degrees)
# v(theta) = Vm * sin(theta + phase)
v_theta = V_m * np.sin(radians_array + phase_rad)

# 2. Calculate current position based on time scrubber
# omega * t gives the angle traveled in radians
omega = 2 * np.pi * f
current_theta_rad = omega * t_snapshot
current_theta_deg = np.rad2deg(current_theta_rad)

# Total angle for the phasor (rotation + initial phase)
total_phasor_angle = current_theta_rad + phase_rad

# --- Visualization ---
fig = plt.figure(figsize=(12, 5))

# Plot 1: Polar plot (The Rotating Phasor)
ax1 = plt.subplot(121, projection='polar')
ax1.annotate('', xy=(total_phasor_angle, V_m), xytext=(0, 0),
             arrowprops=dict(facecolor='dodgerblue', edgecolor='dodgerblue', 
                             shrink=0, width=2, headwidth=8))
ax1.plot(total_phasor_angle, V_m, marker='o', color='dodgerblue', markersize=4)
ax1.set_ylim(0, 10)
ax1.set_title(f"Phasor at t = {t_snapshot:.4f}s", pad=20)

# Plot 2: Cartesian plot (Degree Domain)
ax2 = plt.subplot(122)
ax2.plot(degrees, v_theta, color='crimson', label='$v(\\theta)$', linewidth=2)

# Marker for current position
current_v = V_m * np.sin(total_phasor_angle)
ax2.axvline(x=current_theta_deg, color='dodgerblue', linestyle='--', alpha=0.7)
ax2.plot(current_theta_deg, current_v, marker='o', markersize=8, color='dodgerblue')

# Formatting
ax2.set_xlim(0, 360)
ax2.set_xticks([0, 90, 180, 270, 360])
ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
ax2.set_ylim(-10.5, 10.5)
ax2.set_title("Waveform (0-360°)")
ax2.set_xlabel("Angle (Degrees)")
ax2.set_ylabel("Voltage (V)")
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

st.pyplot(fig)
