import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- Page Config ---
st.set_page_config(page_title="RLC Circuit Pro", layout="wide")

# --- Schemdraw Circuit ---
def draw_schematic(R, L, C, V):
    d = schemdraw.Drawing()
    d.config(unit=3)

    # Source
    V1 = d.add(elm.SourceSin().label(f'{V}V'))

    # Resistor
    d.add(elm.Resistor().right().label(f'R\n{R}Ω'))

    # Inductor
    d.add(elm.Inductor().right().label(f'L\n{L*1000:.0f} mH'))

    # Capacitor
    d.add(elm.Capacitor().right().label(f'C\n{C*1e6:.0f} µF'))

    # Close loop
    d.add(elm.Line().down())
    d.add(elm.Line().left().to(V1.start))
    d.add(elm.Line().up())

    return d

# --- Phasor Diagram ---
def draw_phasors(vr, vl, vc, vs, phase_deg):
    fig, ax = plt.subplots(figsize=(6, 6))

    max_val = max(vr, vl, vc, vs) * 1.3

    ax.axhline(0)
    ax.axvline(0)

    # VR
    ax.quiver(0, 0, vr, 0, angles='xy', scale_units='xy', scale=1)
    # VL
    ax.quiver(0, 0, 0, vl, angles='xy', scale_units='xy', scale=1)
    # VC
    ax.quiver(0, 0, 0, -vc, angles='xy', scale_units='xy', scale=1)
    # VS
    ax.quiver(0, 0, vr, (vl-vc), angles='xy', scale_units='xy', scale=1)

    ax.set_xlim(-max_val/4, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_title(f"Phasor Diagram (Phase: {phase_deg:.2f}°)")
    ax.grid()

    return fig

# --- Title ---
st.title("🔌 Series RLC Analyzer & Phasor Generator")

# --- Sidebar ---
with st.sidebar:
    st.header("Input Parameters")

    V_rms = st.slider("Voltage (Vrms)", 10, 500, 230)
    freq = st.slider("Frequency (Hz)", 1, 200, 50)

    R = st.number_input("Resistance (Ω)", value=100.0)
    L_mH = st.number_input("Inductance (mH)", value=300.0)
    C_uF = st.number_input("Capacitance (µF)", value=30.0)

# --- Physics ---
L = L_mH / 1000
C = C_uF / 1e6

omega = 2 * np.pi * freq

XL = omega * L
XC = 1 / (omega * C)
X = XL - XC

Z = np.sqrt(R**2 + X**2)
I = V_rms / Z

phase = np.arctan2(X, R)
phase_deg = np.degrees(phase)

VR = I * R
VL = I * XL
VC = I * XC

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🏠 Circuit", "📈 Phasor", "🧠 Math"])

# --- Tab 1 ---
with tab1:
    st.subheader("Circuit Diagram")
    st.pyplot(draw_schematic(R, L, C, V_rms))

    c1, c2, c3 = st.columns(3)
    c1.metric("Impedance", f"{Z:.2f} Ω")
    c2.metric("Current", f"{I:.3f} A")
    c3.metric("Phase Angle", f"{phase_deg:.2f}°")

# --- Tab 2 ---
with tab2:
    st.subheader("Phasor Diagram")
    st.pyplot(draw_phasors(VR, VL, VC, V_rms, phase_deg))

    if XL > XC:
        st.info("Inductive Circuit → Voltage leads current")
    elif XC > XL:
        st.info("Capacitive Circuit → Current leads voltage")
    else:
        st.success("Resonance → Purely resistive")

# --- Tab 3 ---
with tab3:
    st.subheader("Equations")

    st.latex(r"X_L = 2\pi f L")
    st.latex(r"X_C = \frac{1}{2\pi f C}")
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")

    st.write("### Values")
    st.write(f"XL = {XL:.2f} Ω")
    st.write(f"XC = {XC:.2f} Ω")
    st.write(f"Z = {Z:.2f} Ω")

    st.write("### Voltages")
    st.write(f"VR = {VR:.2f} V")
    st.write(f"VL = {VL:.2f} V")
    st.write(f"VC = {VC:.2f} V")
