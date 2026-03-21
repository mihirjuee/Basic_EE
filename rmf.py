import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Rotating Magnetic Field (RMF) Simulator")
st.markdown("Observe how three stationary coils fed by 3-phase currents create a rotating field.")

# User control to step through time (electrical degrees)
omega_t_deg = st.slider("Step through Time (Electrical Angle ωt in degrees)", 0, 360, 0, 5)
omega_t = np.deg2rad(omega_t_deg)

# --- Calculations ---
Im = 1.0 # Peak magnitude

# 1. Calculate the instantaneous currents (Time Domain)
# Displaced by 120 degrees in time
ia = Im * np.cos(omega_t)
ib = Im * np.cos(omega_t - np.deg2rad(120))
ic = Im * np.cos(omega_t - np.deg2rad(240))

# 2. Define the spatial orientation of the coils (Space Domain)
# Displaced by 120 degrees in space
dir_a = np.exp(1j * 0)                  # 0 degrees
dir_b = np.exp(1j * np.deg2rad(120))    # 120 degrees
dir_c = np.exp(1j * np.deg2rad(240))    # 240 degrees

# 3. Calculate individual magnetic field vectors (Current magnitude * Spatial direction)
Ba = ia * dir_a
Bb = ib * dir_b
Bc = ic * dir_c

# 4. Calculate the resultant magnetic field vector
B_net = Ba + Bb + Bc

# --- Plotting ---
fig = plt.figure(figsize=(14, 6))

# Left Plot: Time Domain Waveforms
ax1 = plt.subplot(121)
t_arr = np.linspace(0, 2*np.pi, 360)
ax1.plot(np.rad2deg(t_arr), Im * np.cos(t_arr), color='red', label=r'Phase A ($i_a$)')
ax1.plot(np.rad2deg(t_arr), Im * np.cos(t_arr - np.deg2rad(120)), color='blue', label=r'Phase B ($i_b$)')
ax1.plot(np.rad2deg(t_arr), Im * np.cos(t_arr - np.deg2rad(240)), color='green', label=r'Phase C ($i_c$)')

# Draw a vertical line to show the current 'time' snapshot
ax1.axvline(x=omega_t_deg, color='black', linestyle='--', linewidth=2, label='Current Snapshot')

ax1.set_title("3-Phase Currents (Time Domain)", fontsize=14)
ax1.set_xlabel("Electrical Angle ωt (degrees)")
ax1.set_ylabel("Current Magnitude")
ax1.set_xlim(0, 360)
ax1.grid(True, alpha=0.5)
ax1.legend(loc='upper right')

# Right Plot: Spatial Vectors (Polar Plot)
ax2 = plt.subplot(122, projection='polar')

# Plot the individual phase vectors (Notice the 'r' before the string)
ax2.plot([0, np.angle(Ba)], [0, np.abs(Ba)], color='red', linewidth=3, alpha=0.6, label=r'$\vec{B}_a$')
ax2.plot([0, np.angle(Bb)], [0, np.abs(Bb)], color='blue', linewidth=3, alpha=0.6, label=r'$\vec{B}_b$')
ax2.plot([0, np.angle(Bc)], [0, np.abs(Bc)], color='green', linewidth=3, alpha=0.6, label=r'$\vec{B}_c$')

# Plot the resultant rotating vector
ax2.plot([0, np.angle(B_net)], [0, np.abs(B_net)], color='black', linewidth=4, label=r'Net Field ($\vec{B}_{net}$)')
ax2.plot(np.angle(B_net), np.abs(B_net), marker='o', markersize=8, color='black')

# Formatting the polar plot
ax2.set_title(f"Resultant Spatial Vector\nMagnitude: {np.abs(B_net):.2f} (Constant at 1.5x Peak)", fontsize=14, pad=20)
ax2.set_ylim(0, 1.8)
ax2.set_yticks([0.5, 1.0, 1.5])
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# Render in Streamlit
st.pyplot(fig)

st.markdown("""
### The Takeaway
Notice how as you move the slider, the red, blue, and green spatial vectors pulse in and out along their fixed axes, but their sum (the black vector) maintains a perfectly constant length of **1.5** and sweeps smoothly in a circle.
""")
