import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import matplotlib.pyplot as plt

# ================= PAGE =================
st.set_page_config(page_title="Wheatstone Bridge Pro", layout="wide")
st.title("⚡ Wheatstone Bridge – Virtual Lab")
st.latex(r"\frac{R_1}{R_2} = \frac{R_3}{R_4}")

# ================= SIDEBAR =================
st.sidebar.header("🧠 Settings")
unknown = st.sidebar.selectbox("Select Unknown", ["None", "R1", "R2", "R3", "R4"])

def get_input(name, default):
    return st.sidebar.slider(f"{name} (Ω)", 1.0, 1000.0, default)

# Initial values
R1, R2, R3, R4 = [get_input(n, 100.0) for n in ["R1", "R2", "R3", "R4"]]
Vs = st.sidebar.slider("Supply Voltage (V)", 1.0, 50.0, 10.0)

# ================= AUTO SOLVE =================
if unknown != "None":
    if unknown == "R1": R1 = (R2 * R3) / R4
    elif unknown == "R2": R2 = (R1 * R4) / R3
    elif unknown == "R3": R3 = (R1 * R4) / R2
    elif unknown == "R4": R4 = (R2 * R3) / R1

# ================= CALCULATIONS =================
V_left = Vs * (R3 / (R1 + R3))
V_right = Vs * (R4 / (R2 + R4))
Vg = V_left - V_right
balanced = np.isclose(Vg, 0, atol=1e-4)

# ================= CIRCUIT DIAGRAM =================
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("🔌 Bridge Circuit")
    fig, ax = plt.subplots(figsize=(6, 5))
    d = schemdraw.Drawing(canvas=ax)
    
    # Draw Diamond
    d += (D1 := elm.Dot())
    d += (R1_el := elm.Resistor().up().right().label(f"R1: {R1:.1f}Ω"))
    d += (R2_el := elm.Resistor().down().right().label(f"R2: {R2:.1f}Ω"))
    d += (R4_el := elm.Resistor().down().left().label(f"R4: {R4:.1f}Ω"))
    d += (R3_el := elm.Resistor().up().left().label(f"R3: {R3:.1f}Ω"))
    
    # Galvanometer in the middle
    d += elm.Line().at(R1_el.end).to(R3_el.end)
    d += elm.Resistor().label("G").at(R1_el.end).to(R3_el.end)
    
    d.draw()
    st.pyplot(fig)
    plt.close(fig)

# ================= GAUGE & RESULTS =================
with col2:
    st.subheader("🎥 Galvanometer")
    needle = max(min(Vg / 5, 1), -1)
    fig_g = go.Figure(go.Indicator(mode="gauge+number", value=needle, gauge={'axis': {'range': [-1, 1]}}))
    st.plotly_chart(fig_g, use_container_width=True)
    st.metric("Galvanometer Voltage (V)", f"{Vg:.6f}")
    if balanced: st.success("Balanced ✅")
    else: st.error("Unbalanced ❌")

# ================= GRAPH =================
st.subheader("📈 Balance Curve")
R4_range = np.linspace(1, 500, 200)
Vg_curve = Vs*(R3/(R1+R3)) - Vs*(R4_range/(R2+R4_range))
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=R4_range, y=Vg_curve))
fig2.add_hline(y=0, line_dash="dash")
st.plotly_chart(fig2, use_container_width=True)
