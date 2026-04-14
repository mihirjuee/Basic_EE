import streamlit as st
import numpy as np
import schemdraw
import schemdraw.elements as elm
import pandas as pd
import os

# --- Page Config ---
st.set_page_config(
    page_title="Superposition Theorem Lab",
    page_icon="logo.png",
    layout="wide"
)

# --- Logo Loader (safe) ---
def load_logo():
    path = "logo.png"
    return path if os.path.exists(path) else None

logo = load_logo()

# --- Header ---
col1, col2 = st.columns([1, 6])

with col1:
    if logo:
        st.image(logo, width=80)

with col2:
    st.title("⚡ Superposition Theorem Virtual Lab")

if logo:
    st.sidebar.image(logo, use_container_width=True)

st.markdown("""
Analyze circuits with multiple sources using **Superposition Theorem**  
👉 Activate one source at a time (others replaced by internal resistance)
""")

# --- Sidebar Controls ---
st.sidebar.header("🕹️ Circuit Parameters")

V1 = st.sidebar.slider("Voltage Source V1 [V]", 1, 100, 20)
V2 = st.sidebar.slider("Voltage Source V2 [V]", 1, 100, 10)

R1 = st.sidebar.slider("R1 [Ω]", 10, 500, 100)
R2 = st.sidebar.slider("R2 [Ω]", 10, 500, 200)
R3 = st.sidebar.slider("R3 [Ω]", 10, 500, 150)

# --- Superposition Calculations ---

# Case 1: Only V1 active (V2 shorted)
I1_case1 = V1 / (R1 + (R2*R3)/(R2+R3))
V_out1 = I1_case1 * (R2*R3)/(R2+R3)

# Case 2: Only V2 active (V1 shorted)
I2_case2 = V2 / (R3 + (R1*R2)/(R1+R2))
V_out2 = I2_case2 * (R1*R2)/(R1+R2)

# Total response
V_total = V_out1 + V_out2

# --- Circuit Diagram ---
def draw_circuit():
    d = schemdraw.Drawing()
    d.config(unit=3)

    # Left source
    V1_src = d.add(elm.SourceV().label(f'V1\n{V1}V'))
    d.add(elm.Resistor().right().label(f'R1\n{R1}Ω'))

    # Node
    d.add(elm.Dot().label("Output Node", loc='top', color='blue'))

    # Middle branch
    d.push()
    d.add(elm.Resistor().down().label(f'R2\n{R2}Ω'))
    d.add(elm.Ground())
    d.pop()

    # Right branch
    d.add(elm.Resistor().right().label(f'R3\n{R3}Ω'))
    d.add(elm.SourceV().down().label(f'V2\n{V2}V'))

    # Bottom return
    d.add(elm.Line().left().to(V1_src.start))
    d.add(elm.Dot())

    d.save("superposition_circuit.png")

draw_circuit()

# --- Layout ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("🖼️ Circuit Diagram")
    st.image("superposition_circuit.png", use_container_width=True)

with col2:
    st.subheader("📊 Results")

    st.metric("Total Output Voltage", f"{V_total:.2f} V")

    st.markdown("### Contributions")
    st.write(f"🔹 From V1 only: {V_out1:.2f} V")
    st.write(f"🔹 From V2 only: {V_out2:.2f} V")

st.divider()

# --- Step-by-Step Explanation ---
st.subheader("🧠 Step-by-Step Superposition")

st.markdown("### Step 1: Activate V1, Turn OFF V2 (short circuit)")
st.latex(r"V_{out1} = V1 \cdot \frac{R_2 || R_3}{R_1 + (R_2 || R_3)}")

st.markdown("### Step 2: Activate V2, Turn OFF V1")
st.latex(r"V_{out2} = V2 \cdot \frac{R_1 || R_2}{R_3 + (R_1 || R_2)}")

st.markdown("### Step 3: Total Response")
st.latex(r"V_{total} = V_{out1} + V_{out2}")

# --- Table ---
df = pd.DataFrame({
    "Case": ["Only V1 active", "Only V2 active", "Total"],
    "Voltage (V)": [
        f"{V_out1:.2f}",
        f"{V_out2:.2f}",
        f"{V_total:.2f}"
    ]
})

st.table(df)
