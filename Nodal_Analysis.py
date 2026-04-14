import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Nodal Analysis Virtual Lab", layout="wide")

st.title("🔬 Nodal Analysis Virtual Lab")
st.markdown("Solve node voltages using KCL with interactive visualization.")

# --- Sidebar ---
st.sidebar.header("🕹️ Circuit Controls")

V1 = st.sidebar.slider("Voltage Source V1 (to Node 1) [V]", 1, 50, 10)
V2 = st.sidebar.slider("Voltage Source V2 (to Node 3) [V]", 1, 50, 5)

R1 = st.sidebar.slider("R1 (Node1-GND) [Ω]", 10, 1000, 100)
R2 = st.sidebar.slider("R2 (Node1-Node2) [Ω]", 10, 1000, 200)
R3 = st.sidebar.slider("R3 (Node2-GND) [Ω]", 10, 1000, 150)
R4 = st.sidebar.slider("R4 (Node2-Node3) [Ω]", 10, 1000, 220)
R5 = st.sidebar.slider("R5 (Node3-GND) [Ω]", 10, 1000, 180)

highlight = st.sidebar.selectbox("Highlight Node", ["All", "Node 1", "Node 2", "Node 3"])

# --- Conductance Matrix (G = 1/R) ---
G1, G2, G3, G4, G5 = 1/R1, 1/R2, 1/R3, 1/R4, 1/R5

# --- Nodal Equations ---
# [G]*[V] = I

G_matrix = np.array([
    [G1+G2, -G2, 0],
    [-G2, G2+G3+G4, -G4],
    [0, -G4, G4+G5]
])

I_vector = np.array([
    G1*V1,
    0,
    G5*V2
])

Vn1, Vn2, Vn3 = np.linalg.solve(G_matrix, I_vector)

# --- Colors ---
c1 = 'red' if highlight in ["All", "Node 1"] else 'black'
c2 = 'green' if highlight in ["All", "Node 2"] else 'black'
c3 = 'blue' if highlight in ["All", "Node 3"] else 'black'

# --- Draw Circuit ---
def draw_circuit():
    d = schemdraw.Drawing()
    d.config(unit=3)

    # Node 1
    d += elm.Dot().label("N1", loc='top').color(c1)
    d += elm.Resistor().down().label(f'R1\n{R1}Ω')
    d += elm.Ground()

    d += elm.Line().right()
    d += elm.Resistor().label(f'R2\n{R2}Ω')

    # Node 2
    d += elm.Dot().label("N2", loc='top').color(c2)
    d += elm.Resistor().down().label(f'R3\n{R3}Ω')
    d += elm.Ground()

    d += elm.Line().right()
    d += elm.Resistor().label(f'R4\n{R4}Ω')

    # Node 3
    d += elm.Dot().label("N3", loc='top').color(c3)
    d += elm.Resistor().down().label(f'R5\n{R5}Ω')
    d += elm.Ground()

    # Voltage Sources
    d += elm.SourceV().up().at((0,0)).label(f'V1\n{V1}V')
    d += elm.SourceV().up().at((6,0)).label(f'V2\n{V2}V')

    d.save("nodal.png")

draw_circuit()

# --- Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🖼️ Circuit Diagram")
    st.image("nodal.png", use_container_width=True)

with col2:
    st.subheader("🔢 Node Voltages")
    st.metric("V1 (Node 1)", f"{Vn1:.2f} V")
    st.metric("V2 (Node 2)", f"{Vn2:.2f} V")
    st.metric("V3 (Node 3)", f"{Vn3:.2f} V")

# --- KCL Equations ---
st.divider()
st.subheader("🧠 KCL Equations")

st.latex(f"(V_1/{R1}) + (V_1 - V_2)/{R2} = {V1}/{R1}")
st.latex(f"(V_2 - V_1)/{R2} + V_2/{R3} + (V_2 - V_3)/{R4} = 0")
st.latex(f"(V_3 - V_2)/{R4} + V_3/{R5} = {V2}/{R5}")

# --- Branch Currents ---
st.divider()
st.subheader("📊 Branch Currents")

I_R1 = Vn1 / R1
I_R2 = (Vn1 - Vn2) / R2
I_R3 = Vn2 / R3
I_R4 = (Vn2 - Vn3) / R4
I_R5 = Vn3 / R5

df = pd.DataFrame({
    "Branch": ["R1", "R2", "R3", "R4", "R5"],
    "Current (mA)": [
        I_R1*1000,
        I_R2*1000,
        I_R3*1000,
        I_R4*1000,
        I_R5*1000
    ]
})

st.table(df)

# --- Power ---
st.subheader("⚡ Power Dissipation")

power_df = pd.DataFrame({
    "Component": ["R1", "R2", "R3", "R4", "R5"],
    "Power (W)": [
        I_R1**2 * R1,
        I_R2**2 * R2,
        I_R3**2 * R3,
        I_R4**2 * R4,
        I_R5**2 * R5
    ]
})

st.table(power_df)

# --- Footer ---
st.info("Nodal analysis uses KCL: Sum of currents leaving a node = 0.")
