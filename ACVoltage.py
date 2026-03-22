import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="3D AC Generator", layout="wide")

st.title("3D Interactive AC Generator")
st.markdown("Drag the slider to rotate the coil. You can also click and drag the 3D plot to view the generator from any angle!")

# --- Interactive Slider ---
theta_deg = st.slider("Rotate Coil Angle (θ) in Degrees", min_value=0, max_value=360, value=0, step=5)
theta = np.radians(theta_deg)

# --- 3D Figure Setup ---
fig = go.Figure()

# 1. Draw Magnetic Poles (N and S)
# We will represent these as colored planes for simplicity and visibility
# North Pole (Red) at x = -2
fig.add_trace(go.Surface(
    x=[[-2, -2], [-2, -2]],
    y=[[-2, 2], [-2, 2]],
    z=[[-2, -2], [2, 2]],
    colorscale=[[0, 'red'], [1, 'red']],
    showscale=False,
    opacity=0.5,
    name='North Pole'
))

# South Pole (Blue) at x = 2
fig.add_trace(go.Surface(
    x=[[2, 2], [2, 2]],
    y=[[-2, 2], [-2, 2]],
    z=[[-2, -2], [2, 2]],
    colorscale=[[0, 'blue'], [1, 'blue']],
    showscale=False,
    opacity=0.5,
    name='South Pole'
))

# Add Pole Labels
fig.add_trace(go.Scatter3d(x=[-2.2], y=[0], z=[2.5], mode='text', text=['N'], textfont=dict(size=20, color='red'), name='N'))
fig.add_trace(go.Scatter3d(x=[2.2], y=[0], z=[2.5], mode='text', text=['S'], textfont=dict(size=20, color='blue'), name='S'))

# 2. Draw Magnetic Field Lines
for z_line in np.linspace(-1.5, 1.5, 4):
    for y_line in np.linspace(-1.5, 1.5, 4):
        fig.add_trace(go.Scatter3d(
            x=[-2, 2], y=[y_line, y_line], z=[z_line, z_line],
            mode='lines',
            line=dict(color='gray', width=2, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))

# 3. Define Coil Parameters
# Coil rotates around the Y-axis. 
# Length along Y is 3. Radius of rotation (width) is 1.5.
r = 1.5 
coil_length = 1.5

# Calculate 3D coordinates based on angle theta
# Arm a-b
x_ab = r * np.cos(theta)
z_ab = r * np.sin(theta)
# Arm c-d
x_cd = -r * np.cos(theta)
z_cd = -r * np.sin(theta)

# Define the 4 corners of the rectangular coil
coil_x = [x_ab, x_ab, x_cd, x_cd, x_ab]
coil_y = [-coil_length, coil_length, coil_length, -coil_length, -coil_length]
coil_z = [z_ab, z_ab, z_cd, z_cd, z_ab]

# 4. Draw the Coil
fig.add_trace(go.Scatter3d(
    x=coil_x, y=coil_y, z=coil_z,
    mode='lines+markers',
    line=dict(color='gold', width=8),
    marker=dict(size=4, color='black'),
    name='Armature Coil'
))

# Add labels for arms a,b and c,d
fig.add_trace(go.Scatter3d(
    x=[x_ab, x_cd], y=[coil_length + 0.2, coil_length + 0.2], z=[z_ab, z_cd],
    mode='text',
    text=['a-b', 'c-d'],
    textfont=dict(size=14, color='black'),
    showlegend=False
))

# --- Layout Configuration ---
fig.update_layout(
    scene=dict(
        xaxis=dict(title='X (Magnetic Field Direction)', range=[-3, 3]),
        yaxis=dict(title='Y (Rotation Axis)', range=[-3, 3]),
        zaxis=dict(title='Z (Vertical)', range=[-3, 3]),
        aspectmode='cube',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2) # Default viewing angle
        )
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=600
)

# --- Render Plot in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- E.M.F Indicator ---
current_emf = np.sin(theta)
st.subheader(f"Current Output e.m.f: {current_emf:.2f}")

if abs(current_emf) < 0.05:
    st.info("The coil is moving parallel to the magnetic field. **Zero e.m.f is induced.**")
elif abs(current_emf) > 0.95:
    st.success("The coil is moving perpendicularly through the magnetic field. **Maximum e.m.f is induced.**")
else:
    st.warning("The coil is cutting through the field at an angle. e.m.f is between zero and maximum.")
