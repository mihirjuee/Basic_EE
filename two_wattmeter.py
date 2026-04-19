# 🔥 MUST BE FIRST
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Two Wattmeter Lab",
    page_icon="⚡",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ Learn EE")

    V_supply = st.slider("Line Voltage (V)", 100, 440, 400)
    V_rated = st.slider("Rated Voltage (V)", 200, 440, 400)
    I_rated = st.slider("Rated Current (A)", 1, 50, 10)
    P_rated = st.slider("Rated Power (kW)", 1.0, 50.0, 5.0)

# --- CALCULATIONS ---
pf = (P_rated * 1000) / (np.sqrt(3) * V_rated * I_rated)
pf = np.clip(pf, 0, 1)

I_actual = I_rated * (V_supply / V_rated)
phi = np.arccos(pf)

W1 = V_supply * I_actual * np.cos(np.radians(30) - phi)
W2 = V_supply * I_actual * np.cos(np.radians(30) + phi)
P_total = W1 + W2

# --- DRAWING FUNCTION (VERSION SAFE) ---
def get_circuit():
    d = schemdraw.Drawing(unit=2)

    # ========= R PHASE =========
    d += elm.Line().right().label("R", loc='left')
    d += elm.Inductor(loops=3).label("CC1", loc='bottom')

    # PC1 branch (R-Y)
    d.push()
    d += elm.Line().up()
    d += elm.Inductor(loops=7).label("PC1", loc='right')
    d += elm.Line().right(2)
    d.pop()

    d += elm.Line().right()
    d += elm.Resistor().down().label("Zr")

    # ========= Y PHASE =========
    d += elm.Line().left(3)
    d += elm.Line().down(2)

    d += elm.Line().right().label("Y", loc='left')

    d.push()
    d += elm.Line().up(2)   # connection point for PC
    d.pop()

    d += elm.Line().right()
    d += elm.Resistor().down().label("Zy")

    # ========= B PHASE =========
    d += elm.Line().left(3)
    d += elm.Line().down(2)

    d += elm.Line().right().label("B", loc='left')
    d += elm.Inductor(loops=3).label("CC2", loc='bottom')

    # PC2 branch (B-Y)
    d.push()
    d += elm.Line().down()
    d += elm.Inductor(loops=7).label("PC2", loc='right')
    d += elm.Line().right(2)
    d.pop()

    d += elm.Line().right()
    d += elm.Resistor().down().label("Zb")

    # ========= STAR CONNECTION =========
    d += elm.Line().left(2)
    d += elm.Line().down()
    neutral = elm.Dot().label("N", loc='bottom')
    d += neutral

    # Connect three loads to neutral (visually aligned)
    d.push()
    d += elm.Line().left(2)
    d.pop()

    return d

# --- UI ---
st.title("⚡ Two-Wattmeter Method (Version-Safe)")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🔌 Circuit Diagram")
    d = get_circuit()
    fig = d.draw()
    st.pyplot(fig)
    plt.clf()

with col2:
    st.subheader("📊 Results")

    st.metric("Line Current", f"{I_actual:.2f} A")
    st.metric("W1", f"{W1:.1f} W")
    st.metric("W2", f"{W2:.1f} W")
    st.metric("Total Power", f"{P_total:.1f} W")

    st.divider()

    st.metric("Power Factor", f"{pf:.3f}")

    if pf < 0.5:
        st.info("Low Power Factor")
    elif pf < 0.9:
        st.warning("Moderate Power Factor")
    else:
        st.success("Good Power Factor")

    st.divider()

    if V_supply > V_rated:
        st.warning("⚠️ Overvoltage")
    elif V_supply < V_rated:
        st.warning("⚠️ Undervoltage")
    else:
        st.success("✅ Normal Operation")
