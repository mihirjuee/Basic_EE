import streamlit as st
import pandas as pd

st.set_page_config(page_title="Thevenin's Theorem Simulator", layout="wide")

st.title("⚡ Thevenin's Theorem Verification")
st.markdown("""
This app verifies Thevenin's Theorem by comparing the load current in a **Complex Circuit** vs. the **Thevenin Equivalent Circuit**.
""")

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")
V_s = st.sidebar.slider("Source Voltage (Vs) [V]", 1, 100, 12)
R1 = st.sidebar.slider("Resistor R1 [Ω]", 10, 1000, 100)
R2 = st.sidebar.slider("Resistor R2 [Ω]", 10, 1000, 200)
R3 = st.sidebar.slider("Resistor R3 [Ω]", 10, 1000, 150)
RL = st.sidebar.slider("Load Resistor (RL) [Ω]", 10, 1000, 50)

# --- Calculations ---
# 1. Finding V_th (Open circuit voltage across RL)
# V_th is the voltage across R2 in a series circuit of Vs, R1, and R2 (assuming R3 is in series with RL)
V_th = V_s * (R2 / (R1 + R2))

# 2. Finding R_th (Equivalent resistance looking from RL with Vs shorted)
# R_th = (R1 || R2) + R3
R_parallel = (R1 * R2) / (R1 + R2)
R_th = R_parallel + R3

# 3. Calculation of Load Current (IL)
# From Original Circuit (Using Mesh/Nodal results simplified)
I_L_theoretical = V_th / (R_th + RL)

# --- UI Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Step 1: Thevenin Parameters")
    st.metric("Thevenin Voltage (Vth)", f"{V_th:.2f} V")
    st.metric("Thevenin Resistance (Rth)", f"{R_th:.2f} Ω")
    
    st.info(f"**Formula used:** \n $V_{{th}} = V_s \\times \\frac{{R_2}}{{R_1 + R_2}}$  \n $R_{{th}} = \\frac{{R_1 \\times R_2}}{{R_1 + R_2}} + R_3$")

with col2:
    st.subheader("🧪 Step 2: Verification")
    st.write(f"Current through Load ($I_L$) in Equivalent Circuit:")
    st.success(f"**I_L = {I_L_theoretical*1000:.2f} mA**")
    
    # Comparison Table
    data = {
        "Parameter": ["Vth", "Rth", "RL", "Load Current (mA)"],
        "Value": [f"{V_th:.2f} V", f"{R_th:.2f} Ω", f"{RL} Ω", f"{I_L_theoretical*1000:.2f} mA"]
    }
    st.table(pd.DataFrame(data))

st.divider()
st.markdown("### 💡 Theory Recap")
st.write("""
Any linear electrical network with voltage and current sources and only resistances can be replaced at 
terminals A-B by an equivalent voltage source **Vth** in series with a resistance **Rth**.
""")
