import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Realistic AC Physics", layout="wide")

st.title("Realistic 3D Generator & Vector Decomposition")
st.markdown("Observe how the velocity vector $\\vec{v}$ decomposes. Only the component **perpendicular** to the flux induces voltage.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 5)
theta_rad = np.radians(theta_deg)

# --- 1. Realistic 3D Model ---
fig = go.Figure()

# A. Create Curved Pole Shoes (N and S)
def draw_curved_pole(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    z_curved = 2 * np.sin(phi)
    y_curved = np.linspace(-2, 2, 10)
    Y, Phi = np.meshgrid(y_curved, phi)
    Z = 2 * np.sin(Phi)
    X = 2.5 * np.sign(x_offset) + 0.5 * np.cos(Phi) * np.sign(-x_offset)
    
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.8, name=label))

draw_curved_pole(-1, 'red', 'North Pole')
draw_curved_pole(1, 'blue', 'South Pole')

# B. Armature Core (The Cylinder)
u = np.linspace(0, 2*np.pi, 30)
v_cyl = np.linspace(-1.8, 1.8, 10)
U, V_cyl = np.meshgrid(u, v_cyl)
X_cyl = 1.1 * np.cos(U)
Z_cyl = 1.1 * np.sin(U)
fig.add_trace(go.Surface(x=X_cyl, y=V_cyl, z=Z_cyl, colorscale=[[0, 'gray'], [1, 'gray']], 
                         showscale=False, opacity=0.3, name='Iron Core'))

# C. Calculation of Conductor Position & Vectors
r = 1.2
# Point A (Conductor)
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)

# Velocity Vector (v) - Tangential to circle
v_mag = 1.5
# Direction is perpendicular to radius: (-sin, cos)
vx, vz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

# D. Draw Conductor (Arm a-b)
fig.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az],
                         mode='lines+markers', line=dict(color='gold', width=12), name='Conductor a-b'))

# E. 3D Vector Decomposition (As per your diagram)
# Main Velocity v (Black)
fig.add_trace(go.Scatter3d(x=[ax, ax+vx], y=[0, 0], z=[az, az+vz],
                         mode='lines', line=dict(color='black', width=6), name='Total Velocity v'))

# Perpendicular Component (Red) - v sin(theta) - cuts vertical flux
fig.add_trace(go.Scatter3d(x=[ax, ax+vx], y=[0, 0], z=[az, az],
                         mode='lines', line=dict(color='crimson', width=8), name='v sin(θ) (Induced Component)'))

# Parallel Component (Green) - v cos(theta)
fig.add_trace(go.Scatter3d(x=[ax+vx, ax+vx], y=[0, 0], z=[az, az+vz],
                         mode='lines', line=dict(color='green', width=4), name='v cos(θ) (Parallel)'))

# Flux Lines (Top to Bottom as in your image)
for x_f in np.linspace(-1.5, 1.5, 6):
    fig.add_trace(go.Scatter3d(x=[x_f, x_f], y=[0, 0], z=[2, -2],
                             mode='lines', line=dict(color='rgba(100,100,100,0.2)', width=1), showlegend=False))

# Layout
fig.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'),
                  margin=dict(l=0,r=0,b=0,t=0), height=700)

st.plotly_chart(fig, use_container_width=True)

# --- Physics Summary ---
st.markdown("### The Mathematical Breakdown")
col1, col2 = st.columns(2)

with col1:
    st.latex(r"e = B \cdot l \cdot v \cdot \sin(\theta)")
    st.write("The **Red Vector** represents the rate at which the conductor crosses the flux lines.")

with col2:
    current_val = np.sin(theta_rad)
    st.metric("Relative induced e.m.f", f"{current_val:.2f} units")
    if abs(current_val) < 0.1:
        st.error("Neutral Plane: Velocity is parallel to flux. No cutting.")
    elif abs(current_val) > 0.9:
        st.success("Peak Position: Velocity is perpendicular to flux. Maximum cutting.")
