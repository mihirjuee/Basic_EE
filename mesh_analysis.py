import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd
import time

# --- Page Config ---
st.set_page_config(page_title="Mesh Analysis Virtual Lab", layout="wide")

st.title("🔬 Mesh Analysis Virtual Lab")
st.markdown("Interactive 3-loop mesh analysis with visualization, equations, and learning tools.")

# --- Sidebar ---
st.sidebar.header("🕹️ Circuit Controls")

V1 = st.sidebar.slider("Source Voltage V1 [V]", 5, 100, 40)
V2 = st.sidebar.slider("Source Voltage V2 [V]", 5, 100, 20)

R1 = st.sidebar.slider("R1 [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("R2 (Shared 1-2) [Ω]", 10, 500, 150)
R3 = st.sidebar.slider("R3 [Ω]", 10, 500, 100)
R4 = st.sidebar.slider("R4 (Shared 2-3) [Ω]", 10, 500, 200)
R5 = st.sidebar.slider("R5 [Ω]", 10, 500, 120)

selected_loop = st.sidebar.selectbox("Highlight Loop", ["All", "Loop 1", "Loop 2", "Loop 3"])
animate = st.sidebar.checkbox("⚡ Animate Current")
quiz_mode = st.sidebar.checkbox("🎓 Quiz Mode")

# --- Mesh Calculation ---
R_matrix = np.array([
    [R1 + R2, -R2, 0],
    [-R2, R2 + R3 + R4, -R4],
    [0, -R4, R4 + R5]
])

V_vector = np.array([V1, 0, -V2])
I1, I2, I3 = np.linalg.solve(R_matrix, V_vector)

# --- Colors ---
color1 = 'red' if selected_loop in ["All", "Loop 1"] else 'black'
color2 = 'green' if selected_loop in ["All", "Loop 2"] else 'black'
color3 = 'blue' if selected_loop in ["All", "Loop 3"] else 'black'

# --- Draw Circuit ---
def draw_circuit():
    d = schemdraw.Drawing()
    d.config(unit=3)

    # LOOP 1
    V_L = elm.SourceV().label(f'V1\n{V1}V')
    d += V_L

    R1_e = elm.Resistor().right().label(f'R1\n{R1}Ω')
    d += R1_e

    R_S1 = elm.Resistor().down().label(f'R2\n{R2}Ω')
    d += R_S1

    d += elm.Line().left().to(V_L.start)

    # Loop 1 arrow
    d += elm.Line().at((1.5, -0.3)).right(0.5).color(color1)
    d += elm.Line().down(0.6).color(color1)
    d += elm.Line().left(0.5).color(color1)
    d += elm.Arrow().up(0.6).color(color1)
    d += elm.Label().at((1.5, -1.3)).label('$I_1$', color=color1)

    # LOOP 2
    R3_e = elm.Resistor().right().at(R_S1.start).label(f'R3\n{R3}Ω')
    d += R3_e

    R_S2 = elm.Resistor().down().label(f'R4\n{R4}Ω')
    d += R_S2

    d += elm.Line().left().to(R_S1.end)

    # Loop 2 arrow
    d += elm.Line().at((4.5, -0.3)).right(0.5).color(color2)
    d += elm.Line().down(0.6).color(color2)
    d += elm.Line().left(0.5).color(color2)
    d += elm.Arrow().up(0.6).color(color2)
    d += elm.Label().at((4.5, -1.3)).label('$I_2$', color=color2)

    # LOOP 3
    R5_e = elm.Resistor().right().at(R_S2.start).label(f'R5\n{R5}Ω')
    d += R5_e

    V_R = elm.SourceV().down().label(f'V2\n{V2}V')
    d += V_R

    d += elm.Line().left().to(R_S2.end)

    # Loop 3 arrow
    d += elm.Line().at((7.5, -0.3)).right(0.5).color(color3)
    d += elm.Line().down(0.6).color(color3)
    d += elm.Line().left(0.5).color(color3)
    d += elm.Arrow().up(0.6).color(color3)
    d += elm.Label().at((7.5, -1.3)).label('$I_3$', color=color3)

    # Currents
    d += elm.CurrentLabel().at(R_S1).label(f'{(I1-I2)*1000:.1f} mA')
    d += elm.CurrentLabel().at(R_S2).label(f'{(I2-I3)*1000:.1f} mA')

    d.save("mesh.png")

draw_circuit()

# --- Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.image("mesh.png", use_container_width=True)

with col2:
    st.metric("I1", f"{I1*1000:.2f} mA")
    st.metric("I2", f"{I2*1000:.2f} mA")
    st.metric("I3", f"{I3*1000:.2f} mA")

# --- Animation ---
if animate:
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i+1)
        time.sleep(0.01)

# --- KVL ---
st.subheader("KVL Equations")
st.latex(f"I_1({R1}+{R2}) - I_2({R2}) = {V1}")
st.latex(f"-I_1({R2}) + I_2({R2}+{R3}+{R4}) - I_3({R4}) = 0")
st.latex(f"-I_2({R4}) + I_3({R4}+{R5}) = -{V2}")
