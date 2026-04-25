import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= PAGE =================
st.set_page_config(page_title="Lorentz Force + Right Hand Rule", layout="wide")

st.title("⚡ 3D Lorentz Force with Right-Hand Rule")

st.latex(r"\mathbf{F} = I (\mathbf{L} \times \mathbf{B})")

st.markdown("""
### 🧠 Right-Hand Rule:
- 👉 Index finger → **Current (L)**
- 👉 Middle finger → **Magnetic Field (B)**
- 👉 Thumb → **Force (F)**
""")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
L = st.sidebar.slider("Wire Length (L)", 0.1, 5.0, 2.0)
B = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
theta = st.sidebar.slider("Angle of Wire (deg)", 0, 180, 60)

theta_rad = np.radians(theta)

# ================= PHYSICS (CORRECT MODEL) =================

# Wire direction (rotated in X–Z plane)
L_vec = np.array([
    L * np.cos(theta_rad),
    0,
    L * np.sin(theta_rad)
])

# Magnetic field fixed along Y-axis (standard textbook setup)
B_vec = np.array([0, B, 0])

# Lorentz force
F_vec = I * np.cross(L_vec, B_vec)

# ================= PLOT FUNCTION =================
fig = go.Figure()

def add_vector(vec, name, color):
    fig.add_trace(go.Scatter3d(
        x=[0, vec[0]],
        y=[0, vec[1]],
        z=[0, vec[2]],
        mode='lines+markers',
        name=name,
        line=dict(color=color, width=8)
    ))

    # Arrow head (direction only)
    norm = np.linalg.norm(vec) + 1e-9
    direction = vec / norm

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
        showscale=False,
        colorscale=[[0, color], [1, color]]
    ))

# ================= DRAW VECTORS =================
add_vector(L_vec, "Current Direction (L)", "blue")
add_vector(B_vec, "Magnetic Field (B)", "green")
add_vector(F_vec, "Force (F)", "red")

# ================= AXIS =================
limit = 6

fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-limit, limit], title="X"),
        yaxis=dict(range=[-limit, limit], title="Y"),
        zaxis=dict(range=[-limit, limit], title="Z"),
        aspectmode="cube"
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    legend=dict(x=0.75, y=0.9)
)

st.plotly_chart(fig, use_container_width=True)

# ================= RESULTS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Force Magnitude (N)", f"{np.linalg.norm(F_vec):.3f}")

with col2:
    st.metric("Force X", f"{F_vec[0]:.3f}")
    st.metric("Force Y", f"{F_vec[1]:.3f}")

with col3:
    st.metric("Force Z", f"{F_vec[2]:.3f}")

# ================= EXPLANATION =================
st.subheader("💡 Physics Explanation")

st.markdown("""
✔ Current (L) is along the wire direction  
✔ Magnetic field (B) is perpendicular (Y-axis)  
✔ Force (F) is perpendicular to both  

👉 This follows the **Right-Hand Rule** exactly:
- Index → L  
- Middle → B  
- Thumb → F  
""")

# ================= EXTRA INSIGHT =================
if np.linalg.norm(F_vec) < 1e-3:
    st.warning("Force is nearly zero → L is parallel to B")
else:
    st.success("Non-zero force → mechanical motion possible ⚡")
