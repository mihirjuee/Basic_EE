import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE SETUP =================
st.set_page_config(page_title="Lorentz Force 3D", layout="wide")

st.title("⚡ 3D Lorentz Force Visualization")
st.latex(r"\mathbf{F} = I (\mathbf{L} \times \mathbf{B})")

# ================= INPUT =================
st.sidebar.header("🔧 Physics Controls")
I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
L = st.sidebar.slider("Wire Length (L)", 0.1, 5.0, 2.0)
B_mag = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
theta = st.sidebar.slider("Angle of Wire (deg)", 0, 180, 60)

theta_rad = np.radians(theta)

# ================= PHYSICS ENGINE =================
L_vec = np.array([L * np.cos(theta_rad), 0, L * np.sin(theta_rad)])
B_vec = np.array([0, B_mag, 0])
F_vec = I * np.cross(L_vec, B_vec)

# ================= PLOT GENERATION =================
fig = go.Figure()

# 1. Helper function for vectors
def add_vector(vec, name, color):
    # Line
    fig.add_trace(go.Scatter3d(
        x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]],
        mode='lines', name=name,
        line=dict(color=color, width=6)
    ))
    # Arrowhead
    fig.add_trace(go.Cone(
        x=[vec[0]], y=[vec[1]], z=[vec[2]],
        u=[vec[0]], v=[vec[1]], w=[vec[2]],
        sizemode="absolute", sizeref=0.5, anchor="tail",
        showscale=False, colorscale=[[0, color], [1, color]]
    ))

# 2. Add vectors
add_vector(L_vec, "Current (L)", "blue")
add_vector(B_vec, "Magnetic Field (B)", "green")
add_vector(F_vec, "Force (F)", "red")

# 3. Add origin and helper plane
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', 
                           marker=dict(size=4, color='black'), name="Origin"))

# Plane showing the surface spanned by L and B
fig.add_trace(go.Mesh3d(
    x=[0, L_vec[0], L_vec[0], 0],
    y=[0, 0, B_vec[1], B_vec[1]],
    z=[0, L_vec[2], L_vec[2], 0],
    opacity=0.15, color='gray', name="L-B Plane"
))

# ================= LAYOUT =================
limit = max(L, B_mag, np.linalg.norm(F_vec)) + 1
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-limit, limit], title="X"),
        yaxis=dict(range=[-limit, limit], title="Y"),
        zaxis=dict(range=[-limit, limit], title="Z"),
        aspectmode="cube"
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    legend=dict(x=0.05, y=0.95)
)

st.plotly_chart(fig, use_container_width=True)

# ================= METRICS =================
c1, c2, c3 = st.columns(3)
c1.metric("Force Magnitude (N)", f"{np.linalg.norm(F_vec):.2f}")
c2.metric("Force Vector (X, Y, Z)", f"({F_vec[0]:.1f}, {F_vec[1]:.1f}, {F_vec[2]:.1f})")
c3.metric("Status", "Force Active" if np.linalg.norm(F_vec) > 0.1 else "Parallel/Zero")

st.info("The **Gray Plane** represents the plane containing the Current and Magnetic Field vectors. The Force vector is always perpendicular to this plane.")
