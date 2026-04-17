import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Learn EE: RLC Series Lab", layout="wide")

st.title("⚡ RLC Series Circuit Interactive Lab")
st.write("Adjust the parameters to see how the circuit behaves at different frequencies.")

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")
V_rms = st.sidebar.slider("Source Voltage (Vrms)", 10, 230, 220)
R = st.sidebar.slider("Resistance (Ω)", 1, 500, 50)
L = st.sidebar.slider("Inductance (mH)", 1, 1000, 100) / 1000 # Convert to H
C = st.sidebar.slider("Capacitance (μF)", 1, 500, 50) / 1e6    # Convert to F
freq = st.sidebar.slider("Frequency (Hz)", 10, 500, 50)

# --- Calculations ---
omega = 2 * np.pi * freq
XL = omega * L
XC = 1 / (omega * C)
Z_mag = np.sqrt(R**2 + (XL - XC)**2)
phase_rad = np.arctan((XL - XC) / R)
I_rms = V_rms / Z_mag

# Resonance Freq
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# --- Dashboard Layout ---
col1, col2, col3 = st.columns(3)
col1.metric("Impedance (Z)", f"{Z_mag:.2f} Ω")
col2.metric("Current (I)", f"{I_rms:.2f} A")
col3.metric("Resonant Freq", f"{f_res:.2f} Hz")

# --- Phasor Diagram ---
st.subheader("📊 Live Phasor Diagram")
# Creating Phasor vectors
fig_phasor = go.Figure()
fig_phasor.add_trace(go.Scatter(x=[0, R*I_rms], y=[0, 0], name='Vr (Resistive)', line=dict(color='green', width=4)))
fig_phasor.add_trace(go.Scatter(x=[0, 0], y=[0, XL*I_rms], name='Vl (Inductive)', line=dict(color='blue', width=4)))
fig_phasor.add_trace(go.Scatter(x=[0, 0], y=[0, -XC*I_rms], name='Vc (Capacitive)', line=dict(color='red', width=4)))

fig_phasor.update_layout(xaxis=dict(range=[-100, 300]), yaxis=dict(range=[-300, 300]), height=400)
st.plotly_chart(fig_phasor, use_container_width=True)

# --- Educational Insight ---
if abs(freq - f_res) < 2:
    st.success("🎯 **RESONANCE ACHIEVED!** The circuit is purely resistive. Current is at its maximum.")
elif XL > XC:
    st.info("🔄 **Inductive Nature:** The current lags the voltage.")
else:
    st.warning("🔄 **Capacitive Nature:** The current leads the voltage.")
