import streamlit as st
import numpy as np
import plotly.graph_objects as go
is_mobile = st.sidebar.checkbox("📱 Mobile View", value=True)

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Wheatstone Bridge Pro", page_icon="logo.png", layout="wide")

# ================= DARK UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0e1117, #1c1f26);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("⚡ Wheatstone Bridge – Virtual Lab")

st.latex(r"\frac{R_1}{R_2} = \frac{R_3}{R_4}")

# ================= SIDEBAR =================
st.sidebar.header("🧠 Auto Solve")

unknown = st.sidebar.selectbox(
    "Select Unknown",
    ["None", "R1", "R2", "R3", "R4"]
)

def get_input(name, default):
    if unknown == name:
        return None
    return st.sidebar.number_input(
    f"{name} (Ω)",
    min_value=0.1,
    max_value=1e6,
    value=float(default),
    step=1.0,
    format="%.2f"
)

R1 = get_input("R1", 100.0)
R2 = get_input("R2", 100.0)
R3 = get_input("R3", 100.0)
R4 = get_input("R4", 100.0)

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
        st.error("Invalid values!")

# ================= SHOW VALUES =================
st.sidebar.markdown("### 📌 Values")
def show_value(name, value):
    if unknown == name:
        st.sidebar.markdown(
            f"<span style='color:#ff4b4b; font-weight:bold'>{name} = {value:.2f} Ω</span>",
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown(
            f"<span style='color:#ffffff'>{name} = {value:.2f} Ω</span>",
            unsafe_allow_html=True
        )

show_value("R1", R1)
show_value("R2", R2)
show_value("R3", R3)
show_value("R4", R4)

# ================= CALCULATIONS =================
V_left = Vs * (R3 / (R1 + R3))
V_right = Vs * (R4 / (R2 + R4))

Vg = V_left - V_right
balanced = np.isclose(Vg, 0, atol=1e-4)

# Normalize for gauge
def normalize(v):
    return max(min(v / 5, 1), -1)

needle = normalize(Vg)

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# ================= GAUGE =================
with col1:
    st.subheader("🎥 Galvanometer")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=needle,
        title={'text': "Needle Deflection"},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [-1, -0.2], 'color': "#ff4b4b"},
                {'range': [-0.2, 0.2], 'color': "#00ffcc"},
                {'range': [0.2, 1], 'color': "#ff4b4b"},
            ],
        }
    ))

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ================= RESULTS =================
with col2:
    st.subheader("📊 Results")

    st.metric("Galvanometer Voltage (V)", f"{Vg:.6f}")

    if balanced:
        st.success("Balanced ✅ (Null Deflection)")
    else:
        st.error("Unbalanced ❌")

    st.metric("Error", f"{abs(Vg):.6f} V")

# ================= BALANCE CURVE =================
st.subheader("📈 Balance Curve")

# Safe range (avoid flat-looking graph)
R4_bal = (R2 * R3) / R1 if R1 != 0 else 100

R4_range = np.linspace(0.5*R4_bal, 1.5*R4_bal, 300)

Vg_curve = Vs*(R3/(R1+R3)) - Vs*(R4_range/(R2+R4_range))

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=R4_range,
    y=Vg_curve,
    name="Vg",
    line=dict(width=3)
))

# Zero line
fig2.add_hline(y=0, line_dash="dash", line_width=2)

# Balance point marker
fig2.add_trace(go.Scatter(
    x=[R4_bal],
    y=[0],
    mode="markers+text",
    text=["Balance"],
    textposition="top center",
    marker=dict(size=10)
))

# Improve layout
fig2.update_layout(
    template="plotly_dark",
    height=350 if is_mobile else 450,   # 🔥 IMPORTANT
    margin=dict(l=20, r=20, t=40, b=40),
    xaxis_title="R4 (Ω)",
    yaxis_title="Vg (V)",
)

# Better axis readability
fig2.update_xaxes(showgrid=True)
fig2.update_yaxes(showgrid=True)

st.plotly_chart(fig2, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("⚡ Virtual Electrical Lab")
