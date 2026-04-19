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
   # st.image("https://github.com/mihirjuee/Basic_EE/blob/main/logo.png", width=200)
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
# Circuit Diagram section update
with col1:
    st.subheader("🔌 Two Wattmeter Method Connection")

    import schemdraw
    import schemdraw.elements as elm

    d = schemdraw.Drawing()

    # ---------------- LINE A ----------------
    d += elm.SourceV().up().label("Line A")
    d += elm.Line().right()
    d += elm.Resistor().label("W1")   # Wattmeter (symbolic)
    d += elm.Line().right()
    d += elm.Resistor().down().label("Load A")

    # Return to base
    d += elm.Line().left(3)
    d += elm.Line().down(2)

    # ---------------- LINE B ----------------
    d += elm.SourceV().up().label("Line B")
    d += elm.Line().right()
    d += elm.Resistor().label("W2")   # Wattmeter (symbolic)
    d += elm.Line().right()
    d += elm.Resistor().down().label("Load B")

    # Return to base
    d += elm.Line().left(3)
    d += elm.Line().down(2)

    # ---------------- LINE C ----------------
    d += elm.SourceV().up().label("Line C")
    d += elm.Line().right()
    d += elm.Resistor().down().label("Load C")

    # ---------------- COMMON RETURN ----------------
    d += elm.Line().left(2)
    d += elm.Line().down()
    d += elm.Line().right(4)

    fig = d.draw()
    st.pyplot(fig)
    

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
