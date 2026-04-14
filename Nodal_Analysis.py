import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd
import os

# ✅ MUST BE FIRST
st.set_page_config(
    page_title="Nodal Analysis Lab",
    page_icon="⚡",
    layout="wide"
)

# --- Safe Logo Loader ---
def load_logo():
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        return logo_path
    return None

logo = load_logo()

# --- Header ---
col1, col2 = st.columns([1, 6])

with col1:
    if logo:
        st.image(logo, width=80)

with col2:
    st.title("🔬 Nodal Analysis Virtual Lab")

# Sidebar logo
if logo:
    st.sidebar.image(logo, use_container_width=True)

st.markdown("Solve node voltages using **Kirchhoff’s Current Law (KCL)**.")

# --- Sidebar Controls ---
st.sidebar.header("🕹️ Circuit Controls")

Vs1 = st.sidebar.slider("Voltage Source V1 [V]", 5, 100, 40)
Vs2 = st.sidebar.slider("Voltage Source V2 [V]", 5, 100, 20)

R1 = st.sidebar.slider("Resistor R1 [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("Resistor R2 [Ω]", 10, 500, 200)
R3 = st.sidebar.slider("Resistor R3 [Ω]", 10, 500, 150)

# --- Nodal Calculation ---
G_total = (1/R1) + (1/R2) + (1/R3)

# ✅ Correct KCL injection
I_injected = (Vs1/R1) + (Vs2/R3)

V_node = I_injected / G_total

# Currents
I_R1 = (Vs1 - V_node) / R1
I_R2 = V_node / R2
I_R3 = (Vs2 - V_node) / R3

# --- Draw Circuit ---
def draw_nodal_circuit():
    d = schemdraw.Drawing()
    d.config(unit=3)

    # Left branch
    V1 = d.add(elm.SourceV().label(f'V1\n{Vs1}V'))
    d.add(elm.Resistor().right().label(f'R1\n{R1}Ω'))

    # Node
    d.add(elm.Dot().label('Node A', loc='top', color='blue'))

    # Middle branch
    d.push()
    d.add(elm.Resistor().down().label(f'R2\n{R2}Ω'))
    d.add(elm.Ground())
    d.pop()

    # Right branch
    d.add(elm.Resistor().right().label(f'R3\n{R3}Ω'))
    d.add(elm.SourceV().down().label(f'V2\n{Vs2}V'))

    # Bottom loop
    d.add(elm.Line().left().to(V1.start))
    d.add(elm.Dot())

    d.save("nodal_circuit.png")

draw_nodal_circuit()

# --- Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🖼️ Circuit Diagram")
    st.image("nodal_circuit.png", use_container_width=True)
    st.info("💡 KCL: Sum of currents leaving Node A = 0")

with col2:
    st.subheader("📊 Results")

    st.metric("Node Voltage (Va)", f"{V_node:.2f} V")

    st.markdown("### Currents")
    st.write(f"➡️ I_R1 = {I_R1:.2f} A")
    st.write(f"⬇️ I_R2 = {I_R2:.2f} A")
    st.write(f"⬅️ I_R3 = {I_R3:.2f} A")

st.divider()

# --- Math Section ---
st.subheader("🧠 Mathematical Model")

st.latex(r"I_1 + I_2 + I_3 = 0")
st.latex(
    rf"\frac{{V_a - {Vs1}}}{{{R1}}} + \frac{{V_a}}{{{R2}}} + \frac{{V_a - {Vs2}}}{{{R3}}} = 0"
)

# --- Table ---
df = pd.DataFrame({
    "Parameter": ["Va", "I_R1", "I_R2", "I_R3"],
    "Value": [
        f"{V_node:.2f} V",
        f"{I_R1:.2f} A",
        f"{I_R2:.2f} A",
        f"{I_R3:.2f} A"
    ]
})

st.table(df)
