import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE =================
st.set_page_config(page_title="Lorentz Force Animation", layout="wide")

st.title("⚡ Animated Lorentz Force (Wire Motion)")

st.latex(r"\mathbf{F} = I (\mathbf{L} \times \mathbf{B})")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
L = st.sidebar.slider("Wire Length (L)", 1.0, 5.0, 2.0)
B = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
theta = st.sidebar.slider("Angle (deg)", 0, 180, 90)

theta = np.radians(theta)

# ================= CONSTANT VECTORS =================
L_vec = np.array([L, 0, 0])

B_vec = np.array([
    np.cos(theta),
    np.sin(theta),
    0
]) * B

F_vec = I * np.cross(L_vec, B_vec)

# Normalize force for motion
F_dir = F_vec / (np.linalg.norm(F_vec) + 1e-9)

# ================= ANIMATION SETUP =================
placeholder = st.empty()
start = st.button("▶ Start Animation")

# wire initial position
pos = np.array([0.0, 0.0, 0.0])

dt = 0.1
velocity = np.array([0.0, 0.0, 0.0])

# ================= ANIMATION LOOP =================
if start:

    for t in range(40):

        # simple motion model: a = F (scaled)
        acceleration = 0.5 * F_dir

        velocity += acceleration * dt
        pos = pos + velocity * dt

        fig = go.Figure()

        # wire (moving line)
        wire_start = pos
        wire_end = pos + L_vec

        fig.add_trace(go.Scatter3d(
            x=[wire_start[0], wire_end[0]],
            y=[wire_start[1], wire_end[1]],
            z=[wire_start[2], wire_end[2]],
            mode='lines',
            line=dict(color='blue', width=8),
            name="Wire"
        ))

        # force vector
        fig.add_trace(go.Scatter3d(
            x=[pos[0], pos[0] + F_dir[0]],
            y=[pos[1], pos[1] + F_dir[1]],
            z=[pos[2], pos[2] + F_dir[2]],
            mode='lines',
            line=dict(color='red', width=6),
            name="Force"
        ))

        # magnetic field direction (fixed)
        fig.add_trace(go.Scatter3d(
            x=[0, B_vec[0]],
            y=[0, B_vec[1]],
            z=[0, B_vec[2]],
            mode='lines',
            line=dict(color='green', width=6),
            name="B Field"
        ))

        fig.update_layout(
            scene=dict(
                xaxis=dict(range=[-5, 5]),
                yaxis=dict(range=[-5, 5]),
                zaxis=dict(range=[-5, 5]),
                aspectmode="cube"
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            title=f"Time step: {t}"
        )

        placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(0.1)

st.info("Click Start Animation to see wire motion 🔄")
