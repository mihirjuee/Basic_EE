import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Wheatstone Bridge Pro", layout="wide")

# ================= MOBILE DETECTION =================
is_mobile = st.sidebar.checkbox("📱 Mobile View", value=True)

# ================= DARK UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0e1117, #1c1f26);
    color: white;
}

/* Bigger buttons & inputs for mobile */
div[data-baseweb="input"] input {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("⚡ Wheatstone Bridge")
st.caption("Virtual Lab Simulator")

st.latex(r"\frac{R_1}{R_2} = \frac{R_3}{R_4}")

# ================= INPUT =================
st.sidebar.header("🧠 Auto Solve")

unknown = st.sidebar.selectbox(
    "Unknown",
    ["None", "R1", "R2", "R3", "R4"]
)

def get_input(name, default):
    if unknown == name:
        return None
    if is_mobile:
        return st.sidebar.number_input(f"{name} (Ω)", value=default)
    else:
        return st.sidebar.slider(f"{name} (Ω)", 1.0, 1000.0, default)

R1 = get_input("R1", 100.0)
R2 = get_input("R2", 100.0)
R3 = get_input("R3", 100.0)
R4 = get_input("R4", 100.0)

Vs = st.sidebar.number_input("Voltage (V)", value=10.0)

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
        st.error("Invalid values")

# ================= CALC =================
V_left = Vs * (R3 / (R1 + R3))
V_right = Vs * (R4 / (R2 + R4))
Vg = V_left - V_right
balanced = abs(Vg) < 1e-4

def normalize(v):
    return max(min(v / 5, 1), -1)

needle = normalize(Vg)

# ================= LAYOUT =================
if is_mobile:
    col1 = st.container()
    col2 = st.container()
else:
    col1, col2 = st.columns(2)

# ================= DIAGRAM =================
with col1:
    st.subheader("🔌 Bridge")

    top = (0, 2)
    right = (2, 0)
    bottom = (0, -2)
    left = (-2, 0)

    fig = go.Figure()

    def branch(p1, p2, label):
        fig.add_trace(go.Scatter(
            x=[p1[0], p2[0]],
            y=[p1[1], p2[1]],
            mode='lines+text',
            line=dict(width=4),
            text=[label],
            textposition="middle center"
        ))

    branch(top, left, f"R1\n{R1:.0f}")
    branch(top, right, f"R2\n{R2:.0f}")
    branch(left, bottom, f"R3\n{R3:.0f}")
    branch(right, bottom, f"R4\n{R4:.0f}")

    # Galvanometer
    fig.add_trace(go.Scatter(
        x=[left[0], right[0]],
        y=[left[1], right[1]],
        mode='lines+text',
        line=dict(width=3, dash='dot'),
        text=["G"],
        textposition="middle center"
    ))

    # Source
    fig.add_trace(go.Scatter(
        x=[top[0], bottom[0]],
        y=[top[1], bottom[1]],
        mode='lines+text',
        line=dict(width=3, dash='dash'),
        text=[f"{Vs}V"],
        textposition="top center"
    ))

    # Nodes
    for p in [top, right, bottom, left]:
        fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode='markers'))

    fig.update_layout(
        template="plotly_dark",
        height=350 if is_mobile else 500,
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= GAUGE =================
with col2:
    st.subheader("🎥 Galvanometer")

    fig_g = go.Figure(go.Indicator(
        mode="gauge+number",
        value=needle,
        gauge={'axis': {'range': [-1, 1]}}
    ))

    fig_g.update_layout(
        template="plotly_dark",
        height=250 if is_mobile else 400
    )

    st.plotly_chart(fig_g, use_container_width=True)

# ================= RESULTS =================
st.subheader("📊 Results")

if is_mobile:
    st.metric("Vg (V)", f"{Vg:.5f}")
    st.metric("Status", "Balanced" if balanced else "Unbalanced")
else:
    c1, c2 = st.columns(2)
    c1.metric("Vg (V)", f"{Vg:.5f}")
    c2.metric("Status", "Balanced" if balanced else "Unbalanced")

# ================= GRAPH =================
st.subheader("📈 Curve")

R4_range = np.linspace(1, max(2*R4, 200), 200)
Vg_curve = Vs*(R3/(R1+R3)) - Vs*(R4_range/(R2+R4_range))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=R4_range, y=Vg_curve))
fig2.add_hline(y=0)

fig2.update_layout(
    template="plotly_dark",
    height=300 if is_mobile else 400
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("⚡ Mobile Optimized Virtual Lab")
