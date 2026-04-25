import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="3D Lorentz Force", layout="wide")

st.title("⚡ 3D Lorentz Force Visualization")

st.latex(r"\mathbf{F} = I (\mathbf{L} \times \mathbf{B})")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
L = st.sidebar.slider("Wire Length (L)", 0.1, 5.0, 2.0)
B = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
theta = st.sidebar.slider("Angle between L and B (deg)", 0, 180, 90)

theta_rad = np.radians(theta)

# ================= PHYSICS =================
L_vec = np.array([L, 0, 0])

B_vec = np.array([
    np.cos(theta_rad),
    np.sin(theta_rad),
    0
]) * B

F_vec = I * np.cross(L_vec, B_vec)

# ================= NORMALIZATION FOR VISUAL =================
scale = 2
L_vis = L_vec * scale
B_vis = B_vec * scale
F_vis = F_vec * scale

# ================= FIGURE =================
fig = go.Figure()

def add_vector(vec, name, color):
    fig.add_trace(go.Scatter3d(
        x=[0, vec[0]],
        y=[0, vec[1]],
        z=[0, vec[2]],
        mode='lines',
        name=name,
        line=dict(color=color, width=8)
    ))

    # Proper arrow (direction only, not full magnitude again)
    direction = vec / (np.linalg.norm(vec) + 1e-9)

    fig.add_trace(go.Cone(
        x=[vec[0]],
        y=[vec[1]],
        z=[vec[2]],
        u=[direction[0]],
        v=[direction[1]],
        w=[direction[2]],
        sizemode="absolute",
        sizeref=0.5,
        anchor="tail",
        colorscale=[[0, color], [1, color]],
        showscale=False
    ))

# Vectors
add_vector(L_vis, "Current Length (L)", "blue")
add_vector(B_vis, "Magnetic Field (B)", "green")
add_vector(F_vis, "Force (F)", "red")

# ================= LAYOUT =================
limit = 8

fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-limit, limit], title="X"),
        yaxis=dict(range=[-limit, limit], title="Y"),
        zaxis=dict(range=[-limit, limit], title="Z"),
        aspectmode="cube"
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    legend=dict(x=0.8, y=0.9)
)

st.plotly_chart(fig, use_container_width=True)

# ================= RESULTS =================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📘 Results")
    st.write("Force Magnitude:", round(np.linalg.norm(F_vec), 3), "N")
    st.write("Force Vector:", np.round(F_vec, 3))

with col2:
    st.subheader("💡 Interpretation")
    st.markdown("""
- Blue → Current direction (L)  
- Green → Magnetic field (B)  
- Red → Force (F = I × L × B)  

👉 Force is always perpendicular to both L and B
""")
