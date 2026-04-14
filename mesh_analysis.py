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

# --- Safety ---
if any(r == 0 for r in [R1, R2, R3, R4, R5]):
    st.error("Resistance cannot be zero.")
    st.stop()

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
    with schemdraw.Drawing() as d:
        d.config(unit=3, fontsize=10)

        # LOOP 1
        V_L = elm.SourceV().label(f'V1\n{V1}V')
        d += V_L

        R1_e = elm.Resistor().right().label(f'R1\n{R1}Ω')
        d += R1_e

        R_S1 = elm.Resistor().down().label(f'R2\n{R2}Ω')
        d += R_S1

        L1 = elm.Line().left().to(V_L.start)
        d += L1

        # 🔴 Circular Arrow
        d += elm.ArcArrow(radius=0.7, theta1=20, theta2=340, color=color1).at((1.5, -0.6))
        d += elm.Label().at((1.5, -1.4)).label('$I_1$', color=color1)

        # LOOP 2
        R3_e = elm.Resistor().right().at(R_S1.start).label(f'R3\n{R3}Ω')
        d += R3_e

        R_S2 = elm.Resistor().down().label(f'R4\n{R4}Ω')
        d += R_S2

        L2 = elm.Line().left().to(R_S1.end)
        d += L2

        # 🟢 Circular Arrow
        d += elm.ArcArrow(radius=0.7, theta1=20, theta2=340, color=color2).at((4.5, -0.6))
        d += elm.Label().at((4.5, -1.4)).label('$I_2$', color=color2)

        # LOOP 3
        R5_e = elm.Resistor().right().at(R_S2.start).label(f'R5\n{R5}Ω')
        d += R5_e

        V_R = elm.SourceV().down().label(f'V2\n{V2}V')
        d += V_R

        L3 = elm.Line().left().to(R_S2.end)
        d += L3

        # 🔵 Circular Arrow
        d += elm.ArcArrow(radius=0.7, theta1=20, theta2=340, color=color3).at((7.5, -0.6))
        d += elm.Label().at((7.5, -1.4)).label('$I_3$', color=color3)

        # Shared currents
        d += elm.CurrentLabel().at(R_S1).label(f'{(I1-I2)*1000:.1f} mA')
        d += elm.CurrentLabel().at(R_S2).label(f'{(I2-I3)*1000:.1f} mA')

        d.save("mesh.png")

draw_circuit()

# --- Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🖼️ Circuit Diagram")
    st.image("mesh.png", use_container_width=True)

with col2:
    st.subheader("🔢 Results")
    st.metric("I1", f"{I1*1000:.2f} mA")
    st.metric("I2", f"{I2*1000:.2f} mA")
    st.metric("I3", f"{I3*1000:.2f} mA")

# --- Animation ---
if animate:
    st.subheader("⚡ Current Animation")
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i+1)
        time.sleep(0.01)

# --- KVL ---
st.divider()
st.subheader("🧠 KVL Equations")

st.latex(f"I_1({R1}+{R2}) - I_2({R2}) = {V1}")
st.latex(f"-I_1({R2}) + I_2({R2}+{R3}+{R4}) - I_3({R4}) = 0")
st.latex(f"-I_2({R4}) + I_3({R4}+{R5}) = -{V2}")

# --- Table ---
st.divider()
st.subheader("📋 Branch Analysis")

df = pd.DataFrame({
    "Component": ["R1", "R2", "R3", "R4", "R5"],
    "Current (mA)": [
        I1*1000,
        (I1-I2)*1000,
        I2*1000,
        (I2-I3)*1000,
        I3*1000
    ],
    "Voltage (V)": [
        abs(I1*R1),
        abs((I1-I2)*R2),
        abs(I2*R3),
        abs((I2-I3)*R4),
        abs(I3*R5)
    ]
})

st.table(df)

# --- Power ---
st.subheader("⚡ Power Dissipation")

power_df = pd.DataFrame({
    "Component": ["R1", "R2", "R3", "R4", "R5"],
    "Power (W)": [
        I1**2 * R1,
        (I1-I2)**2 * R2,
        I2**2 * R3,
        (I2-I3)**2 * R4,
        I3**2 * R5
    ]
})

st.table(power_df)

# --- Quiz ---
if quiz_mode:
    st.divider()
    st.subheader("🎓 Quiz Mode")

    guess = st.number_input("Guess I1 (mA)")

    if st.button("Check Answer"):
        if abs(guess - I1*1000) < 5:
            st.success("Correct! 🎉")
        else:
            st.error("Try again!")

# --- Footer ---
st.info("Shared branch current = difference of mesh currents. Negative means opposite direction.")
