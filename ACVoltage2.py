import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="AC Generator Physics", layout="wide")

st.title("AC Generator: Velocity Vector Analysis")
st.markdown("This simulation illustrates how the **velocity components** of the coil determine induced e.m.f.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 1)
theta_rad = np.radians(theta_deg)

# --- 1. 3D Generator Model (Physical View) ---
fig_3d = go.Figure()

# Magnets & Flux (Simplified for focus)
fig_3d.add_trace(go.Scatter3d(x=[-2.5, 2.5], y=[0, 0], z=[0, 0], mode='lines', 
                             line=dict(color='gray', width=1, dash='dot'), showlegend=False))

# Coil position
r = 1.5
x_pos, z_pos = r * np.cos(theta_rad), r * np.sin(theta_rad)

# Draw Coil Side (Arm a-b)
fig_3d.add_trace(go.Scatter3d(
    x=[x_pos, x_pos], y=[-1, 1], z=[z_pos, z_pos],
    mode='lines+markers', line=dict(color='gold', width=10), name='Arm a-b'
))

# Tangential Velocity Vector (v) in 3D
v_len = 1.2
vx, vz = -v_len * np.sin(theta_rad), v_len * np.cos(theta_rad)
fig_3d.add_trace(go.Cone(x=[x_pos], y=[0], z=[z_pos], u=[vx], v=[0], w=[vz], 
                         sizemode="absolute", sizeref=0.5, showscale=False, colorscale=[[0, 'black'], [1, 'black']]))

fig_3d.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-2,2], zaxis_range=[-3,3]), height=500, margin=dict(t=0, b=0))

# --- 2. 2D Vector Analysis (The Math from your Image) ---
fig_2d = go.Figure()

# Draw Flux Lines (Background)
for i in np.linspace(-2, 2, 5):
    fig_2d.add_trace(go.Scatter(x=[i, i], y=[-2, 2], mode='lines', line=dict(color='lightblue', dash='dash'), showlegend=False))

# Draw Coil Radius (r)
fig_2d.add_trace(go.Scatter(x=[0, x_pos], y=[0, z_pos], mode='lines+text', 
                            text=["", "A"], textposition="top right", line=dict(color='black', width=2), name="Radius (r)"))

# Main Velocity Vector (v) - Tangential
fig_2d.add_trace(go.Scatter(x=[x_pos, x_pos + vx], y=[z_pos, z_pos + vz], 
                            mode='lines+markers', line=dict(color='black', width=4), marker=dict(symbol="arrow", size=10), name="Total Velocity (v)"))

# Component: v sin(theta) - Perpendicular to Flux
fig_2d.add_trace(go.Scatter(x=[x_pos, x_pos + vx], y=[z_pos, z_pos], 
                            mode='lines', line=dict(color='crimson', width=3), name="v sin(θ) [Cutting Flux]"))

# Component: v cos(theta) - Parallel to Flux
fig_2d.add_trace(go.Scatter(x=[x_pos + vx, x_pos + vx], y=[z_pos, z_pos + vz], 
                            mode='lines', line=dict(color='green', width=3), name="v cos(θ) [Parallel]"))

fig_2d.update_layout(xaxis_range=[-3,3], yaxis_range=[-3,3], height=500, title="Velocity Vector Breakdown", showlegend=True)

# --- Layout ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_3d, use_container_width=True)
with col2:
    st.plotly_chart(fig_2d, use_container_width=True)

# --- Analysis Text ---
st.markdown("---")
col_a, col_b, col_c = st.columns(3)
col_a.metric("Angle (θ)", f"{theta_deg}°")
col_b.metric("Flux Cutting Component", f"{np.sin(theta_rad):.2f} v")
col_c.metric("Parallel Component", f"{np.cos(theta_rad):.2f} v")

st.info(f"""
**Physics Insight:** At {theta_deg}°, the component of velocity cutting the flux lines is **{np.sin(theta_rad):.2f}v**. 
Because Induced EMF $e = B \cdot l \cdot (v \sin\theta)$, the voltage output is directly proportional to the red line in the diagram.
""")
