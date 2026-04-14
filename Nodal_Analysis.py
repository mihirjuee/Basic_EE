import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

# ✅ MUST BE FIRST
st.set_page_config(page_title="Nodal Analysis Lab", page_icon="logo.png", layout="wide")

# --- Header with Logo ---
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo.png", width=80)

with col2:
    st.title("🔬 Nodal Analysis Virtual Lab")

# Sidebar Logo (only once)
st.sidebar.image("logo.png", use_container_width=True)

st.markdown("Solve for unknown node voltages using **Kirchhoff's Current Law (KCL)**.")

# --- Sidebar ---
st.sidebar.header("🕹️ Circuit Controls")

Vs1 = st.sidebar.slider("Voltage Source V1 [V]", 5, 100, 40)
Vs2 = st.sidebar.slider("Voltage Source V2 [V]", 5, 100, 20)

R1 = st.sidebar.slider("Resistor R1 [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("Resistor R2 [Ω]", 10, 500, 200)
R3 = st.sidebar.slider("Resistor R3 [Ω]", 10, 500, 150)

# --- Nodal Calculation ---
G_total = (1/R1) + (1/R2) + (1/R3)

# ✅ FIXED SIGN
I_injected = (Vs1/R1) + (Vs2/R3)

V_node = I_injected / G_total

# Branch currents
I_R1 = (Vs1 - V_node) / R1
I_R2 = V_node / R2
I_R3 = (Vs2 - V_node) / R3

# --- Draw Circuit ---
def draw_nodal_circuit():
    d = schemdraw.Drawing()
    d.config(unit=3)

    # Left source + resistor
    V1_src = d.add(elm.SourceV().label(f'V1\n{Vs1}V'))
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

    # Bottom connection
    d.add(elm.Line().left().to(V1_src.start))
    d.add(elm.Dot())

    d.save("nodal_circuit.png")

draw_nodal_circuit()

# --- Layout ---
col_diag, col_res = st.columns([1.5, 1])

with col_diag:
    st.subheader("🖼️ Circuit Topology")
    st.image("nodal_circuit.png", use_container_width=True)
    st.info("💡 KCL: Sum of currents leaving Node A = 0")

with col_res:
    st.subheader("🔢 Results")

    st.metric("Node Voltage Va", f"{V_node:.2f} V")

    st.markdown("### Currents")
    st.write(f"➡️ I_R1 = {I_R1:.2f} A")
    st.write(f"⬇️ I_R2 = {I_R2:.2f} A")
    st.write(f"⬅️ I_R3 = {I_R3:.2f} A")

st.divider()

# --- Equation ---
st.subheader("🧠 KCL Equation")

st.latex(rf"\frac{{V_a - {Vs1}}}{{{R1}}} + \frac{{V_a}}{{{R2}}} + \frac{{V_a - {Vs2}}}{{{R3}}} = 0")

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
