import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="3D AC Generator Pro", layout="wide")

st.title("3D Interactive AC Generator: Corrected Rotation")
st.markdown("The gold arms represent the **active conductors** where e.m.f. is induced.")

# --- Sidebar Controls ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 0, 5)
theta = np.radians(theta_deg)

# --- 3D Figure Setup ---
fig = go.Figure()

def add_magnet(x_center, color, label):
    """Helper to draw 3D Rectangular Magnets"""
    # Define the 8 corners of a cube/box
    dx, dy, dz = 0.5, 2.0, 2.0
    x = [x_center-dx, x_center+dx]
    y = [-dy, dy]
    z = [-dz, dz]
    
    fig.add_trace(go.Mesh3d(
        x=[x[0], x[0], x[1], x[1], x[0], x[0], x[1], x[1]],
        y=[y[0], y[1], y[1], y[0], y[0], y[1], y[1], y[0]],
        z=[z[0], z[0], z[0], z[0], z[1], z[1], z[1], z[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color, opacity=0.6, name=label
    ))

# 1. Draw Realistic Magnets
add_magnet(-2.5, 'red', 'North Pole (N)')
add_magnet(2.5, 'blue', 'South Pole (S)')

# 2. Magnetic Field Lines (Flux)
for z_line in np.linspace(-1.2, 1.2, 5):
    for y_line in np.linspace(-1.2, 1.2, 5):
        fig.add_trace(go.Scatter3d(
            x=[-2, 2], y=[y_line, y_line], z=[z_line, z_line],
            mode='lines', line=dict(color='lightgray', width=1, dash='dot'),
            showlegend=False
        ))

# 3. Corrected Coil Geometry
# For a vertical start (Neutral Plane), x depends on sin and z depends on cos
r = 1.2 
L = 1.8 

# Position of Arm 1 (a-b)
x1, z1 = r * np.sin(theta), r * np.cos(theta)
# Position of Arm 2 (c-d)
x2, z2 = -r * np.sin(theta), -r * np.cos(theta)

# --- 4. Draw the Coil Components ---
# Active Arm a-b
fig.add_trace(go.Scatter3d(
    x=[x1, x1], y=[-L, L], z=[z1, z1],
    mode='lines+markers+text',
    line=dict(color='gold', width=12),
    text=['b', 'a'], textposition="top center",
    name='Arm a-b'
))

# Active Arm c-d
fig.add_trace(go.Scatter3d(
    x=[x2, x2], y=[-L, L], z=[z2, z2],
    mode='lines+markers+text',
    line=dict(color='gold', width=12),
    text=['c', 'd'], textposition="bottom center",
    name='Arm c-d'
))

# End-turns (Overhangs)
fig.add_trace(go.Scatter3d(
    x=[x1, x2], y=[L, L], z=[z1, z2],
    mode='lines', line=dict(color='black', width=5), name='End-turn'
))
fig.add_trace(go.Scatter3d(
    x=[x1, x2], y=[-L, -L], z=[z1, z2],
    mode='lines', line=dict(color='black', width=5), showlegend=False
))

# Shaft
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[-2.5, 2.5], z=[0, 0],
    mode='lines', line=dict(color='gray', width=3), name='Shaft'
))

# --- Layout ---
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Flux (X)', range=[-4, 4]),
        yaxis=dict(title='Axis (Y)', range=[-3, 3]),
        zaxis=dict(title='Height (Z)', range=[-3, 3]),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=0), height=700
)

st.plotly_chart(fig, use_container_width=True)

# --- Physics Logic ---
# Since we start vertical (parallel to flux), EMF follows sin(theta)
current_emf = np.sin(theta)
st.metric("Induced E.M.F.", f"{current_emf:.2f} V")

if abs(current_emf) < 0.1:
    st.info("Coil is vertical: Arms move **parallel** to flux lines. Induced e.m.f = 0.")
elif abs(current_emf) > 0.9:
    st.success("Coil is horizontal: Arms cut flux **perpendicularly**. Induced e.m.f = Max.")
