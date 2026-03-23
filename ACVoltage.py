import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Magnetic Flux Visualization", layout="wide")
st.title("Interactive 3D Magnetic Field Visualization")
st.markdown("North to South magnetic flux simulation.")

# Create the 3D scene
fig = go.Figure()

# --- 1. Draw North and South Poles (Prisms) ---

def draw_magnet_pole(x_center, y_center, z_center, size, color, label, text_color):
    """Adds a simplified rectangular prism representation of a magnet pole."""
    # Define vertices for a unit cube and scale/shift them
    v = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
    ]) - 0.5  # Center at origin
    
    v = v * size + np.array([x_center, y_center, z_center])
    
    # Trace the wireframe edges
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0], # bottom
        [4, 5], [5, 6], [6, 7], [7, 4], # top
        [0, 4], [1, 5], [2, 6], [3, 7]  # vertical connectors
    ]
    
    for edge in edges:
        fig.add_trace(go.Scatter3d(
            x=[v[edge[0], 0], v[edge[1], 0]],
            y=[v[edge[0], 1], v[edge[1], 1]],
            z=[v[edge[0], 2], v[edge[1], 2]],
            mode='lines',
            line=dict(color=color, width=3),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Add Label
    fig.add_trace(go.Scatter3d(
        x=[x_center], y=[y_center], z=[z_center + size/2 + 0.3],
        mode='text',
        text=[label],
        textfont=dict(size=24, color=text_color),
        showlegend=False
    ))

# Draw the Red North Pole at X = -3
draw_magnet_pole(x_center=-3, y_center=0, z_center=0, size=2, color='red', label='N', text_color='red')

# Draw the Blue South Pole at X = +3
draw_magnet_pole(x_center=3, y_center=0, z_center=0, size=2, color='blue', label='S', text_color='blue')

# --- 2. Draw Magnetic Flux Lines (N to S) ---

# Define the region of space where flux will be shown
y_lines = np.linspace(-1.0, 1.0, 5)
z_lines = np.linspace(-1.0, 1.0, 5)

for y_l in y_lines:
    for z_l in z_lines:
        # Drawing the main line from North to South face
        fig.add_trace(go.Scatter3d(
            x=[-2, 2], y=[y_l, y_l], z=[z_l, z_l],
            mode='lines',
            line=dict(color='gray', width=1.5, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Adding a central cone as a directional arrowhead
        fig.add_trace(go.Cone(
            x=[0], y=[y_l], z=[z_l],
            u=[1], v=[0], w=[0], # Vector direction (along +X)
            sizemode="absolute", sizeref=0.2,
            colorscale=[[0, 'black'], [1, 'black']], showscale=False,
            anchor="center"
        ))

# --- Layout Configuration ---
fig.update_layout(
    scene=dict(
        xaxis=dict(title='X (N-S Axis)', range=[-5, 5], showbackground=False),
        yaxis=dict(title='Y (Width)', range=[-3, 3], showbackground=False),
        zaxis=dict(title='Z (Height)', range=[-3, 3], showbackground=False),
        camera=dict(
            eye=dict(x=1.8, y=1.2, z=0.8) # Viewing angle
        ),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=700
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
