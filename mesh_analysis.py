import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

st.set_page_config(page_title="3-Loop Mesh Lab", layout="wide")

st.title("🕸️ Advanced Mesh Analysis: 3-Loop Circuit")
st.markdown("Experiment with a complex three-loop network and observe how currents redistribute.")

# --- Sidebar: 8 Adjustable Parameters ---
st.sidebar.header("Circuit Parameters")
V1 = st.sidebar.slider("Source V1 [V]", 5, 100, 30)
V2 = st.sidebar.slider("Source V2 [V]", 5, 100, 20)
R1 = st.sidebar.slider("R1 (Loop 1) [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("R2 (Shared 1-2) [Ω]", 10, 500, 150)
R3 = st.sidebar.slider("R3 (Loop 2) [Ω]", 10, 500, 100)
R4 = st.sidebar.slider("R4 (Shared 2-3) [Ω]", 10, 500, 200)
R5 = st.sidebar.slider("R5 (Loop 3) [Ω]", 10, 500, 120)

# --- Math: Solving the 3x3 Matrix ---
# Loop 1: (R1+R2)I1 - R2*I2 = V1
# Loop 2: -R2*I1 + (R2+R3+R4)I2 - R4*I3 = 0
# Loop 3: -R4*I2 + (R4+R5)I3 = -V2

A = np.array([
    [R1 + R2, -R2, 0],
    [-R2, R2 + R3 + R4, -R4],
    [0, -R4, R4 + R5]
])
B = np.array([V1, 0, -V2])

try:
    I = np.linalg.solve(A, B)
    I1, I2, I3 = I[0], I[1], I[2]
except np.linalg.LinAlgError:
    st.error("Calculation Error: Check resistor values.")

# --- Circuit Diagram Generation ---
def draw_3loop():
    with schemdraw.Drawing() as d:
        # Loop 1
        d += (V_left := elm.SourceV().label(f'V1={V1}V'))
        d += elm.Resistor().right().label(f'R1\n{R1}Ω')
        d += (R_shared1 := elm.Resistor().down().label(f'R2\n{R2}Ω'))
        d += elm.Line().left().to(V_left.start)
        
        # Loop 2
        d += elm.Resistor().right().at(R_shared1.start).label(f'R3\n{R3}Ω')
        d += (R_shared2 := elm.Resistor().down().label(f'R4\n{R4}Ω'))
        d += elm.Line().left().to(R_shared1.end)
        
        # Loop 3
        d += elm.Resistor().right().at(R_shared2.start).label(f'R5\n{R5}Ω')
        d += (V_right := elm.SourceV().down().label(f'V2={V2}V', loc='bottom'))
        d += elm.Line().left().to(R_shared2.end)
        
        d.save("three_loop.png")

draw_3loop()

# --- UI Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📋 3-Loop Network Diagram")
    st.image("three_loop.png")
    
    st.markdown("### Mesh Matrix $[R][I] = [V]$")
    st.latex(r"""
    \begin{bmatrix}
    R_1+R_2 & -R_2 & 0 \\
    -R_2 & R_2+R_3+R_4 & -R_4 \\
    0 & -R_4 & R_4+R_5
    \end{bmatrix}
    \begin{bmatrix}
    I_1 \\ I_2 \\ I_3
    \end{bmatrix}
    =
    \begin{bmatrix}
    V_1 \\ 0 \\ -V_2
    \end{bmatrix}
    """)

with col2:
    st.subheader("🧪 Results")
    st.metric("Mesh Current I1", f"{I1*1000:.2f} mA")
    st.metric("Mesh Current I2", f"{I2*1000:.2f} mA")
    st.metric("Mesh Current I3", f"{I3*1000:.2f} mA")
    
    st.divider()
    st.write("**Real Branch Currents:**")
    branch_data = {
        "Branch": ["R1", "R2 (Shared)", "R3", "R4 (Shared)", "R5"],
        "Current": [f"{I1*1000:.2f} mA", f"{(I1-I2)*1000:.2f} mA", f"{I2*1000:.2f} mA", f"{(I2-I3)*1000:.2f} mA", f"{I3*1000:.2f} mA"]
    }
    st.table(pd.DataFrame(branch_data))

st.info("💡 **Observation:** Notice how Mesh 2 has no direct voltage source, yet current flows through it due to the coupling from Mesh 1 and Mesh 3 via the shared resistors.")
