import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Learn EE Interactive",page_icon="logo.png", layout="wide")

# --- CUSTOM CSS FOR BRANDING ---
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

# --- SIDEBAR BRANDING & INPUTS ---
with st.sidebar:
    # Replace the URL with your actual logo image URL
    st.image("https://github.com/mihirjuee/Basic_EE/new/main/logo.png", width=200)
    st.title("Learn EE Interactive")
    
    st.header("⚙️ Supply Settings")
    V_supply = st.slider("Supply Line Voltage (V) [V]", 100, 440, 400)
    
    st.divider()
    
    st.header("🏷️ Load Nameplate Data")
    V_rated = st.slider("Rated Voltage (V) [V]", 200, 440, 400)
    I_rated = st.slider("Rated Current (I) [A]", 1, 50, 10)
    P_rated = st.slider("Rated Active Power (P) [kW]", 1.0, 50.0, 5.0)

# --- LOGIC ---
pf = (P_rated * 1000) / (np.sqrt(3) * V_rated * I_rated)
pf = np.clip(pf, 0.0, 1.0)
I_actual = I_rated * (V_supply / V_rated)
phi = np.arccos(pf)

# Two-wattmeter formulas
W1 = (V_supply * I_actual * np.cos(np.radians(30) - phi))
W2 = (V_supply * I_actual * np.cos(np.radians(30) + phi))
P_total = W1 + W2

# --- MAIN CONTENT ---
st.title("⚡ 2-Wattmeter Power Measurement Lab")
col1, col2 = st.columns([1.5, 1])

# CIRCUIT DIAGRAM
with col1:
    st.subheader("🔌 Connection Schematic")
    d = schemdraw.Drawing()
    d += elm.SourceV().label("Line A").up()
    d += elm.MeterW().label("W1").right()
    d += elm.Line().down().length(1)
    d += elm.Resistor().label("Load A").down()
    
    d += elm.Line().at((0,0)).right().length(1)
    d += elm.SourceV().at((1,0)).label("Line B").up()
    d += elm.MeterW().label("W2").right()
    d += elm.Line().down().length(1)
    d += elm.Resistor().label("Load B").down()
    
    d += elm.SourceV().at((2,0)).label("Line C").up()
    d += elm.Line().up().length(0.5)
    d += elm.Resistor().label("Load C").down()
    
    st.pyplot(d.draw().fig)
    

# READINGS
with col2:
    st.subheader("📊 Results")
    st.metric("Actual Line Current", f"{I_actual:.2f} A")
    st.metric("Wattmeter 1 (W1)", f"{W1:.1f} W")
    st.metric("Wattmeter 2 (W2)", f"{W2:.1f} W")
    st.metric("Total Power", f"{P_total:.1f} W")
    
    if V_supply > V_rated:
        st.warning("⚠️ High Voltage: Check insulation.")
    elif V_supply < V_rated:
        st.warning("⚠️ Low Voltage: Load performance reduced.")
    else:
        st.success("✅ Nominal Operation.")
