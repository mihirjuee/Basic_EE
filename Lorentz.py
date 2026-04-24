import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="3D Lorentz Force", layout="centered")

st.title("⚡ 3D Lorentz Force Visualization")

st.markdown("""
### 🔹 Vector Relationship:
""")

st.latex(r"\mathbf{F} = I \mathbf{L} \times \mathbf{B}")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
B = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
theta = st.sidebar.slider("Angle between I and B (deg)", 0, 180, 90)

theta_rad = np.radians(theta)

# ================= VECTOR SETUP =================
# Current along x-axis
I_vec = np.array([1, 0, 0]) * I

# Magnetic field in xy-plane at angle θ
B_vec = np.array([
    np.cos(theta_rad),
    np.sin(theta_rad),
    0
]) * B

# Lorentz force (cross product)
F_vec = np.cross(I_vec, B_vec)

# ================= PLOTLY FIGURE =================
fig = go.Figure()

origin = [0, 0, 0]

# Current vector
fig.add_trace(go.Scatter3d(
    x=[0, I_vec[0]],
    y=[0, I_vec[1]],
    z=[0, I_vec[2]],
    mode='lines+markers',
    name='Current (I)',
    line=dict(width=6)
))

# Magnetic field vector
fig.add_trace(go.Scatter3d(
    x=[0, B_vec[0]],
    y=[0, B_vec[1]],
    z=[0, B_vec[2]],
    mode='lines+markers',
    name='Magnetic Field (B)',
    line=dict(width=6)
))

# Force vector
fig.add_trace(go.Scatter3d(
    x=[0, F_vec[0]],
    y=[0, F_vec[1]],
    z=[0, F_vec[2]],
    mode='lines+markers',
    name='Force (F)',
    line=dict(width=6)
))

# Layout
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

# ================= DISPLAY =================
st.plotly_chart(fig, use_container_width=True)

# ================= INFO =================
st.subheader("📘 Results")

st.write("Force Vector:", np.round(F_vec, 2))

st.success("3D Lorentz Force Visualization Ready ⚡")
