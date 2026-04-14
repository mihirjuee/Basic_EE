import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="RLC Phasor Analyzer", layout="wide")

st.title("🔌 Series RLC Circuit & Phasor Diagram")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Circuit Parameters")
    v_rms = st.number_input("Source Voltage (Vrms)", value=230.0)
    freq = st.number_input("Frequency (Hz)", value=50.0)
    r = st.number_input("Resistance R (Ω)", value=100.0)
    l_mH = st.number_input("Inductance L (mH)", value=300.0)
    c_uF = st.number_input("Capacitance C (µF)", value=30.0)

# --- Calculations ---
l = l_mH / 1000
c = c_uF / 1e6
omega = 2 * np.pi * freq

xl = omega * l
xc = 1 / (omega * c)
net_x = xl - xc
z = np.sqrt(r**2 + net_x**2)
i_rms = v_rms / z
phase_rad = np.arctan2(net_x, r)
phase_deg = np.degrees(phase_rad)

# Voltages
vr = i_rms * r
vl = i_rms * xl
vc = i_rms * xc

# --- UI Layout ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📊 Analysis Results")
    st.write(f"**Inductive Reactance ($X_L$):** {xl:.2f} Ω")
    st.write(f"**Capacitive Reactance ($X_C$):** {xc:.2f} Ω")
    st.write(f"**Total Impedance ($Z$):** {z:.2f} Ω")
    st.metric("RMS Current (I)", f"{i_rms:.3f} A")
    st.metric("Phase Angle (φ)", f"{phase_deg:.2f}°")
    
    if xl > xc:
        st.warning("Circuit is Inductive (Current Lags)")
    elif xc > xl:
        st.info("Circuit is Capacitive (Current Leads)")
    else:
        st.success("Circuit is at Resonance!")

with col2:
    # --- Phasor Diagram ---
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Draw Phasors
    # VR (Reference horizontal)
    ax.quiver(0, 0, vr, 0, angles='xy', scale_units='xy', scale=1, color='red', label='VR (Resistor)')
    # VL (Up)
    ax.quiver(0, 0, 0, vl, angles='xy', scale_units='xy', scale=1, color='blue', label='VL (Inductor)')
    # VC (Down)
    ax.quiver(0, 0, 0, -vc, angles='xy', scale_units='xy', scale=1, color='green', label='VC (Capacitor)')
    # V Source (Resultant)
    ax.quiver(0, 0, vr, net_x * i_rms, angles='xy', scale_units='xy', scale=1, color='black', width=0.015, label='V Total')

    # Formatting
    limit = max(vr, vl, vc, v_rms) * 1.2
    ax.set_xlim(-limit/4, limit)
    ax.set_ylim(-limit, limit)
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.grid(True, linestyle='--')
    ax.set_title("Phasor Diagram")
    ax.legend()
    
    st.pyplot(fig)

# --- Waveform Visualization ---
st.divider()
st.subheader("📈 Time Domain Waveforms")
t = np.linspace(0, 2/freq, 500)
v_source_t = np.sqrt(2) * v_rms * np.sin(omega * t)
i_t = np.sqrt(2) * i_rms * np.sin(omega * t - phase_rad)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(t, v_source_t, label="Voltage (V)", color='black')
ax2.plot(t, i_t * (v_rms/i_rms * 0.5), label="Current (I) - Scaled", color='orange', linestyle='--')
ax2.set_xlabel("Time (s)")
ax2.legend()
st.pyplot(fig2)
