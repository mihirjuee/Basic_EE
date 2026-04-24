import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(page_title="3D Lorentz Force", layout="wide")

st.title("⚡ 3D Lorentz Force Visualization")
st.latex(r"\mathbf{F} = I (\mathbf{L} \times \mathbf{B})")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")
I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
L = st.sidebar.slider("Wire Length (L)", 0.1, 5.0, 1.0)
B = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
theta = st.sidebar.slider("Angle between L and B (deg)", 0, 180, 90)

theta_rad = np.radians(theta)

# ================= PHYSICS CALCULATION =================
# L along x-axis
L_vec = np.array([L, 0, 0])
# B in xy-plane
B_vec = np.array([np.cos(theta_rad), np.sin(theta_rad), 0]) * B
# F = I * (L x B)
F_vec = I * np.cross(L_vec, B_vec)

# ================= PLOTLY FIGURE =================
fig = go.Figure()

def add_vector(fig, vec, name, color):
    # Line
    fig.add_trace(go.Scatter3d(
        x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]],
        mode='lines', name=name,
        line=dict(color=color, width=6)
    ))
    # Arrow head
    fig.add_trace(go.Cone(
        x=[vec[0]], y=[vec[1]], z=[vec[2]],
        u=[vec[0]], v=[vec[1]], w=[vec[2]],
        sizemode="absolute", sizeref=0.5,
        colorscale=[[0, color], [1, color]], showscale=False
    ))

add_vector(fig, L_vec, 'Wire Length (L)', 'blue')
add_vector(fig, B_vec, 'Magnetic Field (B)', 'green')
add_vector(fig, F_vec, 'Force (F)', 'red')

# Fixed Axis for stability
limit = 10
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-limit, limit]),
        yaxis=dict(range=[-limit, limit]),
        zaxis=dict(range=[-limit, limit]),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# ================= INFO =================
col1, col2 = st.columns(2)
with col1:
    st.subheader("📘 Calculations")
    st.write(f"**Calculated Force Magnitude:** {np.linalg.norm(F_vec):.2f} N")
    st.write(f"**Force Vector (x, y, z):** {np.round(F_vec, 2)}")

with col2:
    st.subheader("💡 Physics Note")
    st.markdown("""
    The direction of the force is determined by the **Right-Hand Rule**:
    1. Point fingers in direction of **L**.
    2. Curl fingers toward **B**.
    3. The thumb points in the direction of **F**.
    """)
    

[Image of the right-hand rule for magnetic force]
