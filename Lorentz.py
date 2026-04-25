import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE =================
st.set_page_config(page_title="DC Motor Virtual Lab", layout="wide")

st.title("⚡ DC Motor Virtual Lab (Industry Level Simulation)")

st.markdown("""
### 🔹 Real DC Motor Model
- Torque production
- Back EMF effect
- Speed dynamics
- Load interaction
""")

# ================= INPUT =================
st.sidebar.header("🔧 Motor Parameters")

V = st.sidebar.slider("Supply Voltage (V)", 0.0, 240.0, 120.0)
R = st.sidebar.slider("Armature Resistance (Ω)", 0.1, 5.0, 1.0)
k = st.sidebar.slider("Motor Constant (kΦ)", 0.1, 2.0, 0.8)
J = st.sidebar.slider("Inertia (J)", 0.1, 5.0, 1.0)
Bf = st.sidebar.slider("Friction (B)", 0.0, 1.0, 0.1)
TL = st.sidebar.slider("Load Torque (Nm)", 0.0, 10.0, 2.0)

# ================= INITIAL CONDITIONS =================
dt = 0.05
steps = 200

omega = 0.0
history_omega = []
history_torque = []
history_current = []

# ================= SIMULATION =================
placeholder = st.empty()

if st.button("▶ Start Motor Simulation"):

    for t in range(steps):

        # Back EMF
        Eb = k * omega

        # Armature current
        Ia = (V - Eb) / R

        # Electromagnetic torque
        Te = k * Ia

        # Motion equation
        domega = (Te - TL - Bf * omega) / J

        omega += domega * dt

        # store
        history_omega.append(omega)
        history_torque.append(Te)
        history_current.append(Ia)

        # ================= PLOT =================
        fig = go.Figure()

        fig.add_trace(go.Scatter(y=history_omega, name="Speed (ω)", line=dict(color="blue")))
        fig.add_trace(go.Scatter(y=history_torque, name="Torque (Te)", line=dict(color="red")))
        fig.add_trace(go.Scatter(y=history_current, name="Current (Ia)", line=dict(color="green")))

        fig.update_layout(
            title="Motor Dynamic Response",
            xaxis_title="Time Step",
            yaxis_title="Value",
            height=500
        )

        placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(0.03)

# ================= STEADY STATE =================
st.subheader("📊 Final Operating Point")

col1, col2, col3 = st.columns(3)

col1.metric("Speed (ω)", f"{omega:.2f} rad/s")
col2.metric("Current (Ia)", f"{Ia:.2f} A")
col3.metric("Back EMF (Eb)", f"{Eb:.2f} V")

# ================= PHYSICAL INSIGHT =================
st.subheader("💡 Physical Insight")

st.markdown("""
- At start: ω = 0 → high current → high torque  
- As speed increases → back EMF increases → current reduces  
- Motor reaches equilibrium when:
  - Torque = Load Torque + Losses
""")
