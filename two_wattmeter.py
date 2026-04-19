# 🔥 MUST BE FIRST (prevents Streamlit backend issues)
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Learn EE Interactive",
    page_icon="⚡",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
}
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Learn EE Interactive")

    st.header("⚙️ Supply Settings")
    V_supply = st.slider("Supply Line Voltage (V)", 100, 440, 400)

    st.divider()

    st.header("🏷️ Load Nameplate Data")
    V_rated = st.slider("Rated Voltage (V)", 200, 440, 400)
    I_rated = st.slider("Rated Current (A)", 1, 50, 10)
    P_rated = st.slider("Rated Power (kW)", 1.0, 50.0, 5.0)

# --- CALCULATIONS ---
pf = (P_rated * 1000) / (np.sqrt(3) * V_rated * I_rated)
pf = np.clip(pf, 0.0, 1.0)

I_actual = I_rated * (V_supply / V_rated)
phi = np.arccos(pf)

# Two-wattmeter method
W1 = V_supply * I_actual * np.cos(np.radians(30) - phi)
W2 = V_supply * I_actual * np.cos(np.radians(30) + phi)
P_total = W1 + W2

# --- CIRCUIT DRAWING FUNCTION ---
def get_circuit_drawing():
    d = schemdraw.Drawing(unit=2)

    # ================= R LINE =================
    d += elm.Line().right().label("R", loc='left')

    # W1 Current Coil (few turns)
    d += elm.Inductor(loops=3).label("CC1", loc='bottom')

    r_node = d += elm.Dot()

    d += elm.Line().right()
    d += elm.Resistor().down().label("Load R")

    # ================= Y LINE =================
    d += elm.Line().left(3)
    d += elm.Line().down(2)

    d += elm.Line().right().label("Y", loc='left')
    y_node = d += elm.Dot()

    d += elm.Line().right()
    d += elm.Resistor().down().label("Load Y")

    # ================= B LINE =================
    d += elm.Line().left(3)
    d += elm.Line().down(2)

    d += elm.Line().right().label("B", loc='left')

    # W2 Current Coil (few turns)
    d += elm.Inductor(loops=3).label("CC2", loc='bottom')

    b_node = d += elm.Dot()

    d += elm.Line().right()
    d += elm.Resistor().down().label("Load B")

    # ================= COMMON RETURN =================
    d += elm.Line().left(2)
    d += elm.Line().down()
    d += elm.Line().right(4)

    # ================= POTENTIAL COILS =================

    # --- W1 PC across R-Y (more turns) ---
    d.push()
    d.move_from(r_node)
    d += elm.Line().up()
    d += elm.Inductor(loops=7).label("PC1", loc='right')
    d += elm.Line().to(y_node)
    d.pop()

    # --- W2 PC across B-Y (more turns) ---
    d.push()
    d.move_from(b_node)
    d += elm.Line().down()
    d += elm.Inductor(loops=7).label("PC2", loc='right')
    d += elm.Line().to(y_node)
    d.pop()

    return d

# --- MAIN TITLE ---
st.title("⚡ Two-Wattmeter Power Measurement Lab")

col1, col2 = st.columns([1.5, 1])

# --- CIRCUIT DIAGRAM ---
with col1:
    st.subheader("🔌 Two Wattmeter Method Connection")

    d = get_circuit_drawing()

    d.draw()
    fig = plt.gcf()
    st.pyplot(fig)
    plt.clf()

# --- RESULTS ---
with col2:
    st.subheader("📊 Results")

    st.metric("Line Current", f"{I_actual:.2f} A")
    st.metric("Wattmeter W1", f"{W1:.1f} W")
    st.metric("Wattmeter W2", f"{W2:.1f} W")
    st.metric("Total Power", f"{P_total:.1f} W")

    st.divider()

    st.metric("Power Factor", f"{pf:.3f}")

    if pf < 0.5:
        st.info("Low Power Factor (Highly Inductive Load)")
    elif pf < 0.9:
        st.warning("Moderate Power Factor")
    else:
        st.success("Good Power Factor")

    st.divider()

    if V_supply > V_rated:
        st.warning("⚠️ High Voltage: Risk of insulation damage.")
    elif V_supply < V_rated:
        st.warning("⚠️ Low Voltage: Reduced performance.")
    else:
        st.success("✅ Nominal Operation")
