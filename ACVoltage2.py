import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Realistic AC Generator", layout="wide")

st.title("AC Generator: Dual Conductor (a-b & c-d) Analysis")
st.markdown("Both sides of the coil contribute to the total induced e.m.f. Note how their velocity vectors are opposite but their **flux-cutting components** (Red) work together.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 5)
theta_rad = np.radians(theta_deg)

fig = go.Figure()

# --- 1. Realistic Magnets (Pole Shoes) ---
def draw_pole_shoe(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2, 2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    # Curved face
    Z = 2 * np.sin(Phi)
    X = x_offset + 0.4 * np.cos(Phi) * np.sign(-x_offset)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.7, name=label))

draw_pole_shoe(-2.2, 'red', 'North Pole')
draw_pole_shoe(2.2, 'blue', 'South Pole')

# --- 2. Central Iron Core ---
u = np.linspace(0, 2*np.pi, 30)
v_cyl = np.linspace(-1.8, 1.8, 10)
U, V_cyl = np.meshgrid(u, v_cyl)
fig.add_trace(go.Surface(x=1.1*np.cos(U), y=V_cyl, z=1.1*np.sin(U), 
                         colorscale=[[0, 'lightgray'], [1, 'lightgray']], 
                         showscale=False, opacity=0.3, name='Core'))

# --- 3. Conductor Geometry & Velocity ---
r = 1.2
v_mag = 1.3

# Conductor A-B (Top-Right quadrant initially)
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
vax, vaz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

# Conductor C-D (Bottom-Left quadrant, 180 degrees apart)
cx, cz = -ax, -az
vcx, vcz = -vax, -vaz

# --- 4. Plotting Conductors & Vectors ---

def add_conductor_side(x, z, vx, vz, label, color_main):
    # The Wire
    fig.add_trace(go.Scatter3d(x=[x, x], y=[-1.8, 1.8], z=[z, z],
                             mode='lines+markers+text', 
                             line=dict(color='gold', width=12),
                             text=[label[0], label[1]], textposition="top center",
                             name=f"Side {label}"))
    
    # Total Velocity Vector v (Black)
    fig.add_trace(go.Scatter3d(x=[x, x+vx], y=[0, 0], z=[z, z+vz],
                             mode='lines', line=dict(color='black', width=5), 
                             showlegend=False))
    
    # Flux Cutting Component (Red) - v sin(theta)
    # This represents the horizontal cutting of the vertical field
    fig.add_trace(go.Scatter3d(x=[x, x+vx], y=[0, 0], z=[z, z],
                             mode='lines', line=dict(color='crimson', width=8), 
                             name=f"v sin(θ) at {label}"))

# Draw both sides
add_conductor_side(ax, az, vax, vaz, "ab", "gold")
add_conductor_side(cx, cz, vcx, vcz, "cd", "gold")

# End-turns (Connecting a-b to c-d)
fig.add_trace(go.Scatter3d(x=[ax, cx], y=[1.8, 1.8], z=[az, cz],
                         mode='lines', line=dict(color='black', width=4), name="End-turn"))
fig.add_trace(go.Scatter3d(x=[ax, cx], y=[-1.8, -1.8], z=[az, cz],
                         mode='lines', line=dict(color='black', width=4), showlegend=False))

# --- 5. Magnetic Flux Lines (Vertical as per your Diagram) ---
for x_f in np.linspace(-1.6, 1.6, 7):
    fig.add_trace(go.Scatter3d(x=[x_f, x_f], y=[0, 0], z=[1.8, -1.8],
                             mode='lines', line=dict(color='rgba(100,100,100,0.15)', width=1), 
                             showlegend=False))

# --- Layout ---
fig.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'),
                  margin=dict(l=0,r=0,b=0,t=0), height=750)

st.plotly_chart(fig, use_container_width=True)

# --- Physics Analysis ---
st.markdown("---")
st.latex(r"E_{total} = E_{ab} + E_{cd} = 2 \cdot (B \cdot l \cdot v \sin \theta)")
st.info(f"At angle {theta_deg}°, both conductors have a horizontal velocity component of **{abs(vax):.2f}** units. Since they are connected in series, their voltages add up to create the full AC cycle.")
