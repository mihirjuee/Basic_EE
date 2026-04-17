import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io

# -------------------------------
# ⚙️ PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Learn EE: RLC Smart Lab", layout="wide")

st.title("⚡ Series RLC Circuit Interactive Analyzer")
st.markdown("Developed for **Learn EE Interactive**. Adjust sliders to explore resonance and phasors.")

# -------------------------------
# 🔧 SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🔧 Circuit Parameters")

V_rms = st.sidebar.slider("Source Voltage (Vrms)", 10, 230, 220)
freq = st.sidebar.slider("Frequency (Hz)", 10, 500, 50)
R = st.sidebar.slider("Resistance (Ω)", 1, 500, 50)
L_mH = st.sidebar.slider("Inductance (mH)", 1, 1000, 100)
C_uF = st.sidebar.slider("Capacitance (μF)", 1, 500, 50)

# Convert units
L = L_mH / 1000
C = C_uF / 1e6

# -------------------------------
# ⚡ ELECTRICAL CALCULATIONS
# -------------------------------
omega = 2 * np.pi * freq
XL = omega * L
XC = 1 / (omega * C)
X_net = XL - XC
Z_mag = np.sqrt(R**2 + X_net**2)

# Ohm's Law
I = V_rms / Z_mag
Vr = I * R
Vl = I * XL
Vc = I * XC

# Phase and Resonance
phi_deg = np.degrees(np.arctan2(X_net, R))
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# -------------------------------
# 📊 TOP METRICS BAR
# -------------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current (I)", f"{I:.2f} A")
m2.metric("Impedance (Z)", f"{Z_mag:.2f} Ω")
m3.metric("Phase Angle", f"{phi_deg:.1f}°")
m4.metric("Resonant Freq", f"{f_res:.1f} Hz")

st.divider()

# -------------------------------
# 🔌 MAIN CONTENT: SCHEMATIC & PHASOR
# -------------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔌 Circuit Schematic")

    d = schemdraw.Drawing(show=False)

    # ✔️ SAFE labels (this fixes your error)
    d += elm.SourceSin().label("AC Source", loc="right")
    d += elm.Resistor().right().label(f"{R} Ω", loc="right")
    d += elm.Inductor().right().label(f"{L_mH} mH", loc="right")
    d += elm.Capacitor().right().label(f"{C_uF} μF", loc="right")

    # Return path (safe loop)
    d += elm.Line().down().length(2)
    d += elm.Ground()
    d += elm.Line().left().length(6)
    d += elm.Line().up()

    # Render safely
    buf = io.BytesIO()
    d.save(buf)
    buf.seek(0)

    st.image(buf)

with col2:
    st.subheader("📈 Phasor Diagram")
    
    fig = go.Figure()

    # Vr (Reference along X-axis)
    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, 0], mode='lines+markers', name='Vr (Resistive)', line=dict(color='green', width=4)))
    
    # Vl (+90 degrees)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, Vl], mode='lines+markers', name='Vl (Inductive)', line=dict(color='blue', width=4)))
    
    # Vc (-90 degrees)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, -Vc], mode='lines+markers', name='Vc (Capacitive)', line=dict(color='red', width=4)))
    
    # Total V Source (Resultant)
    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, X_net*I], mode='lines+markers', name='V Total', line=dict(color='black', width=3, dash='dash')))

    # Keep diagram centered and scaled
    limit = max(Vr, Vl, Vc) * 1.2
    fig.update_layout(
        xaxis=dict(title="Real (V)", range=[-limit/3, limit], zeroline=True),
        yaxis=dict(title="Imaginary (V)", range=[-limit, limit], zeroline=True),
        height=450,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 📚 THEORY SECTION
# -------------------------------
with st.expander("📘 Educational Resources (LaTeX)"):
    st.write("In a series RLC circuit, total impedance is represented as:")
    st.latex(r"Z = R + j(X_L - X_C)")
    st.write("The resonance occurs when $X_L = X_C$, leading to minimum impedance:")
    st.latex(r"f_r = \frac{1}{2\pi\sqrt{LC}}")
