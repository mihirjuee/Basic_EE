import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io
from PIL import Image

# -------------------------------
# ⚙️ PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Learn EE: RLC Smart Lab", layout="wide")

st.title("⚡ Series RLC Circuit Interactive Analyzer")
st.markdown("Developed for **Learn EE Interactive**")

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

Z_mag = np.sqrt(R**2 + X_net**2)

I = V_rms / Z_mag
Vr = I * R
Vl = I * XL
Vc = I * XC

phi_deg = np.degrees(np.arctan2(X_net, R))
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# -------------------------------
# 📊 METRICS
# -------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current (A)", f"{I:.2f}")
c2.metric("Impedance (Ω)", f"{Z_mag:.2f}")
c3.metric("Phase (°)", f"{phi_deg:.1f}")
c4.metric("Resonant Freq", f"{f_res:.1f}")

st.divider()

# -------------------------------
# 🔌 CIRCUIT (FIXED PROPER LOOP)
# -------------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔌 Circuit Schematic")

    d = schemdraw.Drawing(show=False)

    # ✔️ Proper closed-loop RLC (NO loc issues, NO crashes)

    d += elm.SourceSin().label("AC Source", loc="left")
    d += elm.Resistor().right().label(f"{R} Ω")
    d += elm.Inductor().right().label(f"{L_mH} mH")
    d += elm.Capacitor().right().label(f"{C_uF} μF")

    # Return path (stable loop)
    d += elm.Line().down().length(2)
    d += elm.Ground()
    d += elm.Line().left().length(6)
    d += elm.Line().up()

    # Convert to image safely (IMPORTANT FIX)
    buf = io.BytesIO()
    d.save(buf)
    buf.seek(0)

    img = Image.open(buf)
    st.image(img)

# -------------------------------
# 📈 PHASOR
# -------------------------------
with col2:
    st.subheader("📈 Phasor Diagram")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, 0],
                             mode='lines+markers',
                             name='Vr',
                             line=dict(color='green', width=4)))

    fig.add_trace(go.Scatter(x=[0, 0], y=[0, Vl],
                             mode='lines+markers',
                             name='Vl',
                             line=dict(color='blue', width=4)))

    fig.add_trace(go.Scatter(x=[0, 0], y=[0, -Vc],
                             mode='lines+markers',
                             name='Vc',
                             line=dict(color='red', width=4)))

    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, X_net * I],
                             mode='lines+markers',
                             name='V total',
                             line=dict(color='black', width=3, dash='dash')))

    limit = max(Vr, Vl, Vc) * 1.2

    fig.update_layout(
        xaxis=dict(title="Real (V)", range=[-limit, limit]),
        yaxis=dict(title="Imaginary (V)", range=[-limit, limit]),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 📚 THEORY
# -------------------------------
with st.expander("📘 Theory"):
    st.latex(r"Z = R + j(X_L - X_C)")
    st.latex(r"X_L = 2\pi f L")
    st.latex(r"X_C = \frac{1}{2\pi f C}")
    st.latex(r"f_r = \frac{1}{2\pi\sqrt{LC}}")
