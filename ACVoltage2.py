import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="3D Generator Vector Analysis", layout="wide")

st.title("Realistic 3D Generator: Vector & Angle Analysis")
st.markdown("This model shows the **velocity components** at conductor $a$-$b$ as it rotates through the vertical flux.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 1)
theta_rad = np.radians(theta_deg)

fig = go.Figure()

# --- 1. Realistic Magnets & Core ---
def draw_pole_shoe(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2, 2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    Z = 2 * np.sin(Phi)
    X = x_offset + 0.4 * np.cos(Phi) * np.sign(-x_offset)
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.6, name=label))

draw_pole_shoe(-2.2, 'red', 'North Pole')
draw_pole_shoe(2.2, 'blue', 'South Pole')

# Central Iron Core
u = np.linspace(0, 2*np.pi, 30)
v_cyl = np.linspace(-1.8, 1.8, 10)
U, V_cyl = np.meshgrid(u, v_cyl)
fig.add_trace(go.Surface(x=1.1*np.cos(U), y=V_cyl, z=1.1*np.sin(U), 
                         colorscale=[[0, 'lightgray'], [1, 'lightgray']], 
                         showscale=False, opacity=0.2, name='Core'))

# --- 2. Geometry & Motion ---
r = 1.2
v_mag = 1.5

# Conductor A-B Position
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
# Tangential Velocity Vector (v)
vax, vaz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)

# Conductor C-D Position
cx, cz = -ax, -az

# --- 3. Vector Components at Point A ---
# We draw these at the front face (y=1.8) for maximum visibility

# Radius Line (r)
fig.add_trace(go.Scatter3d(x=[0, ax], y=[1.8, 1.8], z=[0, az],
                         mode='lines', line=dict(color='black', width=4), name="Radius (r)"))

# Total Velocity Vector (v)
fig.add_trace(go.Scatter3d(x=[ax, ax+vax], y=[1.8, 1.8], z=[az, az+vaz],
                         mode='lines+markers', line=dict(color='black', width=6), 
                         marker=dict(size=4), name="Total Velocity v"))

# Flux Cutting Component (v sin theta) - Horizontal
fig.add_trace(go.Scatter3d(x=[ax, ax+vax], y=[1.8, 1.8], z=[az, az],
                         mode='lines+text', text=["", f"v sin({theta_deg}°)"], 
                         line=dict(color='crimson', width=10), name="Induced Component"))

# Parallel Component (v cos theta) - Vertical
fig.add_trace(go.Scatter3d(x=[ax+vax, ax+vax], y=[1.8, 1.8], z=[az, az+vaz],
                         mode='lines+text', text=["", f"v cos({theta_deg}°)"],
                         line=dict(color='green', width=4), name="Parallel Component"))

# --- 4. The Coil Loop ---
# Arm a-b
fig.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az],
                         mode='lines+markers+text', line=dict(color='gold', width=12),
                         text=['b', 'a'], textposition="top center", name="Arm a-b"))
# Arm c-d
fig.add_trace(go.Scatter3d(x=[cx, cx], y=[-1.8, 1.8], z=[cz, cz],
                         mode='lines+markers+text', line=dict(color='gold', width=12),
                         text=['c', 'd'], textposition="bottom center", name="Arm c-d"))
# End-turns
fig.add_trace(go.Scatter3d(x=[ax, cx], y=[1.8, 1.8], z=[az, cz], mode='lines', line=dict(color='black', width=4)))
fig.add_trace(go.Scatter3d(x=[ax, cx], y=[-1.8, -1.8], z=[az, cz], mode='lines', line=dict(color='black', width=4)))

# --- 5. Magnetic Flux (Vertical Lines) ---
for x_f in np.linspace(-1.6, 1.6, 7):
    fig.add_trace(go.Scatter3d(x=[x_f, x_f], y=[0, 0], z=[1.8, -1.8],
                             mode='lines', line=dict(color='rgba(100,100,100,0.15)', width=1), showlegend=False))

# Layout
fig.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'),
                  margin=dict(l=0,r=0,b=0,t=0), height=800)

st.plotly_chart(fig, use_container_width=True)

# --- Waveform Display ---
st.markdown("---")
angles = np.linspace(0, 360, 200)
waveform = np.sin(np.radians(angles))
fig_wave = go.Figure()
fig_wave.add_trace(go.Scatter(x=angles, y=waveform, line=dict(color='crimson', width=2)))
fig_wave.add_trace(go.Scatter(x=[theta_deg], y=[np.sin(theta_rad)], mode='markers', marker=dict(size=12, color='gold')))
fig_wave.update_layout(title="Induced E.M.F Output", height=300, xaxis_title="θ (Degrees)", yaxis_title="Voltage")
st.plotly_chart(fig_wave, use_container_width=True)
