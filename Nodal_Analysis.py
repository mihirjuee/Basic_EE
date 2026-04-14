import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

st.set_page_config(page_title="Nodal Analysis Lab", layout="wide")

st.title("📍 Nodal Analysis Simulator")
st.markdown("Solve for unknown node voltages using **Kirchhoff's Current Law (KCL)**.")

# --- Sidebar: Circuit Parameters ---
st.sidebar.header("🕹️ Circuit Controls")
Vs1 = st.sidebar.slider("Voltage Source V1 [V]", 5, 100, 40)
Vs2 = st.sidebar.slider("Voltage Source V2 [V]", 5, 100, 20)
R1 = st.sidebar.slider("Resistor R1 [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("Resistor R2 [Ω]", 10, 500, 200)
R3 = st.sidebar.slider("Resistor R3 [Ω]", 10, 500, 150)

# --- Calculation Engine (Nodal Equations) ---
# Node 1 is at the junction of R1, R2, and R3.
# Let V_node be the voltage at this central junction.
# KCL at Node: (V_node - Vs1)/R1 + (V_node / R2) + (V_node + Vs2)/R3 = 0
# V_node * (1/R1 + 1/R2 + 1/R3) = (Vs1/R1) + (Vs2/R3)

G_total = (1/R1) + (1/R2) + (1/R3)
I_injected = (Vs1/R1) - (Vs2/R3)
V_node = I_injected / G_total

# Branch Currents
I_R1 = (Vs1 - V_node) / R1
I_R2 = V_node / R2
I_R3 = (Vs2 - V_node) / R3

# --- Diagram Generation ---
def draw_nodal_circuit():
    with schemdraw.Drawing() as d:
        d.config(unit=3, fontsize=10)
        
        # Left branch
        V1_src = d.add(elm.SourceV().label(f'V1\n{Vs1}V'))
        d.add(elm.Resistor().right().label(f'R1\n{R1}Ω'))
        
        # Central Node
        node_dot = d.add(elm.Dot().label('Node A', loc='top', color='blue'))
        
        # Middle branch
        d.push()
        d.add(elm.Resistor().down().label(f'R2\n{R2}Ω'))
        d.add(elm.Ground())
        d.pop()
        
        # Right branch
        d.add(elm.Resistor().right().label(f'R3\n{R3}Ω'))
        V2_src = d.add(elm.SourceV().down().label(f'V2\n{Vs2}V', loc='bottom'))
        
        # Bottom connection
        d.add(elm.Line().left().to(V1_src.start))
        d.add(elm.Dot())
        
        d.save("nodal_circuit.png")

draw_nodal_circuit()

# --- UI Layout ---
col_diag, col_res = st.columns([1.5, 1])

with col_diag:
    st.subheader("🖼️ Circuit Topology")
    st.image("nodal_circuit.png", use_container_width=True)
    st.info("💡 **KCL Equation:** The sum of currents leaving 'Node A' must be zero.")

with col_res:
    st.subheader("🔢 Nodal Results")
    st.metric("Voltage at Node A (Va)", f"{V_node:.2f} V")
    
    st.markdown("---")
    st.write("**Branch Current Directions:**")
    st.write(f"➡️ From V1: **{I_R1:.2f} A**")
    st.write(f"⬇️ Through R2: **{I_R2:.2f} A**")
    st.write(f"⬅️ From V2: **{I_R3:.2f} A**")

st.divider()

# --- Math Section ---
st.subheader("📝 The Mathematical Model")
st.latex(r"I_1 + I_2 + I_3 = 0")
st.latex(rf"\frac{{V_a - {Vs1}}}{{{R1}}} + \frac{{V_a}}{{ {R2} }} + \frac{{V_a + {Vs2}}}{{{R3}}} = 0")

# Comparison Table
analysis_df = pd.DataFrame({
    "Parameter": ["Node A Voltage", "Current I_R1", "Current I_R2", "Current I_R3"],
    "Value": [f"{V_node:.2f} V", f"{I_R1*1000:.2f} mA", f"{I_R2*1000:.2f} mA", f"{I_R3*1000:.2f} mA"]
})
st.table(analysis_df)
