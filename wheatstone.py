import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE =================
st.set_page_config(page_title="Wheatstone Bridge Pro+", layout="wide")

st.title("⚡ Wheatstone Bridge – Animated Lab Simulator")

st.latex(r"\frac{R_1}{R_2} = \frac{R_3}{R_4}")

# ================= SIDEBAR =================
st.sidebar.header("🧠 Auto Solve Mode")

unknown = st.sidebar.selectbox(
    "Select Unknown Resistor",
    ["None", "R1", "R2", "R3", "R4"]
)

def input_resistor(name, default):
    if unknown == name:
        return None
    return st.sidebar.slider(f"{name} (Ω)", 1.0, 1000.0, default)

R1 = input_resistor("R1", 100.0)
R2 = input_resistor("R2", 100.0)
R3 = input_resistor("R3", 100.0)
R4 = input_resistor("R4", 100.0)

Vs = st.sidebar.slider("Supply Voltage (V)", 1.0, 50.0, 10.0)

# ================= AUTO SOLVE =================
if unknown != "None":
    try:
        if unknown == "R1":
            R1 = (R2 * R3) / R4
        elif unknown == "R2":
            R2 = (R1 * R4) / R3
        elif unknown == "R3":
            R3 = (R1 * R4) / R2
        elif unknown == "R4":
            R4 = (R2 * R3) / R1
    except:
        st.error("Invalid values for solving")

# ================= DISPLAY VALUES =================
st.sidebar.markdown("### 📌 Current Values")
st.sidebar.write(f"R1 = {R1:.2f} Ω")
st.sidebar.write(f"R2 = {R2:.2f} Ω")
st.sidebar.write(f"R3 = {R3:.2f} Ω")
st.sidebar.write(f"R4 = {R4:.2f} Ω")

# ================= CALCULATION =================
V_left = Vs * (R3 / (R1 + R3))
V_right = Vs * (R4 / (R2 + R4))

Vg = V_left - V_right
balanced = np.isclose(Vg, 0, atol=1e-4)

# ================= LAYOUT =================
col1, col2 = st.columns([1,1])

# ================= ANALOG GAUGE =================
with col1:
    st.subheader("🎥 Galvanometer (Analog)")

    gauge_placeholder = st.empty()

    # Normalize for display (-1 to 1)
    def normalize(v):
        return max(min(v/5, 1), -1)

    target = normalize(Vg)

    # Animate needle
    for val in np.linspace(0, target, 30):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            title={'text': "Needle Deflection"},
            gauge={
                'axis': {'range': [-1, 1]},
                'bar': {'thickness': 0.3},
            }
        ))
        fig.update_layout(template="plotly_dark")
        gauge_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.02)

# ================= RESULTS =================
with col2:
    st.subheader("📊 Results")

    st.metric("Galvanometer Voltage (V)", f"{Vg:.5f}")

    if balanced:
        st.success("Perfect Balance ✅ (Null Deflection)")
    else:
        st.warning("Unbalanced ⚠️")

    st.metric("Balance Error", f"{abs(Vg):.6f} V")

# ================= BALANCE CURVE =================
st.subheader("📈 Balance Curve")

R4_range = np.linspace(1, 2*R4 if R4 else 200, 200)
Vg_curve = Vs*(R3/(R1+R3)) - Vs*(R4_range/(R2+R4_range))

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=R4_range,
    y=Vg_curve,
    name="Vg"
))

fig2.add_hline(y=0, line_dash="dash")
fig2.update_layout(template="plotly_dark")

st.plotly_chart(fig2, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("⚡ Advanced Virtual Lab Instrument")
