import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="3D AC Generator", layout="wide")

st.title("3D Interactive AC Generator: Armature Analysis")
st.markdown("""
Drag the slider to rotate the coil. 
* **Gold Arms (a-b, c-d):** Active segments cutting magnetic flux.
* **Black Lines:** Overhangs (End-turns) connecting the circuit.
""")

# --- Sidebar Controls ---
st.sidebar.header("Generator Settings")
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 0, 5)
theta = np.radians(theta_deg)

# --- 3D Figure Setup ---
fig = go.Figure()

# 1. Draw Magnetic Poles (N and S)
# North Pole (Red)
fig.add_trace(go.Surface(
    x=[[-2, -2], [-2, -2]], y=[[-2, 2], [-2, 2]], z=[[-2, -2], [2, 2]],
    colorscale=[[0, 'red'], [1, 'red']], showscale=False, opacity=0.3, name='North Pole'
))

# South Pole (Blue)
fig.add_trace(go.Surface(
    x=[[2, 2], [2, 2]], y=[[-2, 2], [-2, 2]], z=[[-2, -2], [2, 2]],
    colorscale=[[0, 'blue'], [1, 'blue']], showscale=False, opacity=0.3, name='South Pole'
))

# 2. Magnetic Field Lines (Flux B)
for z_line in np.linspace(-1.5, 1.5, 4):
    for y_line in np.linspace(-1.5, 1.5, 4):
        fig.add_trace(go.Scatter3d(
            x=[-2, 2], y=[y_line, y_line], z=[z_line, z_line],
            mode='lines', line=dict(color='lightgray', width=1, dash='dot'),
            showlegend=False, hoverinfo='skip'
        ))

# 3. Coil Geometry Calculations
r = 1.5 
coil_length = 1.8  # Length of the active arms

# Coordinates for Arm a-b
x_ab, z_ab = r * np.cos(theta), r * np.sin(theta)
# Coordinates for Arm c-d
x_cd, z_cd = -r * np.cos(theta), -r * np.sin(theta)

# --- 4. Draw the Coil Components ---

# Active Arm a-b
fig.add_trace(go.Scatter3d(
    x=[x_ab, x_ab], y=[-coil_length, coil_length], z=[z_ab, z_ab],
    mode='lines+markers+text',
    line=dict(color='gold', width=12),
    marker=dict(size=4),
    text=['b', 'a'], textposition="top center",
    name='Active Arm (a-b)'
))

# Active Arm c-d
fig.add_trace(go.Scatter3d(
    x=[x_cd, x_cd], y=[-coil_length, coil_length], z=[z_cd, z_cd],
    mode='lines+markers+text',
    line=dict(color='gold', width=12),
    marker=dict(size=4),
    text=['c', 'd'], textposition="bottom center",
    name='Active Arm (c-d)'
))

# Overhang 1 (Top End-turn)
fig.add_trace(go.Scatter3d(
    x=[x_ab, x_cd], y=[coil_length, coil_length], z=[z_ab, z_cd],
    mode='lines', line=dict(color='black', width=5),
    name='Overhang (End-turn)'
))

# Overhang 2 (Bottom End-turn)
fig.add_trace(go.Scatter3d(
    x=[x_ab, x_cd], y=[-coil_length, -coil_length], z=[z_ab, z_cd],
    mode='lines', line=dict(color='black', width=5),
    showlegend=False
))

# Rotation Axis (Shaft)
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[-2.5, 2.5], z=[0, 0],
    mode='lines', line=dict(color='gray', width=2, dash='dashdot'),
    name='Rotation Axis'
))

# --- Layout ---
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Flux Direction', range=[-3, 3]),
        yaxis=dict(title='Axial Length', range=[-3, 3]),
        zaxis=dict(title='Vertical', range=[-3, 3]),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=700
)

# --- UI Display ---
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Induced E.M.F.")
    # e = B * l * v * sin(theta)
    # At 0 degrees (vertical), arms move parallel to B -> 0 e.m.f.
    # We use sin(theta) because theta=0 is vertical in this coordinate setup
    current_emf = np.sin(theta)
    
    # Simple Gauge or Text Indicator
    st.metric(label="Normalized Voltage", value=f"{current_emf:.2f} V")
    
    # 2D Waveform Plot
    t_plot = np.linspace(0, 2*np.pi, 100)
    v_plot = np.sin(t_plot)
    
    fig_2d = go.Figure()
    fig_2d.add_trace(go.Scatter(x=np.degrees(t_plot), y=v_plot, line=dict(color='crimson', width=2)))
    # Moving Tracer on 2D Plot
    fig_2d.add_trace(go.Scatter(x=[theta_deg], y=[current_emf], mode='markers', marker=dict(color='gold', size=12)))
    
    fig_2d.update_layout(
        title="Output Waveform",
        xaxis_title="Angle (Deg)",
        yaxis_title="e.m.f",
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_2d, use_container_width=True)

# Status Messages
if abs(current_emf) < 0.1:
    st.info("💡 **Magnetic Neutral Plane:** The coil sides are moving parallel to the flux lines. No flux is being 'cut', so induced e.m.f. is zero.")
elif abs(current_emf) > 0.9:
    st.success("⚡ **Maximum Induction:** The coil sides are moving perpendicular to the flux lines. Flux cutting rate is at its peak.")
