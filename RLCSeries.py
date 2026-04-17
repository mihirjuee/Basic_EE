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
st.set_page_config(page_title="Learn EE: RLC Smart Lab", layout="wide", page_icon="logo.png")

# Custom CSS to make it look like a professional dashboard
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Series RLC Circuit Interactive Analyzer")
st.markdown("### Virtual Laboratory for **Learn EE Interactive**")

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
L, C = L_mH / 1000, C_uF / 1e6

# -------------------------------
# ⚡ CALCULATIONS
# -------------------------------
omega = 2 * np.pi * freq
XL, XC = omega * L, 1 / (omega * C)
X_net = XL - XC
Z_mag = np.sqrt(R**2 + X_net**2)
I = V_rms / Z_mag
Vr, Vl, Vc = I * R, I * XL, I * XC
phi_deg = np.degrees(np.arctan2(X_net, R))
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# -------------------------------
# 📊 METRICS SECTION
# -------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current (I)", f"{I:.2f} A")
c2.metric("Impedance (Z)", f"{Z_mag:.2f} Ω")
c3.metric("Phase Angle", f"{phi_deg:.1f}°")
c4.metric("Resonant Freq", f"{f_res:.1f} Hz")

st.divider()

# -------------------------------
# 🔌 MAIN VISUALIZATION
# -------------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🔌 Circuit Schematic")
    d = schemdraw.Drawing(show=False)
    # Using specific locs and labels to ensure stability
    d += (V1 := elm.SourceSin().label("Source", loc="left"))
    d += elm.Resistor().right().label(f"{R}Ω")
    d += elm.Inductor().right().label(f"{L_mH}mH")
    d += (C1 := elm.Capacitor().right().label(f"{C_uF}μF"))
    
    # Return path
    d += elm.Line().down().at(C1.end).length(3)
    d += elm.Line().left().tox(V1.start)
    d += elm.Line().up().to(V1.start)

    buf = io.BytesIO()
    d.save(buf)
    buf.seek(0)
    st.image(Image.open(buf), use_container_width=True)

    # Operating Status Box
    if abs(freq - f_res) < 1.5:
        st.success("🎯 **Condition: RESONANCE** (I is max, Z is min)")
    elif XL > XC:
        st.info("🔵 **Condition: INDUCTIVE** (Current lags Voltage)")
    else:
        st.warning("🔴 **Condition: CAPACITIVE** (Current leads Voltage)")

with col2:
    tab1, tab2 = st.tabs(["📈 Phasor Diagram", "📐 Impedance Triangle"])
    
    with tab1:
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=[0, Vr], y=[0, 0], mode='lines+markers', name='Vr', line=dict(color='green', width=4)))
        fig_p.add_trace(go.Scatter(x=[0, 0], y=[0, Vl], mode='lines+markers', name='Vl', line=dict(color='blue', width=4)))
        fig_p.add_trace(go.Scatter(x=[0, 0], y=[0, -Vc], mode='lines+markers', name='Vc', line=dict(color='red', width=4)))
        fig_p.add_trace(go.Scatter(x=[0, I], y=[0, 0], mode='lines+markers', name='I', line=dict(color='orange', width=4)))
        fig_p.add_trace(go.Scatter(x=[0, Vr], y=[0, X_net*I], mode='lines+markers', name='V Total', line=dict(color='black', width=3, dash='dash')))
          
limit = max(Vr, Vl, Vc) * 1.2
fig_p.update_layout(xaxis=dict(range=[-limit/4, limit]), yaxis=dict(range=[-limit, limit]), height=450)
st.plotly_chart(fig_p, use_container_width=True)
        with tab2:
        # Drawing the Impedance Triangle (R, X, Z)
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(x=[0, R], y=[0, 0], mode='lines+markers', name='Resistance (R)', line=dict(color='green', width=5)))
        fig_t.add_trace(go.Scatter(x=[R, R], y=[0, X_net], mode='lines+markers', name='Reactance (X_net)', line=dict(color='orange', width=5)))
        fig_t.add_trace(go.Scatter(x=[0, R], y=[0, X_net], mode='lines+markers', name='Impedance (Z)', line=dict(color='purple', width=4, dash='dot')))
        
        fig_t.update_layout(title="Impedance Triangle (R-X-Z)", height=450)
        st.plotly_chart(fig_t, use_container_width=True)

# -------------------------------
# 📚 THEORY SECTION
# -------------------------------
with st.expander("📘 Detailed Theory and Equations"):
    st.markdown("### Fundamental Relationships")
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2} \angle \tan^{-1}\left(\frac{X_L - X_C}{R}\right)")
    col_a, col_b = st.columns(2)
    col_a.latex(r"X_L = 2\pi f L")
    col_b.latex(r"X_C = \frac{1}{2\pi f C}")
    st.markdown("At **Resonance**:")
    st.latex(r"f_r = \frac{1}{2\pi\sqrt{LC}} \implies X_L = X_C \implies Z = R")
