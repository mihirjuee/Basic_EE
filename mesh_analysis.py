import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

# Page Configuration
st.set_page_config(page_title="3-Loop Mesh Simulator", layout="wide")

st.title("🕸️ Interactive 3-Loop Mesh Analysis")
st.markdown("""
This lab solves a 3-loop resistive network using the **Mesh Current Method**. 
Adjust the sliders to see how the currents $I_1, I_2,$ and $I_3$ interact in shared branches.
""")

# --- Sidebar: Circuit Parameters ---
st.sidebar.header("🕹️ Circuit Controls")
V1 = st.sidebar.slider("Source Voltage V1 [V]", 5, 100, 40)
V2 = st.sidebar.slider("Source Voltage V2 [V]", 5, 100, 20)
R1 = st.sidebar.slider("Resistor R1 (Loop 1) [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("Resistor R2 (Shared 1-2) [Ω]", 10, 500, 150)
R3 = st.sidebar.slider("Resistor R3 (Loop 2) [Ω]", 10, 500, 100)
R4 = st.sidebar.slider("Resistor R4 (Shared 2-3) [Ω]", 10, 500, 200)
R5 = st.sidebar.slider("Resistor R5 (Loop 3) [Ω]", 10, 500, 120)

# --- Calculation Engine (Matrix Math) ---
# Matrix R * I = V
# Row 1: (R1+R2)I1 - R2*I2 + 0 = V1
# Row 2: -R2*I1 + (R2+R3+R4)I2 - R4*I3 = 0
# Row 3: 0 - R4*I2 + (R4+R5)I3 = -V2
R_matrix = np.array([
    [R1 + R2, -R2, 0],
    [-R2, R2 + R3 + R4, -R4],
    [0, -R4, R4 + R5]
])
V_vector = np.array([V1, 0, -V2])

try:
    I_results = np.linalg.solve(R_matrix, V_vector)
    I1, I2, I3 = I_results[0], I_results[1], I_results[2]
except np.linalg.LinAlgError:
    st.error("Matrix error. Please check resistor values.")

# --- Diagram Generation with Loop Currents ---
def generate_circuit_diagram():
    with schemdraw.Drawing() as d:
        d.config(unit=3, fontsize=10)
        
        # --- Mesh 1 ---
        d += (V_L := elm.SourceV().label(f'V1\n{V1}V'))
        d += elm.Resistor().right().label(f'R1\n{R1}Ω')
        d += (R_S1 := elm.Resistor().down().label(f'R2\n{R2}Ω'))
        d += elm.Line().left().to(V_L.start)
        d += elm.LoopCurrent([V_L, R_S1], direction='cw').label('$I_1$')
        
        # --- Mesh 2 ---
        d += elm.Resistor().right().at(R_S1.start).label(f'R3\n{R3}Ω')
        d += (R_S2 := elm.Resistor().down().label(f'R4\n{R4}Ω'))
        d += elm.Line().left().to(R_S1.end)
        d += elm.LoopCurrent([R_S1, R_S2], direction='cw').label('$I_2$')
        
        # --- Mesh 3 ---
        d += elm.Resistor().right().at(R_S2.start).label(f'R5\n{R5}Ω')
        d += (V_R := elm.SourceV().down().label(f'V2\n{V2}V', loc='bottom'))
        d += elm.Line().left().to(R_S2.end)
        d += elm.LoopCurrent([R_S2, V_R], direction='cw').label('$I_3$')
        
        d.save("mesh_3_loop.png")

generate_circuit_diagram()

# --- UI Layout ---
col_diag, col_math = st.columns([1.5, 1])

with col_diag:
    st.subheader("🖼️ Live Circuit Diagram")
    st.image("mesh_3_loop.png", use_container_width=True)
    st.caption("The circular arrows indicate the clockwise Mesh Currents assumed in our equations.")

with col_math:
    st.subheader("🔢 System of Equations")
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
    
    st.markdown("---")
    st.subheader("🧪 Results")
    st.metric("Mesh Current I1", f"{I1*1000:.2f} mA")
    st.metric("Mesh Current I2", f"{I2*1000:.2f} mA")
    st.metric("Mesh Current I3", f"{I3*1000:.2f} mA")

st.divider()

# --- Analysis Table ---
st.subheader("📋 Detailed Branch Analysis")
analysis_data = {
    "Component": ["R1", "R2 (Shared)", "R3", "R4 (Shared)", "R5"],
    "KCL Expression": ["I1", "I1 - I2", "I2", "I2 - I3", "I3"],
    "Current (mA)": [
        f"{I1*1000:.2f}", 
        f"{(I1-I2)*1000:.2f}", 
        f"{I2*1000:.2f}", 
        f"{(I2-I3)*1000:.2f}", 
        f"{I3*1000:.2f}"
    ],
    "Voltage Drop (V)": [
        f"{abs(I1*R1):.2f}", 
        f"{abs((I1-I2)*R2):.2f}", 
        f"{abs(I2*R3):.2f}", 
        f"{abs((I2-I3)*R4):.2f}", 
        f"{abs(I3*R5):.2f}"
    ]
}
st.table(pd.DataFrame(analysis_data))

st.info("**Pedagogical Note:** In Mesh Analysis, the physical current in a shared branch (like R2) is the algebraic difference between the two mesh currents overlapping there. If the result is negative, it simply means the actual current flows opposite to our assumed direction.")
