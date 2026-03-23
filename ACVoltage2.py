import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Corrected Generator Physics", layout="wide")

st.title("AC Generator: Corrected Pole & Flux Physics")
st.markdown("""
**Corrected Logic:**
* **Poles:** North (Left) and South (Right). Flux is **Horizontal**.
* **Max EMF:** Occurs at $0^\circ$ (Horizontal Coil) because the wire is moving **UP** (cutting horizontal flux at $90^\circ$).
* **Zero EMF:** Occurs at $90^\circ$ (Vertical Coil) because the wire is moving **LEFT** (parallel to horizontal flux).
""")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 0, 1)
theta_rad = np.radians(theta_deg)

fig_3d = go.Figure()

# 1. Realistic Magnets (Left and Right)
def draw_pole(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2, 2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    # Curved faces facing the center
    Z = 2 * np.sin(Phi)
    X = x_offset + 0.4 * np.cos(Phi) * np.sign(-x_offset)
    fig_3d.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.6, name=label))

draw_pole(-2.2, 'red', 'North Pole')
draw_pole(2.2, 'blue', 'South Pole')

# 2. Horizontal Flux Lines (N to S)
for zl in np.linspace(-1.2, 1.2, 5):
    for yl in np.linspace(-1.2, 1.2, 5):
        fig_3d.add_trace(go.Scatter3d(x=[-1.8, 1.8], y=[yl, yl], z=[zl, zl],
                                 mode='lines', line=dict(color='rgba(150,150,150,0.3)', width=1), showlegend=False))

# 3. Conductor Geometry
r = 1.2
v_mag = 1.5
# Position
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
# Velocity (Tangential)
# v_horizontal (vx), v_vertical (vz)
vx, vz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

# 4. Corrected Vectors
# Because flux is HORIZONTAL, the cutting component is the VERTICAL velocity (vz)
fig_3d.add_trace(go.Scatter3d(x=[ax, ax], y=[1.8, 1.8], z=[az, az + vz],
                         mode='lines', line=dict(color='red', width=10), name="Cutting Component (v cosθ)"))

fig_3d.add_trace(go.Scatter3d(x=[ax, ax + vx], y=[1.8, 1.8], z=[az + vz, az + vz],
                         mode='lines', line=dict(color='limegreen', width=5), name="Parallel Component (v sinθ)"))

# Coil Arms
fig_3d.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az], mode='lines', line=dict(color='gold', width=12), name="Arm a-b"))
fig_3d.add_trace(go.Scatter3d(x=[-ax, -ax], y=[-1.8, 1.8], z=[-az, -az], mode='lines', line=dict(color='gold', width=12), name="Arm c-d"))

fig_3d.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'), margin=dict(l=0,r=0,b=0,t=0), height=600)

# --- Waveform ---
angles = np.linspace(0, 360, 500)
# EMF is now cos(theta) because max is at 0 degrees
current_emf = np.cos(theta_rad)
v_out = np.cos(np.radians(angles))

fig_wave = go.Figure()
fig_wave.add_trace(go.Scatter(x=angles, y=v_out, line=dict(color='rgba(200,200,200,0.3)', width=2)))
fig_wave.add_trace(go.Scatter(x=[theta_deg, theta_deg], y=[0, current_emf], mode='lines+markers', line=dict(color='red', width=6), name="Output EMF"))

fig_wave.update_layout(title="Induced EMF (Max when Coil is Horizontal)", xaxis=dict(title="Angle θ"), yaxis=dict(range=[-1.2, 1.2]), template="plotly_white", height=400)

# --- Layout ---
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(fig_3d, use_container_width=True)
with c2:
    st.plotly_chart(fig_wave, use_container_width=True)
    st.latex(rf"e = B \cdot l \cdot v \cdot \cos({theta_deg}^\circ) = {current_emf:.2f}")
