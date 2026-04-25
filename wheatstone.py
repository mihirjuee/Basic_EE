import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Wheatstone Bridge Pro", layout="wide")

# ================= CUSTOM STYLING =================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0e1117, #1c1f26); color: white; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Wheatstone Bridge")
st.latex(r"\frac{R_1}{R_2} = \frac{R_3}{R_4}")

# ================= SIDEBAR INPUTS =================
st.sidebar.header("🧠 Parameters")
is_mobile = st.sidebar.checkbox("📱 Mobile View", value=True)
unknown = st.sidebar.selectbox("Unknown Variable", ["None", "R1", "R2", "R3", "R4"])

def get_input(name, default):
    if unknown == name: return None
    return st.sidebar.number_input(f"{name} (Ω)", value=default) if is_mobile \
           else st.sidebar.slider(f"{name} (Ω)", 1.0, 1000.0, default)

R1, R2, R3, R4 = [get_input(n, 100.0) for n in ["R1", "R2", "R3", "R4"]]
Vs = st.sidebar.number_input("Supply Voltage (V)", value=10.0)

# ================= AUTO SOLVE LOGIC =================
if unknown != "None":
    if unknown == "R1": R1 = (R2 * R3) / R4
    elif unknown == "R2": R2 = (R1 * R4) / R3
    elif unknown == "R3": R3 = (R1 * R4) / R2
    elif unknown == "R4": R4 = (R2 * R3) / R1

# ================= CALCULATIONS =================
V_left = Vs * (R3 / (R1 + R3))
V_right = Vs * (R4 / (R2 + R4))
Vg = V_left - V_right
balanced = abs(Vg) < 1e-3

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# ================= CIRCUIT DIAGRAM =================
with col1:
    st.subheader("🔌 Bridge Circuit")
    fig = go.Figure()
    # Nodes: Top(0,2), Bottom(0,-2), Left(-2,0), Right(2,0)
    nodes = {'T': (0, 2), 'B': (0, -2), 'L': (-2, 0), 'R': (2, 0)}
    
    def add_line(p1, p2, text, color="white", dash="solid"):
        fig.add_trace(go.Scatter(x=[p1[0], p2[0]], y=[p1[1], p2[1]], mode='lines+text',
                                 line=dict(width=3, color=color, dash=dash),
                                 text=[None, text], textposition="middle center"))

    add_line(nodes['T'], nodes['L'], f"R1: {R1:.0f}Ω")
    add_line(nodes['T'], nodes['R'], f"R2: {R2:.0f}Ω")
    add_line(nodes['L'], nodes['B'], f"R3: {R3:.0f}Ω")
    add_line(nodes['R'], nodes['B'], f"R4: {R4:.0f}Ω")
    add_line(nodes['L'], nodes['R'], "G", color="yellow", dash="dot")

    fig.add_trace(go.Scatter(x=[0, 0, -2, 2], y=[2, -2, 0, 0], mode='markers', marker=dict(size=12)))
    fig.update_layout(template="plotly_dark", height=400, xaxis=dict(range=[-3, 3], visible=False), 
                      yaxis=dict(range=[-3, 3], visible=False), showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# ================= GAUGE & RESULTS =================
with col2:
    st.subheader("🎥 Galvanometer")
    fig_g = go.Figure(go.Indicator(mode="gauge+number", value=Vg, gauge={'axis': {'range': [-5, 5]}}))
    fig_g.update_layout(template="plotly_dark", height=250)
    st.plotly_chart(fig_g, use_container_width=True)
    
    st.metric("Galvanometer Voltage (V)", f"{Vg:.4f}")
    st.success("Balanced") if balanced else st.error("Unbalanced")

# ================= CURVE =================
st.subheader("📈 Balance Curve")
R4_range = np.linspace(1, 500, 100)
Vg_curve = Vs*(R3/(R1+R3)) - Vs*(R4_range/(R2+R4_range))
fig2 = go.Figure(go.Scatter(x=R4_range, y=Vg_curve))
fig2.add_hline(y=0, line_dash="dash", line_color="red")
fig2.update_layout(template="plotly_dark", height=300)
st.plotly_chart(fig2, use_container_width=True)
