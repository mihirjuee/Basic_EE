import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io

# -------------------------------
# ⚙️ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Learn EE: RLC Smart Lab", layout="wide")

st.title("⚡ Series RLC Circuit Interactive Analyzer")
st.markdown("Developed for **Learn EE Interactive**. Adjust parameters to visualize impedance, resonance, and phasors.")

# -------------------------------
# 🔧 SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🔧 Circuit Parameters")

V_rms = st.sidebar.slider("Source Voltage (Vrms)", 10, 230, 220)
freq = st.sidebar.slider("Frequency (Hz)", 10, 500, 50)
R = st.sidebar.slider("Resistance (Ω)", 1, 500, 50)
L_mH = st.sidebar.slider("Inductance (mH)", 1, 1000, 100)
C_uF = st.sidebar.slider("Capacitance (μF)", 1, 500, 50)

# Unit Conversions
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

# Current and Voltages
I = V_rms / Z_mag
Vr = I * R
Vl = I * XL
Vc = I * XC

# Phase and Resonance
phi_rad = np.arctan2(X_net, R)
phi_deg = np.degrees(phi_rad)
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# -------------------------------
# 📊 TOP METRICS
# -------------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current (I)", f"{I:.2f} A")
m2.metric("Impedance (Z)", f"{Z_mag:.2f} Ω")
m3.metric("Phase Angle", f"{phi_deg:.1f}°")
m4.metric("Resonant Freq", f"{f_res:.1f} Hz")

st.divider()

# -------------------------------
# 🔌 MAIN DASHBOARD
# -------------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔌 Circuit Schematic")
    
    # Corrected Schemdraw Logic for Streamlit
    d = schemdraw.Drawing(show=False)
    
    # Adding components with updated label logic
    d += (V1 := elm.SourceSin().label("AC Source", loc='outside'))
    d += elm.Resistor().label(f"{R}Ω").right().dot()
    d += elm.Inductor().label(f"{L_mH}mH").right().dot()
    d += (C1 := elm.Capacitor().label(f"{C_uF}μF").right().dot())
    
    # Closing the loop properly
    d += elm.Line().down().at(C1.end).length(2)
    d += elm.Line().left().tox(V1.start)
    d += elm.Line().up().to(V1.start)
    
    # Render to BytesIO buffer
    buf = io.BytesIO()
    d.save(buf)
    buf.seek(0)
    st.image(buf)

    # Operating Mode Indicator
    if abs(freq - f_res) < 1.5:
        st.success("🎯 **Mode: Resonance** (Z is minimum)")
    elif XL > XC:
        st.info("🔵 **Mode: Inductive** (Current lags Voltage)")
    else:
        st.warning("🔴 **Mode: Capacitive** (Current leads Voltage)")

with col2:
    st.subheader("📈 Phasor Diagram")
    
    fig = go.Figure()

    # Resistive Component (Ref)
    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, 0], mode='lines+markers', name='Vr (Resistive)', line=dict(color='green', width=4)))
    # Inductive Component (+90)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, Vl], mode='lines+markers', name='Vl (Inductive)', line=dict(color='blue', width=4)))
    # Capacitive Component (-90)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, -Vc], mode='lines+markers', name='Vc (Capacitive)', line=dict(color='red', width=4)))
    # Net Voltage (Resultant)
    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, X_net*I], mode='lines+markers', name='V Total', line=dict(color='black', width=3, dash='dash')))

    # Axis Formatting to keep the center at 0,0
    limit = max(Vr, Vl, Vc) * 1.2
    fig.update_layout(
        xaxis=dict(title="Real (V)", range=[-limit/4, limit], zeroline=True),
        yaxis=dict(title="Imaginary (V)", range=[-limit, limit], zeroline=True),
        height=450,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 📚 THEORY SECTION
# -------------------------------
with st.expander("📘 Mathematical Derivations (LaTeX)"):
    st.write("The total impedance $Z$ in a series RLC circuit is given by:")
    st.latex(r"Z = R + j\left(\omega L - \frac{1}{\omega C}\right)")
    st.write("The magnitude and phase angle:")
    st.latex(r"|Z| = \sqrt{R^2 + (X_L - X_C)^2} \quad \angle \theta = \tan^{-1}\left(\frac{X_L - X_C}{R}\right)")
