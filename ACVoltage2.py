import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Generator Vector Analysis", layout="wide")

st.title("AC Generator: Angular & Velocity Components")
st.markdown("This view matches the geometric breakdown: $v \sin \\theta$ is the **horizontal** component cutting the **vertical** flux.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 1)
theta_rad = np.radians(theta_deg)

# --- Geometry Setup ---
r = 2.0      # Radius
v_mag = 2.0  # Velocity magnitude
# Conductor position (A)
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
# Velocity vector (tangential)
vx, vz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

fig = go.Figure()

# 1. Background Flux Lines (Vertical)
for x in np.linspace(-2.5, 2.5, 7):
    fig.add_trace(go.Scatter(x=[x, x], y=[-3, 3], mode='lines', 
                             line=dict(color='rgba(100,100,100,0.1)', dash='dash'), showlegend=False))

# 2. Circular Path
phi = np.linspace(0, 2*np.pi, 100)
fig.add_trace(go.Scatter(x=r*np.cos(phi), y=r*np.sin(phi), mode='lines', 
                         line=dict(color='lightgray', dash='dot'), name="Circular Path"))

# 3. Radius Vector (r) and Angle Arc
fig.add_trace(go.Scatter(x=[0, ax], y=[0, az], mode='lines+markers', 
                         line=dict(color='black', width=2), name="Radius (r)"))

# Angle Arc (θ)
arc_theta = np.linspace(0, theta_rad, 20)
fig.add_trace(go.Scatter(x=0.5*np.cos(arc_theta), y=0.5*np.sin(arc_theta), 
                         mode='lines', line=dict(color='orange', width=3), name="Angle θ"))

# 4. Total Velocity Vector (v) - Tangential
fig.add_trace(go.Scatter(x=[ax, ax + vx], y=[az, az + vz], 
                         mode='lines+markers', line=dict(color='black', width=4), 
                         marker=dict(symbol="arrow", size=10, angleref="previous"), name="Total Velocity (v)"))

# 5. Velocity Components (The Right Triangle)
# Horizontal Component: v * sin(theta) -> CUTTING COMPONENT
fig.add_trace(go.Scatter(x=[ax, ax + vx], y=[az, az], 
                         mode='lines+text', text=["", f"v sin({theta_deg}°)"], textposition="bottom center",
                         line=dict(color='crimson', width=5), name="Flux Cutting (v sinθ)"))

# Vertical Component: v * cos(theta) -> PARALLEL COMPONENT
fig.add_trace(go.Scatter(x=[ax + vx, ax + vx], y=[az, az + vz], 
                         mode='lines+text', text=["", f"v cos({theta_deg}°)"], textposition="middle right",
                         line=dict(color='green', width=3), name="Parallel (v cosθ)"))

# Labels for Points
fig.add_trace(go.Scatter(x=[0, ax, ax+vx], y=[0, az, az+vz], mode='text', 
                         text=["O", "A", "V"], textfont=dict(size=16, color="black"), showlegend=False))

# --- Layout ---
fig.update_layout(
    xaxis=dict(range=[-4, 4], scaleanchor="y", scaleratio=1),
    yaxis=dict(range=[-4, 4]),
    width=800, height=700,
    title=f"Vector Decomposition at θ = {theta_deg}°",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# --- Metric Panel ---
c1, c2, c3 = st.columns(3)
c1.metric("Induced Component", f"{abs(np.sin(theta_rad)):.2f} v")
c2.metric("Parallel Component", f"{abs(np.cos(theta_rad)):.2f} v")
c3.write(f"**Result:** Induced E.M.F is proportional to {abs(np.sin(theta_rad)):.2f} of max.")
