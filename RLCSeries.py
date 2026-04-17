import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io

# --- Page Configuration ---
st.set_page_config(page_title="Learn EE Interactive: RLC Lab", layout="wide")

st.title("⚡ Series RLC Circuit Interactive Analyzer")
st.write("Welcome to the **Learn EE Interactive** virtual lab. Adjust parameters to visualize resonance and phasors.")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 Circuit Parameters")
V_rms = st.sidebar.slider("Source Voltage (Vrms)", 10, 230, 220)
freq = st.sidebar.slider("Frequency (Hz)", 10, 500, 50)
R = st.sidebar.slider("Resistance (Ω)", 1, 500, 50)
L_mH = st.sidebar.slider("Inductance (mH)", 1, 1000, 100)
C_uF = st.sidebar.slider("Capacitance (μF)", 1, 500, 50)

# Convert units
L = L_mH / 1000
C = C_uF / 1e6

# --- Calculations ---
omega = 2 * np.pi * freq
XL = omega * L
XC = 1 / (omega * C)
X_net = XL - XC
Z_mag = np.sqrt(R**2 + X_net**2)
phi_rad = np.arctan2(X_net, R)
phi_deg = np.degrees(phi_rad)
I_rms = V_rms / Z_mag

# Component Voltages
Vr = I_rms * R
Vl = I_rms * XL
Vc = I_rms * XC
f_res = 1 / (2 * np.pi * np.sqrt(L * C))

# --- Layout: Top Metrics ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current (I)", f"{I_rms:.2f} A")
m2.metric("Impedance (Z)", f"{Z_mag:.2f} Ω")
m3.metric("Phase Angle", f"{phi_deg:.1f}°")
m4.metric("Resonant Freq", f"{f_res:.1f} Hz")

st.divider()

# --- Main Content: Schematic and Phasor ---
left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.subheader("🔌 Circuit Schematic")
    d = schemdraw.Drawing(show=False)
    d += (V1 := elm.SourceSin().label("AC Source", loc='outside'))
    d += elm.Resistor().label(f"{R}Ω").right().dot()
    d += elm.Inductor().label(f"{L_mH}mH").right().dot()
    d += (C1 := elm.Capacitor().label(f"{C_uF}μF").right().dot())
    
    # Complete loop
    d += elm.Line().down().at(C1.end).length(2)
    d += elm.Line().left().tox(V1.start)
    d += elm.Line().up().to(V1.start)
    
    buf = io.BytesIO()
    d.save(buf)
    st.image(buf)
    
    st.info(f"**Operating Mode:** {'Resonance' if abs(freq-f_res)<1 else 'Inductive' if XL > XC else 'Capacitive'}")

with right_col:
    st.subheader("📈 Phasor Diagram (Voltages)")
    
    fig = go.Figure()
    # Reference Vr (along X-axis)
    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, 0], mode='lines+markers', name='Vr (Resistive)', line=dict(color='green', width=4)))
    # Vl (Leading 90)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, Vl], mode='lines+markers', name='Vl (Inductive)', line=dict(color='blue', width=4)))
    # Vc (Lagging 90)
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, -Vc], mode='lines+markers', name='Vc (Capacitive)', line=dict(color='red', width=4)))
    # Total V_source
    fig.add_trace(go.Scatter(x=[0, Vr], y=[0, X_net*I_rms], mode='lines+markers', name='V Total', line=dict(color='black', width=3, dash='dash')))

    fig.update_layout(
        xaxis=dict(title="Real (V)", zeroline=True, range=[-max(Vl, Vc, Vr), max(Vl, Vc, Vr)*1.2]),
        yaxis=dict(title="Imaginary (V)", zeroline=True, range=[-max(Vl, Vc, Vr), max(Vl, Vc, Vr)*1.2]),
        height=450,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Bottom Section: Theory ---
with st.expander("📚 View Mathematical Formulas"):
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")
    st.latex(r"X_L = 2\pi f L \quad | \quad X_C = \frac{1}{2\pi f C}")
    st.latex(r"\theta = \tan^{-1}\left(\frac{X_L - X_C}{R}\right)")
