import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="3D Generator Vector Analysis", layout="wide")

st.title("AC Generator: Velocity Vector & Angle Analysis")
st.markdown("Observe how the velocity vector $\\vec{v}$ decomposes. The **Red Vector** ($v \cos \\theta$) represents the vertical cutting of the horizontal magnetic field.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 30, 1)
theta_rad = np.radians(theta_deg)

fig = go.Figure()

# --- 1. Realistic Magnets & Core ---
def draw_pole_shoe(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2, 2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    Z = 2.2 * np.sin(Phi)
    X = x_offset + 0.5 * np.cos(Phi) * np.sign(-x_offset)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.5, name=label))

draw_pole_shoe(-2.8, 'red', 'North Pole')
draw_pole_shoe(2.8, 'blue', 'South Pole')

# Central Iron Core (Armature)
u = np.linspace(0, 2*np.pi, 30)
v_cyl = np.linspace(-1.8, 1.8, 10)
U, V_cyl = np.meshgrid(u, v_cyl)
fig.add_trace(go.Surface(x=1.2*np.cos(U), y=V_cyl, z=1.2*np.sin(U), 
                         colorscale=[[0, 'lightgray'], [1, 'gray']], 
                         showscale=False, opacity=0.4, name='Core'))

# --- 2. Geometry & Motion ---
r = 1.25  # Conductor radius
v_mag = 1.8 # Velocity magnitude

# Conductor A-B Position
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
# Tangential Velocity Vector (v) - Perpendicular to Radius
vx, vz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

# --- 3. Vector Analysis Overlay (At the front face y=1.8) ---

# Radius Line (r) - Marking the Angle theta
fig.add_trace(go.Scatter3d(x=[0, ax], y=[1.85, 1.85], z=[0, az],
                         mode='lines+text', text=["O", f"θ={theta_deg}°"], 
                         line=dict(color='black', width=4), name="Radius (r)"))

# Total Velocity Vector v (Black)
fig.add_trace(go.Scatter3d(x=[ax, ax+vx], y=[1.85, 1.85], z=[az, az+vz],
                         mode='lines+markers', line=dict(color='black', width=6), 
                         marker=dict(size=4), name="Total Velocity v"))

# Cutting Component (v cos theta) - Vertical (Because flux is horizontal)
fig.add_trace(go.Scatter3d(x=[ax, ax], y=[1.85, 1.85], z=[az, az+vz],
                         mode='lines+text', text=["", "v cosθ"], 
                         line=dict(color='red', width=10), name="Cutting Component"))

# Parallel Component (v sin theta) - Horizontal
fig.add_trace(go.Scatter3d(x=[ax, ax+vx], y=[1.85, 1.85], z=[az+vz, az+vz],
                         mode='lines+text', text=["", "v sinθ"],
                         line=dict(color='limegreen', width=4), name="Parallel Component"))

# --- 4. The Active Conductors ---
fig.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az],
                         mode='lines', line=dict(color='gold', width=12), name="Arm a-b"))
fig.add_trace(go.Scatter3d(x=[-ax, -ax], y=[-1.8, 1.8], z=[-az, -az],
                         mode='lines', line=dict(color='gold', width=12), name="Arm c-d"))

# --- 5. Horizontal Flux Lines (N to S) ---
for z_f in np.linspace(-1.5, 1.5, 6):
    fig.add_trace(go.Scatter3d(x=[-2.2, 2.2], y=[0, 0], z=[z_f, z_f],
                             mode='lines', line=dict(color='rgba(100,100,100,0.15)', width=1), showlegend=False))

# Layout
fig.update_layout(scene=dict(xaxis_range=[-4,4], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'),
                  margin=dict(l=0,r=0,b=0,t=0), height=800)

st.plotly_chart(fig, use_container_width=True)

# --- Analysis Readout ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.latex(r"v_{cutting} = v \cos(\theta)")
    st.write("Vertical velocity component cutting horizontal flux.")
with c2:
    st.latex(rf"e \propto \cos({theta_deg}^\circ) = {np.cos(theta_rad):.2f}")
    st.write("Instantaneous E.M.F. output.")
with c3:
    st.info("When $\\theta = 0^\circ$ (Horizontal), the conductor moves purely **UP**, providing maximum flux cutting.")
