import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="3-Loop Mesh Analysis", layout="wide")

st.title("🕸️ Interactive 3-Loop Mesh Simulator")
st.markdown("""
This tool solves a 3-loop resistive network using **Matrix-based Mesh Analysis**. 
Adjust the sliders to observe how shared branch currents are calculated.
""")

# 2. Sidebar: Circuit Parameters
st.sidebar.header("🕹️ Circuit Controls")
V1 = st.sidebar.slider("Source Voltage V1 [V]", 5, 100, 40)
V2 = st.sidebar.slider("Source Voltage V2 [V]", 5, 100, 20)
R1 = st.sidebar.slider("R1 (Loop 1) [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("R2 (Shared 1-2) [Ω]", 10, 500, 150)
R3 = st.sidebar.slider("R3 (Loop 2) [Ω]", 10, 500, 100)
R4 = st.sidebar.slider("R4 (Shared 2-3) [Ω]", 10, 500, 200)
R5 = st.sidebar.slider("R5 (Loop 3) [Ω]", 10, 500, 120)

# 3. Calculation Engine (Solving the 3x3 Matrix)
# Matrix Equation: [R][I] = [V]
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
    st.error("Mathematical Error: The system of equations cannot be solved. Check resistor values.")
    st.stop()

# 4. Diagram Generation
def generate_circuit():
    with schemdraw.Drawing() as d:
        d.config(unit=3, fontsize=10)
        
        # --- Mesh 1 ---
        V_L = d.add(elm.SourceV().label(f'V1\n{V1}V'))
        d.add(elm.Resistor().right().label(f'R1\n{R1}Ω'))
        R_S1 = d.add(elm.Resistor().down().label(f'R2\n{R2}Ω'))
        d.add(elm.Line().left().to(V_L.start))
        # Loop Current I1
        d.add(elm.LoopCurrent(direction='cw').at(R_S1).label('$I_1$'))
        
        # --- Mesh 2 ---
        d.add(elm.Resistor().right().at(R_S1.start).label(f'R3\n{R3}Ω'))
        R_S2 = d.add(elm.Resistor().down().label(f'R4\n{R4}Ω'))
        d.add(elm.Line().left().to(R_S1.end))
        # Loop Current I2
        d.add(elm.LoopCurrent(direction='cw').at(R_S2).label('$I_2$'))
        
        # --- Mesh 3 ---
        d.add(elm.Resistor().right().at(R_S2.start).label(f'R5\n{R5}Ω'))
        V_R = d.add(elm.SourceV().down().label(f'V2\n{V2}V', loc='bottom'))
        d.add(elm.Line().left().to(R_S2.end))
        # Loop Current I3
        d.add(elm.LoopCurrent(direction='cw').at(V_R).label('$I_3$'))
        
        d.save("mesh_diagram.png")

generate_circuit()

# 5. UI Layout
col_diag, col_results = st.columns([1.5, 1])

with col_diag:
    st.subheader("🖼️ Circuit Visualization")
    st.image("mesh_diagram.png", use_container_width=True)
    st.caption("The circular arrows represent our clockwise Mesh Current assumptions.")

with col_results:
    st.subheader("🔢 Mesh Current Results")
    st.metric("Mesh Current I1", f"{I1*1000:.2f} mA")
    st.metric("Mesh Current I2", f"{I2*1000:.2f} mA")
    st.metric("Mesh Current I3", f"{I3*1000:.2f} mA")
    
    st.markdown("---")
    st.subheader("📝 System Matrix")
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

st.divider()

# 6. Detailed Branch Data
st.subheader("📋 Branch Current & Voltage Analysis")
analysis_df = pd.DataFrame({
    "Branch": ["R1", "R2 (Shared)", "R3", "R4 (Shared)", "R5"],
    "Current Formula": ["I1", "I1 - I2", "I2", "I2 - I3", "I3"],
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
})
st.table(analysis_df)

st.info("**Quick Tip:** A negative branch current simply means the real current flows in the opposite direction of our assumed mesh loop.")
