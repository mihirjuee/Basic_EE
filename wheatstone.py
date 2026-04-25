import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm

# ================= PAGE =================
st.set_page_config(page_title="Wheatstone Bridge Pro", layout="wide")

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
    return st.sidebar.slider(f"{name} (Ω)", 1.0, 1000.0, default)

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

# ================= CALCULATIONS =================
V_left = Vs * (R3 / (R1 + R3))
V_right = Vs * (R4 / (R2 + R4))
Vg = V_left - V_right
balanced = np.isclose(Vg, 0, atol=1e-4)

def normalize(v):
    return max(min(v / 5, 1), -1)

needle = normalize(Vg)

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# ================= CIRCUIT =================
# ================= CIRCUIT =================
with col1:
    st.subheader("🔌 Bridge Circuit")

    d = schemdraw.Drawing()

    # Top left node
    d += elm.Dot()
    
    # R1 (top left to top right)
    d += elm.Resistor().right().label(f"R1\n{R1:.1f}Ω")
    d += elm.Dot()
    top_right = d.here

    # R2 (top right to bottom right)
    d += elm.Resistor().down().label(f"R2\n{R2:.1f}Ω")
    d += elm.Dot()
    bottom_right = d.here

    # Bottom wire (right to left)
    d += elm.Line().left(3)

    # R3 (bottom left to top left)
    d += elm.Resistor().up().label(f"R3\n{R3:.1f}Ω")
    d += elm.Dot()
    top_left = d.here

    # Voltage source (left vertical)
    d += elm.SourceV().down().label(f"{Vs}V")

    # -------- Galvanometer branch --------
    d.push()
    d += elm.Line().at(top_left).to(top_right)
    d += elm.Meter().label("G")
    d.pop()

    st.pyplot(d.draw())
# ================= GAUGE =================
with col2:
    st.subheader("🎥 Galvanometer")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=needle,
        title={'text': "Needle Deflection"},
        gauge={
            'axis': {'range': [-1, 1]},
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
st.subheader("📊 Results")

col3, col4 = st.columns(2)

with col3:
    st.metric("Galvanometer Voltage (V)", f"{Vg:.6f}")

with col4:
    if balanced:
        st.success("Balanced ✅")
    else:
        st.error("Unbalanced ❌")

# ================= GRAPH =================
st.subheader("📈 Balance Curve")

R4_range = np.linspace(1, max(2*R4, 200), 200)
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
st.markdown("⚡ Virtual Electrical Lab")
