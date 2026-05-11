# =========================================
# ⚡ OHM'S LAW INTERACTIVE SIMULATOR
# Streamlit App - Basic Electrical Engineering
# =========================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ohm's Law Interactive Simulator",
    page_icon="⚡",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #eaf6ff;
}
.big-font {
    font-size:22px !important;
    font-weight:bold;
    color:#003366;
}
.result-box {
    padding:15px;
    border-radius:12px;
    background-color:#ffffff;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("⚡ Ohm’s Law Interactive Simulator")
st.markdown("### Explore the relationship between Voltage (V), Current (I), and Resistance (R)")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔧 Input Controls")

material = st.sidebar.selectbox(
    "Select Material",
    ["Custom", "Copper", "Nichrome", "Tungsten"]
)

# Preset resistance values
if material == "Copper":
    resistance = st.sidebar.slider("Resistance (Ω)", 1.0, 10.0, 2.0)
elif material == "Nichrome":
    resistance = st.sidebar.slider("Resistance (Ω)", 5.0, 50.0, 20.0)
elif material == "Tungsten":
    resistance = st.sidebar.slider("Resistance (Ω)", 10.0, 100.0, 40.0)
else:
    resistance = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)

voltage = st.sidebar.slider("Voltage (V)", 0.0, 24.0, 12.0)

# ---------------- CALCULATIONS ----------------
current = voltage / resistance if resistance != 0 else 0
power = voltage * current

# ---------------- BULB BRIGHTNESS ----------------
brightness = min(current / 5, 1.0)

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1])

# -------- LEFT PANEL --------
with col1:
    st.subheader("📘 Formula")
    st.latex(r"V = I R")
    st.latex(r"P = V I")

    st.subheader("📊 Calculated Results")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="result-box">
        <h3>Current</h3>
        <h2>{current:.2f} A</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="result-box">
        <h3>Power</h3>
        <h2>{power:.2f} W</h2>
        </div>
        """, unsafe_allow_html=True)

    # Safety Warning
    if current > 5:
        st.error("⚠ Warning: Excessive Current! Fuse May Blow!")
    else:
        st.success("✅ Safe Operating Range")

# -------- RIGHT PANEL --------
# Replace your existing bulb_fig section with this larger bulb indicator

with col2:
    st.subheader("💡 Bulb Brightness Indicator")

    bulb_color = f"rgba(255, 223, 0, {brightness})"

    bulb_fig = go.Figure()

    # Larger bulb circle
    bulb_fig.add_shape(
        type="circle",
        x0=0.15, y0=0.15,
        x1=0.85, y1=0.85,
        fillcolor=bulb_color,
        line_color="black",
        line_width=4
    )

    # Bulb base
    bulb_fig.add_shape(
        type="rect",
        x0=0.42, y0=0.02,
        x1=0.58, y1=0.18,
        fillcolor="gray",
        line_color="black"
    )

    bulb_fig.update_layout(
        width=550,   # Increased width
        height=550,  # Increased height
        xaxis=dict(
            visible=False,
            range=[0, 1]
        ),
        yaxis=dict(
            visible=False,
            range=[0, 1]
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white"
    )

    st.plotly_chart(bulb_fig, use_container_width=True)

# ---------------- V-I GRAPH ----------------
st.subheader("📈 Voltage vs Current Graph")

voltages = np.linspace(0, 24, 50)
currents = voltages / resistance

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=voltages,
    y=currents,
    mode='lines+markers',
    name='V-I Characteristic'
))

fig.update_layout(
    xaxis_title="Voltage (V)",
    yaxis_title="Current (A)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("📋 Observation Table")

data = pd.DataFrame({
    "Voltage (V)": voltages.round(2),
    "Current (A)": currents.round(2)
})

st.dataframe(data, use_container_width=True)

# ---------------- QUIZ SECTION ----------------
st.subheader("🧠 Quick Quiz")

quiz_voltage = 12
quiz_resistance = 4
correct_answer = quiz_voltage / quiz_resistance

user_answer = st.number_input(
    "If Voltage = 12V and Resistance = 4Ω, what is Current (A)?",
    min_value=0.0,
    step=0.1
)

if st.button("Submit Answer"):
    if abs(user_answer - correct_answer) < 0.1:
        st.success("🎉 Correct! Current = 3A")
    else:
        st.error(f"❌ Incorrect! Correct Answer = {correct_answer} A")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("### 🎓 Designed for Basic Electrical Engineering Students")
st.markdown("Explore • Learn • Visualize ⚡")
