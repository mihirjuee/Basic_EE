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
    st.title("⚡ Settings")
    st.header("Supply")
    V_supply = st.slider("Line Voltage (V)", 100, 440, 400)

    st.header("Load (Rated)")
    V_rated = st.slider("Rated Voltage (V)", 200, 440, 400)
    I_rated = st.slider("Rated Current (A)", 1, 50, 10)
    P_rated = st.slider("Rated Power (kW)", 1.0, 50.0, 5.0)

# --- CALCULATIONS ---
# Calculate Impedance Z = V_phase / I_phase
Z = (V_rated / np.sqrt(3)) / I_rated
# Current for given supply voltage
I_actual = (V_supply / np.sqrt(3)) / Z
# Determine Power Factor
pf = (P_rated * 1000) / (np.sqrt(3) * V_rated * I_rated)
pf = np.clip(pf, 0, 1)
phi = np.arccos(pf)

# Two Wattmeter Formulas
W1 = (V_supply * I_actual) * np.cos(np.radians(30) - phi)
W2 = (V_supply * I_actual) * np.cos(np.radians(30) + phi)
P_total = W1 + W2

# --- CIRCUIT DIAGRAM FUNCTION ---
def get_circuit():
    with schemdraw.Drawing(unit=2) as d:
        d += elm.Line().right(6)
        # R Phase
        d.push()
        d.move(-6, 0)
        d += elm.Dot().label("R", loc='left')
        d += elm.Inductor(loops=3).label("CC1", loc='bottom')
        d += elm.Line().right(2)
        d += elm.Resistor().down(2).label("Zr")
        d.pop()
        # Y Phase
        d.push()
        d.move(-3, 0)
        d += elm.Dot().label("Y", loc='left')
        d += elm.Line().right(2)
        d += elm.Resistor().down(2).label("Zy")
        d.pop()
        # B Phase
        d.push()
        d.move(0, 0)
        d += elm.Dot().label("B", loc='left')
        d += elm.Inductor(loops=3).label("CC2", loc='bottom')
        d += elm.Line().right(2)
        d += elm.Resistor().down(2).label("Zb")
        d.pop()
        return d

# --- MAIN UI ---
st.title("⚡ Two-Wattmeter Method (Star Connected Load)")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🔌 Circuit Diagram")
    # Rendering schemdraw in Streamlit
    fig = get_circuit().draw()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📊 Results")
    st.metric("Line Current", f"{I_actual:.2f} A")
    st.metric("Wattmeter W1", f"{W1:.1f} W")
    st.metric("Wattmeter W2", f"{W2:.1f} W")
    st.metric("Total Power", f"{P_total:.1f} W")
    
    st.divider()
    st.metric("Power Factor", f"{pf:.3f}")
    
    # Educational Insights
    if phi > np.radians(60):
        st.error("⚠️ Wattmeter W2 is reading negative! (PF < 0.5)")
    elif pf < 0.9:
        st.warning("Moderate Power Factor")
    else:
        st.success("Good Power Factor")

# Understanding the phasor relationship is critical for this experiment.
