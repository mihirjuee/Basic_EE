# 🔥 MUST BE FIRST (Streamlit + matplotlib safety)
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Two Wattmeter Method",
    page_icon="⚡",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ Learn EE")

    st.header("Supply")
    V_supply = st.slider("Line Voltage (V)", 100, 440, 400)

    st.header("Load")
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

# --- TEXTBOOK CIRCUIT FUNCTION ---
def get_circuit():
    d = schemdraw.Drawing(unit=2)

    # ================= TOP BUS =================
    d += elm.Line().right(6)

    # ================= R PHASE =================
    d.push()
    d.move(-6, 0)
    d += elm.Dot().label("R", loc='left')
    d += elm.Inductor(loops=3).label("CC1", loc='bottom')
    d += elm.Line().right(2)
    d += elm.Resistor().down(2).label("Zr")
    d.pop()

    # ================= Y PHASE =================
    d.push()
    d.move(-3, 0)
    d += elm.Dot().label("Y", loc='left')
    d += elm.Line().right(2)
    d += elm.Resistor().down(2).label("Zy")
    d.pop()

    # ================= B PHASE =================
    d.push()
    d.move(0, 0)
    d += elm.Dot().label("B", loc='left')
    d += elm.Inductor(loops=3).label("CC2", loc='bottom')
    d += elm.Line().right(2)
    d += elm.Resistor().down(2).label("Zb")
    d.pop()

    # ================= STAR NEUTRAL =================
    d.push()
    d.move(-3, -4)
    d += elm.Dot().label("N", loc='bottom')
    d.pop()

    # ================= LOAD CONNECTIONS =================
    d.push()
    d.move(-4, -2)
    d += elm.Line().down(2)
    d += elm.Line().right(1)
    d.pop()

    d.push()
    d.move(-1, -2)
    d += elm.Line().down(2)
    d.pop()

    d.push()
    d.move(2, -2)
    d += elm.Line().down(2)
    d += elm.Line().left(1)
    d.pop()

    # ================= POTENTIAL COILS =================

    # W1 (R-Y)
    d.push()
    d.move(-4, 0)
    d += elm.Line().up()
    d += elm.Inductor(loops=7).label("PC1", loc='right')
    d += elm.Line().right(3)
    d.pop()

    # W2 (B-Y)
    d.push()
    d.move(2, 0)
    d += elm.Line().down()
    d += elm.Inductor(loops=7).label("PC2", loc='right')
    d += elm.Line().left(3)
    d.pop()

    return d

# --- MAIN UI ---
st.title("⚡ Two-Wattmeter Method (Star Connected Load)")

col1, col2 = st.columns([1.5, 1])

# --- CIRCUIT DIAGRAM ---
with col1:
    st.subheader("🔌 Circuit Diagram (Textbook Style)")

    d = get_circuit()
    d.draw()                 # IMPORTANT FIX
    fig = plt.gcf()          # get matplotlib figure
    st.pyplot(fig)           # show in Streamlit
    plt.clf()                # clear for rerun safety

# --- RESULTS PANEL ---
with col2:
    st.subheader("📊 Results")

    st.metric("Line Current", f"{I_actual:.2f} A")
    st.metric("Wattmeter W1", f"{W1:.1f} W")
    st.metric("Wattmeter W2", f"{W2:.1f} W")
    st.metric("Total Power", f"{P_total:.1f} W")

    st.divider()

    st.metric("Power Factor", f"{pf:.3f}")

    if pf < 0.5:
        st.info("Low Power Factor (Inductive Load)")
    elif pf < 0.9:
        st.warning("Moderate Power Factor")
    else:
        st.success("Good Power Factor")

    st.divider()

    if V_supply > V_rated:
        st.warning("⚠️ Overvoltage Condition")
    elif V_supply < V_rated:
        st.warning("⚠️ Undervoltage Condition")
    else:
        st.success("✅ Normal Operation")
