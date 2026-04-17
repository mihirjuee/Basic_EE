import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io

# -------------------------------
# ⚙️ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="⚡ RLC Smart Lab", layout="wide")

st.title("⚡ Series RLC Circuit Interactive Analyzer")
st.markdown("Adjust parameters to visualize impedance, resonance, and phasors.")

# -------------------------------
# 🔧 INPUTS
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
# ⚡ CALCULATIONS
# -------------------------------
omega = 2 * np.pi * freq
XL = omega * L
XC = 1 / (omega * C)

X_net = XL - XC
Z = np.sqrt(R**2 + X_net**2)

phi = np.arctan2(X_net, R)
phi_deg = np.degrees(phi)

I = V_rms / Z

Vr = I * R
Vl = I * XL
Vc = I * XC

f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# -------------------------------
# 📊 METRICS
# -------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current (A)", f"{I:.2f}")
c2.metric("Impedance (Ω)", f"{Z:.2f}")
c3.metric("Phase (°)", f"{phi_deg:.1f}")
c4.metric("Resonant Freq (Hz)", f"{f_res:.1f}")

st.divider()

# -------------------------------
# 🔌 CIRCUIT DIAGRAM (FIXED 100%)
# -------------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔌 Circuit Schematic")

    d = schemdraw.Drawing(show=False)

    # IMPORTANT FIX:
    # Always use explicit loc="right" to avoid Schemdraw errors

    d += elm.SourceSin().label("AC Source", loc="right")
    d += elm.Resistor().label(f"{R} Ω", loc="right")
    d += elm.Inductor().label(f"{L_mH} mH", loc="right")
    d += elm.Capacitor().label(f"{C_uF} μF", loc="right")

    # Safe loop closure (no coordinates, no .start/.tox)
    d += elm.Line().down().length(2)
    d += elm.Ground()
    d += elm.Line().left().length(6)
    d += elm.Line().up()

    # Render safely
    buf = io.BytesIO()
    d.save(buf)
    buf.seek(0)

    st.image(buf)

    # Operating mode
    if abs(freq - f_res) < 1:
        mode = "⚡ Resonance"
    elif XL > XC:
        mode = "🔵 Inductive"
    else:
        mode = "🔴 Capacitive"

    st.info(f"Operating Mode: {mode}")

# -------------------------------
# 📈 PHASOR DIAGRAM
# -------------------------------
with col2:
    st.subheader("📈 Phasor Diagram")

    fig = go.Figure()

    # Vr
    fig.add_trace(go.Scatter(
        x=[0, Vr], y=[0, 0],
        mode='lines+markers',
        name='Vr',
        line=dict(color='green', width=4)
    ))

    # Vl
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[0, Vl],
        mode='lines+markers',
        name='Vl',
        line=dict(color='blue', width=4)
    ))

    # Vc
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[0, -Vc],
        mode='lines+markers',
        name='Vc',
        line=dict(color='red', width=4)
    ))

    # Resultant
    Vx = Vr
    Vy = Vl - Vc

    fig.add_trace(go.Scatter(
        x=[0, Vx], y=[0, Vy],
        mode='lines+markers',
        name='V Total',
        line=dict(color='black', width=3, dash='dash')
    ))

    # Current reference
    fig.add_trace(go.Scatter(
        x=[0, Vr], y=[0, 0],
        mode='lines',
        name='I (Reference)',
        line=dict(color='orange', width=2, dash='dot')
    ))

    fig.update_layout(
        height=450,
        xaxis_title="Real Axis (V)",
        yaxis_title="Imaginary Axis (V)",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 📚 FORMULAS
# -------------------------------
with st.expander("📘 Formulas"):
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")
    st.latex(r"X_L = 2\pi f L")
    st.latex(r"X_C = \frac{1}{2\pi f C}")
    st.latex(r"f_r = \frac{1}{2\pi\sqrt{LC}}")
    st.latex(r"\phi = \tan^{-1}\left(\frac{X_L - X_C}{R}\right)")
