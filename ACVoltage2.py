import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="3D Armature Generator", layout="wide")

st.title("AC Generator: 3D Armature & Vector Analysis")
st.markdown("""
**Physics Logic:**
* **Horizontal Flux:** Lines flow from **Red (North)** to **Blue (South)**.
* **The Armature:** The grey cylinder represents the iron core.
* **Max Induction:** Occurs when the gold conductors are at the **Top/Bottom** of the rotation (moving horizontally through the vertical-most part of the flux).
""")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 0, 1)
theta_rad = np.radians(theta_deg)

fig_3d = go.Figure()

# 1. Realistic Curved Magnets (North and South)
def draw_pole(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2.2, 2.2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    Z = 2.2 * np.sin(Phi)
    X = x_offset + 0.5 * np.cos(Phi) * np.sign(-x_offset)
    fig_3d.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.6, name=label))

draw_pole(-2.8, 'red', 'North Pole')
draw_pole(2.8, 'blue', 'South Pole')

# 2. The 3D Armature Core (Cylinder)
u_cyl = np.linspace(0, 2*np.pi, 50)
v_cyl = np.linspace(-1.8, 1.8, 20)
U, V = np.meshgrid(u_cyl, v_cyl)
r_core = 1.2
X_core = r_core * np.cos(U)
Z_core = r_core * np.sin(U)

fig_3d.add_trace(go.Surface(x=X_core, y=V, z=Z_core, 
                             colorscale=[[0, 'lightgray'], [1, 'gray']], 
                             showscale=False, opacity=0.5, name='Armature Core'))

# 3. Magnetic Flux Lines (Horizontal N to S)
for zl in np.linspace(-1.5, 1.5, 6):
    for yl in np.linspace(-1.5, 1.5, 3):
        fig_3d.add_trace(go.Scatter3d(x=[-2.2, 2.2], y=[yl, yl], z=[zl, zl],
                                 mode='lines', line=dict(color='rgba(150,150,150,0.2)', width=1), showlegend=False))

# 4. Conductor Position & Velocity Vectors
# Coil Radius is slightly larger than core radius to show it on the surface
r_coil = 1.25 
v_mag = 1.8

# Position of Arm a-b
ax, az = r_coil * np.cos(theta_rad), r_coil * np.sin(theta_rad)
# Tangential Velocity
vx, vz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

# Conductor c-d is opposite
cx, cz = -ax, -az

# --- 5. Component Vectors ---
# Red = Cutting Component (Vertical movement vz because flux is horizontal)
fig_3d.add_trace(go.Scatter3d(x=[ax, ax], y=[1.8, 1.8], z=[az, az + vz],
                         mode='lines', line=dict(color='red', width=10), name="Cutting Component"))

# Green = Parallel Component (Horizontal movement vx)
fig_3d.add_trace(go.Scatter3d(x=[ax, ax + vx], y=[1.8, 1.8], z=[az + vz, az + vz],
                         mode='lines', line=dict(color='limegreen', width=5), name="Parallel Component"))

# --- 6. The Coil Windings ---
# Arm a-b
fig_3d.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az], 
                             mode='lines', line=dict(color='gold', width=12), name="Conductor a-b"))
# Arm c-d
fig_3d.add_trace(go.Scatter3d(x=[cx, cx], y=[-1.8, 1.8], z=[cz, cz], 
                             mode='lines', line=dict(color='gold', width=12), name="Conductor c-d"))
# End-turns
fig_3d.add_trace(go.Scatter3d(x=[ax, cx], y=[1.8, 1.8], z=[az, cz], mode='lines', line=dict(color='black', width=5)))
fig_3d.add_trace(go.Scatter3d(x=[ax, cx], y=[-1.8, -1.8], z=[az, cz], mode='lines', line=dict(color='black', width=5)))

# Shaft
fig_3d.add_trace(go.Scatter3d(x=[0, 0], y=[-2.5, 2.5], z=[0, 0],
                             mode='lines', line=dict(color='black', width=6, dash='dashdot'), name='Shaft'))

fig_3d.update_layout(scene=dict(xaxis_range=[-4,4], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'), 
                  margin=dict(l=0,r=0,b=0,t=0), height=700)

# --- 7. Waveform Comparison ---
# In this horizontal flux setup, max EMF is at 0 degrees (Vertical velocity is max)
current_emf = np.cos(theta_rad)
angles = np.linspace(0, 360, 500)
v_out = np.cos(np.radians(angles))

fig_wave = go.Figure()
fig_wave.add_trace(go.Scatter(x=angles, y=v_out, line=dict(color='rgba(200,200,200,0.4)', width=2)))
fig_wave.add_trace(go.Scatter(x=[theta_deg, theta_deg], y=[0, current_emf], 
                             mode='lines+markers', line=dict(color='red', width=6), name="Instantaneous EMF"))

fig_wave.update_layout(title="Induced EMF Output", xaxis=dict(title="Angle θ"), yaxis=dict(range=[-1.2, 1.2]), height=400)

# Render
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(fig_3d, use_container_width=True)
with c2:
    st.plotly_chart(fig_wave, use_container_width=True)
    st.metric("Relative E.M.F.", f"{current_emf:.3f}")
