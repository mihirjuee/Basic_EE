import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ================= PAGE =================
st.set_page_config(page_title="Coil Lorentz Force", layout="wide")

st.title("⚡ Lorentz Force on Current-Carrying Coil")

st.latex(r"\mathbf{F} = I (\mathbf{L} \times \mathbf{B})")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
B = st.sidebar.slider("Magnetic Field (B)", 0.0, 5.0, 2.0)
L = st.sidebar.slider("Coil Length", 1.0, 5.0, 2.0)
W = st.sidebar.slider("Coil Width", 0.5, 3.0, 1.0)
theta = st.sidebar.slider("Initial Angle (deg)", 0, 180, 90)

theta = np.radians(theta)

# ================= COIL POINTS =================
def get_coil(angle):
    # rotation matrix
    R = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])

    # rectangle coil (2D)
    base = np.array([
        [-L/2, -W/2],
        [ L/2, -W/2],
        [ L/2,  W/2],
        [-L/2,  W/2],
        [-L/2, -W/2]
    ])

    rotated = base @ R.T
    return rotated

# ================= FORCE FUNCTION =================
def force_on_side(direction):
    # direction: +1 or -1 side
    return np.array([
        direction * I * B * W,
        0,
        0
    ])

# ================= ANIMATION =================
start = st.button("▶ Start Coil Motion")

placeholder = st.empty()

angle = theta
omega = 0.05  # angular speed

if start:

    for t in range(50):

        angle += omega

        coil = get_coil(angle)

        # expand to 3D
        x, y = coil[:, 0], coil[:, 1]
        z = np.zeros_like(x)

        fig = go.Figure()

        # coil wire
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='blue', width=6),
            name="Coil"
        ))

        # forces on two sides (simplified)
        F_left = force_on_side(-1)
        F_right = force_on_side(1)

        center = np.mean(coil[:-1], axis=0)

        # left force
        fig.add_trace(go.Scatter3d(
            x=[center[0], center[0] + F_left[0]*0.2],
            y=[center[1], center[1]],
            z=[0, 0],
            mode='lines',
            line=dict(color='red', width=6),
            name="Force L"
        ))

        # right force
        fig.add_trace(go.Scatter3d(
            x=[center[0], center[0] + F_right[0]*0.2],
            y=[center[1], center[1]],
            z=[0, 0],
            mode='lines',
            line=dict(color='green', width=6),
            name="Force R"
        ))

        fig.update_layout(
            scene=dict(
                xaxis=dict(range=[-4, 4]),
                yaxis=dict(range=[-4, 4]),
                zaxis=dict(range=[-2, 2]),
                aspectmode="cube"
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            title=f"Coil Rotation Angle: {np.degrees(angle):.1f}°"
        )

        placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(0.08)

st.info("Click Start Animation to simulate coil motion 🔄")
