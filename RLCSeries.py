import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm

# -------------------------------
# ⚙️ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="⚡ RLC Smart Lab", layout="wide")

# -------------------------------
# 🎯 TITLE
# -------------------------------
st.title("⚡ RLC Series Circuit Interactive Lab")
st.markdown("Explore impedance, resonance, and current behavior in an RLC circuit.")

# -------------------------------
# 🔧 SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🔧 Circuit Parameters")

V_rms = st.sidebar.slider("Source Voltage (Vrms)", 10, 230, 220)
R = st.sidebar.slider("Resistance (Ω)", 1, 500, 50)
L = st.sidebar.slider("Inductance (mH)", 1, 1000, 100) / 1000
C = st.sidebar.slider("Capacitance (μF)", 1, 500, 50) / 1e6
freq = st.sidebar.number_input(
    "Frequency (Hz)",
    min_value=10.0,
    max_value=500.0,
    value=50.0,
    step=0.01
)

# -------------------------------
# 🔌 CIRCUIT DIAGRAM (FIXED)
# -------------------------------
import io

st.subheader("🔌 RLC Series Circuit Diagram")

# Create the drawing
with schemdraw.Drawing(show=False) as d:
    # Adding components in series
    d += (V1 := elm.SourceSin().label("AC Source", loc='left'))
    d += elm.Resistor().label(f"{R} Ω").right()
    d += elm.Inductor().label(f"{L*1000:.0f} mH").right()
    d += (C1 := elm.Capacitor().label(f"{C*1e6:.1f} μF").right())
    
    # Completing the loop
    d += elm.Line().down().at(C1.end)
    d += elm.Line().left().tox(V1.start)
    d += elm.Line().up().to(V1.start)

# Save to buffer
buf = io.BytesIO()
d.save(buf)
st.image(buf, caption="Dynamic Circuit Schematic", use_container_width=False)



# -------------------------------
# ⚡ CALCULATIONS
# -------------------------------
omega = 2 * np.pi * freq
XL = omega * L
XC = 1 / (omega * C)
Z = np.sqrt(R**2 + (XL - XC)**2)
phase = np.arctan((XL - XC) / R)
I = V_rms / Z

# Resonance Frequency
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# -------------------------------
# 📘 FORMULAS
# -------------------------------
st.subheader("📘 Key Formulas")

st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")
st.latex(r"X_L = \omega L,\quad X_C = \frac{1}{\omega C}")
st.latex(r"f_r = \frac{1}{2\pi\sqrt{LC}}")

st.subheader("📘 Calculations ")
col1, col2, col3 = st.columns(3)
col1.metric("Applied Frequency", f"{freq:.2f} Hz")
col2.metric("Inductive reactance (XL)", f"{XL:.2f} Ω")
col3.metric("Inductive reactance (XC)", f"{XC:.2f} Ω")

# -------------------------------
# 📊 METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Impedance (Z)", f"{Z:.2f} Ω")
col2.metric("Current (I)", f"{I:.2f} A")
col3.metric("Resonant Frequency", f"{f_res:.2f} Hz")



# -------------------------------
# 📊 PHASOR DIAGRAM (IMPROVED)
# -------------------------------
st.subheader("📊 Phasor Diagram")

fig_phasor = go.Figure()

Vr = R * I
Vl = XL * I
Vc = XC * I

# Vr
fig_phasor.add_trace(go.Scatter(
    x=[0, Vr], y=[0, 0],
    mode='lines+markers+text',
    name='Vr',
    text=["", "Vr"],
    textposition="top center",
    line=dict(width=4)
))

# Vl
fig_phasor.add_trace(go.Scatter(
    x=[0, 0], y=[0, Vl],
    mode='lines+markers+text',
    name='Vl',
    text=["", "Vl"],
    textposition="top center",
    line=dict(width=4)
))

# Vc
fig_phasor.add_trace(go.Scatter(
    x=[0, 0], y=[0, -Vc],
    mode='lines+markers+text',
    name='Vc',
    text=["", "Vc"],
    textposition="bottom center",
    line=dict(width=4)
))

# Resultant Voltage
Vx = Vr
Vy = Vl - Vc

fig_phasor.add_trace(go.Scatter(
    x=[0, Vx], y=[0, Vy],
    mode='lines+markers+text',
    name='V',
    text=["", "V"],
    textposition="top right",
    line=dict(width=4, dash='dash')
))

# Current vector (reference)
fig_phasor.add_trace(go.Scatter(
    x=[0, max(Vr, 1)], y=[0, 0],
    mode='lines+text',
    name='I',
    text=["", "I"],
    textposition="bottom center",
    line=dict(width=2, dash='dot')
))

# Arrowheads
fig_phasor.update_layout(
    annotations=[
        dict(x=Vr, y=0, ax=0, ay=0, arrowhead=3),
        dict(x=0, y=Vl, ax=0, ay=0, arrowhead=3),
        dict(x=0, y=-Vc, ax=0, ay=0, arrowhead=3),
        dict(x=Vx, y=Vy, ax=0, ay=0, arrowhead=3),
        dict(x=max(Vr, 1), y=0, ax=0, ay=0, arrowhead=2),
    ],
    height=450,
    xaxis_title="Real Axis",
    yaxis_title="Imaginary Axis"
)

st.plotly_chart(fig_phasor, use_container_width=True)

# -------------------------------
# 📈 FREQUENCY RESPONSE
# -------------------------------
st.subheader("📈 Frequency Response")

freq_range = np.linspace(10, 500, 300)
I_values = []

for f in freq_range:
    w = 2 * np.pi * f
    XL_f = w * L
    XC_f = 1 / (w * C)
    Z_f = np.sqrt(R**2 + (XL_f - XC_f)**2)
    I_values.append(V_rms / Z_f)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=freq_range,
    y=I_values,
    name="Current",
    line=dict(width=3)
))

fig.add_vline(
    x=f_res,
    line_dash="dash",
    annotation_text="Resonance"
)

fig.update_layout(
    xaxis_title="Frequency (Hz)",
    yaxis_title="Current (A)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 🔬 ADVANCED ANALYSIS
# -------------------------------
st.subheader("🔬 ")

power_factor = np.cos(phase)

st.write(f"**Power Factor:** {power_factor:.3f}")
st.write(f"**Phase Angle (rad):** {phase:.3f}")

# -------------------------------
# 🎯 INSIGHT
# -------------------------------
st.subheader("🎯 Concept Insight")

if abs(freq - f_res) < 2:
    st.success("🎯 Resonance: Circuit behaves purely resistive. Current is MAX ⚡")
elif XL > XC:
    st.info("🔄 Inductive Circuit: Current lags voltage")
else:
    st.warning("🔄 Capacitive Circuit: Current leads voltage")

# -------------------------------
# 📢 FOOTER
# -------------------------------
st.markdown("---")
st.markdown("⚡ Built for Electrical Engineering Students | Learn by Visualization 🚀")
