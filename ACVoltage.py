import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="3D AC Generator Pro", layout="wide")

st.title("3D AC Generator: Physical Model & Waveform")
st.markdown("Rotate the coil to see how the physical position relates to the induced sine wave.")

# --- Sidebar Controls ---
st.sidebar.header("Controls")
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 0, 5)
theta_rad = np.radians(theta_deg)

# --- 1. 3D Generator Model ---
fig_3d = go.Figure()

def add_block_magnet(x_center, color, label):
    """Draws a solid 3D block for the magnet poles"""
    dx, dy, dz = 0.6, 2.0, 2.0
    x = [x_center - dx, x_center + dx]
    y = [-dy, dy]
    z = [-dz, dz]
    
    fig_3d.add_trace(go.Mesh3d(
        x=[x[0], x[0], x[1], x[1], x[0], x[0], x[1], x[1]],
        y=[y[0], y[1], y[1], y[0], y[0], y[1], y[1], y[0]],
        z=[z[0], z[0], z[0], z[0], z[1], z[1], z[1], z[1]],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color=color, opacity=0.5, name=label
    ))
    # Pole Labels
    fig_3d.add_trace(go.Scatter3d(
        x=[x_center], y=[0], z=[2.5],
        mode='text', text=[label[0]], 
        textfont=dict(size=24, color=color), showlegend=False
    ))

# Add Magnets
add_block_magnet(-2.8, 'red', 'North')
add_block_magnet(2.8, 'blue', 'South')

# Magnetic Flux Lines (N to S)
for zl in np.linspace(-1.2, 1.2, 4):
    for yl in np.linspace(-1.2, 1.2, 4):
        # Dashed lines
        fig_3d.add_trace(go.Scatter3d(
            x=[-2.2, 2.2], y=[yl, yl], z=[zl, zl],
            mode='lines', line=dict(color='gray', width=1, dash='dot'),
            showlegend=False
        ))
        # Directional Arrow (Cone)
        fig_3d.add_trace(go.Cone(
            x=[0], y=[yl], z=[zl], u=[1], v=[0], w=[0],
            sizemode="absolute", sizeref=0.3, showscale=False, colorscale=[[0, 'black'], [1, 'black']]
        ))

# Coil Geometry (Corrected Rotation around Y-axis)
r, L = 1.3, 1.8
# Start position: Vertical (Neutral Plane)
x1, z1 = r * np.sin(theta_rad), r * np.cos(theta_rad)
x2, z2 = -r * np.sin(theta_rad), -r * np.cos(theta_rad)

# Active Arms (a-b and c-d)
fig_3d.add_trace(go.Scatter3d(
    x=[x1, x1], y=[-L, L], z=[z1, z1],
    mode='lines+markers+text', line=dict(color='gold', width=12),
    text=['b', 'a'], textposition="top center", name='Active Arm a-b'
))
fig_3d.add_trace(go.Scatter3d(
    x=[x2, x2], y=[-L, L], z=[z2, z2],
    mode='lines+markers+text', line=dict(color='gold', width=12),
    text=['c', 'd'], textposition="bottom center", name='Active Arm c-d'
))

# Overhangs (End-turns)
fig_3d.add_trace(go.Scatter3d(
    x=[x1, x2], y=[L, L], z=[z1, z2],
    mode='lines', line=dict(color='black', width=5), name='End-turn'
))
fig_3d.add_trace(go.Scatter3d(
    x=[x1, x2], y=[-L, -L], z=[z1, z2],
    mode='lines', line=dict(color='black', width=5), showlegend=False
))

# Shaft/Axis
fig_3d.add_trace(go.Scatter3d(
    x=[0, 0], y=[-2.5, 2.5], z=[0, 0],
    mode='lines', line=dict(color='black', width=4, dash='dashdot'), name='Shaft'
))

fig_3d.update_layout(
    scene=dict(xaxis_range=[-4, 4], yaxis_range=[-3, 3], zaxis_range=[-3, 3], aspectmode='cube'),
    margin=dict(l=0, r=0, b=0, t=0), height=600
)

# --- 2. 2D Waveform Model ---
# EMF is sin(theta) because theta=0 is vertical (no flux cutting)
current_emf = np.sin(theta_rad)
angles = np.linspace(0, 360, 200)
waveform = np.sin(np.radians(angles))

fig_2d = go.Figure()
# Fixed Sine Path
fig_2d.add_trace(go.Scatter(x=angles, y=waveform, line=dict(color='crimson', width=2, dash='dot'), name='Waveform'))
# Moving Tracer
fig_2d.add_trace(go.Scatter(x=[theta_deg], y=[current_emf], mode='markers', marker=dict(color='gold', size=15, line=dict(width=2, color='black')), name='Current EMF'))

fig_2d.update_layout(
    title="Output Voltage (e.m.f)",
    xaxis=dict(title="Angle (Degrees)", tickvals=[0, 90, 180, 270, 360]),
    yaxis=dict(title="Voltage", range=[-1.2, 1.2]),
    template="plotly_white", height=400
)

# --- Layout Display ---
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig_3d, use_container_width=True)

with col2:
    st.plotly_chart(fig_2d, use_container_width=True)
    st.metric("Instantaneous E.M.F.", f"{current_emf:.3f} V")
    
    if abs(current_emf) < 0.1:
        st.info("The coil sides are moving **parallel** to the flux. Cutting rate = 0.")
    elif abs(current_emf) > 0.9:
        st.success("The coil sides are moving **perpendicular** to the flux. Cutting rate = Max.")
