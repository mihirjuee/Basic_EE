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

# --- MAIN TITLE ---
st.title("⚡ Two-Wattmeter Power Measurement Lab")

col1, col2 = st.columns([1.5, 1])

# --- CIRCUIT DIAGRAM ---

def get_circuit_drawing():
    d = schemdraw.Drawing()
    
    # R-Phase
    d.add(elm.Line().label("R", loc='left').length(1))
    d.add(elm.Circle().label("W1")) # Circles work in almost all versions
    d.add(elm.Line().right().length(1))
    d.add(elm.Resistor().label("Load").right())
    
    # Y-Phase
    d.add(elm.Line().at((0,-2)).label("Y", loc='left').length(1))
    d.add(elm.Dot())
    
    # B-Phase
    d.add(elm.Line().at((0,-4)).label("B", loc='left').length(1))
    d.add(elm.Circle().label("W2")) # Using Circle instead of Meter
    d.add(elm.Line().right().length(1))
    d.add(elm.Resistor().label("Load").right())
    
    return d

# --- Streamlit Display ---
st.subheader("🔌 2-Wattmeter Method Schematic")

# Generate the drawing object
drawing = get_circuit_drawing()

# Convert the drawing to a matplotlib figure
fig = drawing.draw()

# Pass the figure directly to st.pyplot
st.pyplot(fig)


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

    # Voltage condition alerts
    if V_supply > V_rated:
        st.warning("⚠️ High Voltage: Risk of insulation damage.")
    elif V_supply < V_rated:
        st.warning("⚠️ Low Voltage: Reduced performance.")
    else:
        st.success("✅ Nominal Operation")
