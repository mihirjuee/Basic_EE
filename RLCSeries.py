import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import io

# --- Page Config ---
st.set_page_config(page_title="⚡ Full AC Lab", layout="wide")

# --- Title ---
st.title("⚡ Full AC Circuits Virtual Lab")

# ------------------ SCHEMATIC ------------------
import os

def draw_circuit(R, L, C, V):
    d = schemdraw.Drawing()
    d.config(unit=3)

    V1 = d.add(elm.SourceSin().label(f'{V}V'))
    d.add(elm.Resistor().right().label(f'R\n{R}Ω'))
    d.add(elm.Inductor().right().label(f'L\n{L*1000:.0f} mH'))
    d.add(elm.Capacitor().right().label(f'C\n{C*1e6:.0f} µF'))

    d.add(elm.Line().down())
    d.add(elm.Line().left().to(V1.start))
    d.add(elm.Line().up())

    # 👉 Save to file (SAFE METHOD)
    filename = "circuit.png"
    d.save(filename)

    return filename

# ------------------ PHASOR ------------------
def phasor_plot(VR, VL, VC, V):
    fig, ax = plt.subplots(figsize=(5,5))

    ax.axhline(0)
    ax.axvline(0)

    ax.quiver(0,0,VR,0, angles='xy', scale_units='xy', scale=1, label='Vr')
    ax.quiver(0,0,0,VL, angles='xy', scale_units='xy', scale=1, label='Vl')
    ax.quiver(0,0,0,-VC, angles='xy', scale_units='xy', scale=1, label='Vc')
    ax.quiver(0,0,VR,(VL-VC), angles='xy', scale_units='xy', scale=1, label='Vs')

    ax.set_title("Phasor Diagram")
    ax.grid()
    ax.legend()

    return fig

# ------------------ POWER TRIANGLE ------------------
def power_triangle(V, I, phi):
    P = V * I * np.cos(phi)
    Q = V * I * np.sin(phi)
    S = V * I

    fig, ax = plt.subplots()

    ax.plot([0, P], [0, 0])
    ax.plot([P, P], [0, Q])
    ax.plot([0, P], [0, Q])

    ax.set_title("Power Triangle")
    ax.set_xlabel("Real Power (P)")
    ax.set_ylabel("Reactive Power (Q)")
    ax.grid()

    return fig, P, Q, S

# ------------------ FREQUENCY SWEEP ------------------
def freq_response(R, L, C):
    f = np.linspace(1, 500, 500)
    w = 2*np.pi*f

    XL = w * L
    XC = 1/(w*C)
    Z = np.sqrt(R**2 + (XL-XC)**2)
    I = 1/Z

    fig, ax = plt.subplots()
    ax.plot(f, I)
    ax.set_title("Frequency Response (Resonance Curve)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Current (A)")
    ax.grid()

    return fig

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("Controls")

    V = st.slider("Voltage (Vrms)", 10, 500, 230)
    f = st.slider("Frequency (Hz)", 1, 200, 50)

    R = st.number_input("Resistance (Ω)", value=100.0)
    L_mH = st.number_input("Inductance (mH)", value=200.0)
    C_uF = st.number_input("Capacitance (µF)", value=50.0)

# --- Convert Units ---
L = L_mH / 1000
C = C_uF / 1e6

w = 2*np.pi*f

XL = w * L
XC = 1/(w*C)
X = XL - XC

Z = np.sqrt(R**2 + X**2)
I = V / Z

phi = np.arctan2(X, R)

VR = I * R
VL = I * XL
VC = I * XC

# ------------------ TABS ------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🔌 Circuit", "📈 Phasor", "⚡ Power", "📊 Resonance", "🧠 Theory"]
)

# --- Circuit ---
with tab1:
    st.subheader("Circuit Diagram")
    st.image(draw_circuit(R, L, C, V))

    col1, col2, col3 = st.columns(3)
    col1.metric("Impedance", f"{Z:.2f} Ω")
    col2.metric("Current", f"{I:.3f} A")
    col3.metric("Phase Angle", f"{np.degrees(phi):.2f}°")

# --- Phasor ---
with tab2:
    st.subheader("Phasor Diagram")
    st.pyplot(phasor_plot(VR, VL, VC, V))

# --- Power ---
with tab3:
    st.subheader("Power Triangle")
    fig, P, Q, S = power_triangle(V, I, phi)
    st.pyplot(fig)

    st.write(f"Real Power (P): {P:.2f} W")
    st.write(f"Reactive Power (Q): {Q:.2f} VAR")
    st.write(f"Apparent Power (S): {S:.2f} VA")

# --- Resonance ---
with tab4:
    st.subheader("Frequency Sweep")
    st.pyplot(freq_response(R, L, C))

# --- Theory ---
with tab5:
    st.latex(r"X_L = 2\pi f L")
    st.latex(r"X_C = \frac{1}{2\pi f C}")
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")
    st.latex(r"P = VI\cos\phi")
    st.latex(r"Q = VI\sin\phi")
    st.latex(r"S = VI")
