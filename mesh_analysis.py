import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd

st.set_page_config(page_title="3-Loop Mesh Analysis", layout="wide")

st.title("🕸️ Interactive 3-Loop Mesh Simulator")

# --- Sidebar: Circuit Parameters ---
st.sidebar.header("🕹️ Circuit Controls")
V1 = st.sidebar.slider("Source Voltage V1 [V]", 5, 100, 40)
V2 = st.sidebar.slider("Source Voltage V2 [V]", 5, 100, 20)
R1 = st.sidebar.slider("R1 (Loop 1) [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("R2 (Shared 1-2) [Ω]", 10, 500, 150)
R3 = st.sidebar.slider("R3 (Loop 2) [Ω]", 10, 500, 100)
R4 = st.sidebar.slider("R4 (Shared 2-3) [Ω]", 10, 500, 200)
R5 = st.sidebar.slider("R5 (Loop 3) [Ω]", 10, 500, 120)

# --- Calculation Engine ---
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
    st.error("Mathematical Error: Matrix is singular.")
    st.stop()

# --- Diagram Generation (FIXED LoopCurrent Syntax) ---
def generate_circuit():
    with schemdraw.Drawing() as d:
        d.config(unit=3, fontsize=10)
        
        # Mesh 1
        L1_V = d.add(elm.SourceV().label(f'V1\n{V1}V'))
        L1_R = d.add(elm.Resistor().right().label(f'R1\n{R1}Ω'))
        R_S1 = d.add(elm.Resistor().down().label(f'R2\n{R2}Ω'))
        L1_B = d.add(elm.Line().left().to(L1_V.start))
        # Pass elements to LoopCurrent to define the loop boundary
        d.add(elm.LoopCurrent([L1_V, L1_R, R_S1, L1_B], direction='cw').label('$I_1$'))
        
        # Mesh 2
        L2_T = d.add(elm.Resistor().right().at(R_S1.start).label(f'R3\n{R3}Ω'))
        R_S2 = d.add(elm.Resistor().down().label(f'R4\n{R4}Ω'))
        L2_B = d.add(elm.Line().left().to(R_S1.end))
        d.add(elm.LoopCurrent([R_S1, L2_T, R_S2, L2_B], direction='cw').label('$I_2$'))
        
        # Mesh 3
        L3_T = d.add(elm.Resistor().right().at(R_S2.start).label(f'R5\n{R5}Ω'))
        L3_V = d.add(elm.SourceV().down().label(f'V2\n{V2}V', loc='bottom'))
        L3_B = d.add(elm.Line().left().to(R_S2.end))
        d.add(elm.LoopCurrent([R_S2, L3_T, L3_V, L3_B], direction='cw').label('$I_3$'))
        
        d.save("mesh_diagram.png")

generate_circuit()

# --- UI Layout ---
col_diag, col_results = st.columns([1.5, 1])

with col_diag:
    st.subheader("🖼️ Circuit Visualization")
    st.image("mesh_diagram.png", use_container_width=True)

with col_results:
    st.subheader("🔢 Results")
    st.metric("Mesh Current I1", f"{I1*1000:.2f} mA")
    st.metric("Mesh Current I2", f"{I2*1000:.2f} mA")
    st.metric("Mesh Current I3", f"{I3*1000:.2f} mA")
    
    st.markdown("---")
    st.latex(r"I_{R2} = I_1 - I_2")
    st.write(f"Current through Shared R2: **{(I1-I2)*1000:.2f} mA**")

# Branch Data Table
st.divider()
analysis_df = pd.DataFrame({
    "Branch": ["R1", "R2 (Shared)", "R3", "R4 (Shared)", "R5"],
    "Current (mA)": [f"{I1*1000:.2f}", f"{(I1-I2)*1000:.2f}", f"{I2*1000:.2f}", f"{(I2-I3)*1000:.2f}", f"{I3*1000:.2f}"]
})
st.table(analysis_df)
