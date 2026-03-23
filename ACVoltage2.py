import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Corrected AC Physics", layout="wide")

st.title("AC Generator: Corrected Vector Analysis")
st.markdown("""
**Physics Correction:** * <span style='color:red; font-weight:bold;'>Red Vector ($v \sin \\theta$):</span> Horizontal motion. Cuts the **vertical** flux lines.
* <span style='color:limegreen; font-weight:bold;'>Green Vector ($v \cos \\theta$):</span> Vertical motion. Moves **parallel** to the flux lines (No induction).
""", unsafe_allow_html=True)

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 1)
theta_rad = np.radians(theta_deg)

# --- 1. 3D Model with Corrected Vectors ---
fig_3d = go.Figure()

# Pole Shoes
def draw_pole_shoe(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2, 2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    Z = 2 * np.sin(Phi)
    X = x_offset + 0.4 * np.cos(Phi) * np.sign(-x_offset)
    fig_3d.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.4, name=label))

draw_pole_shoe(-2.2, 'red', 'North Pole')
draw_pole_shoe(2.2, 'blue', 'South Pole')

# Conductor Geometry
r = 1.2
v_mag = 1.6
# Conductor A-B position
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
# Tangential velocity components
# v_horizontal = -v*sin(theta), v_vertical = v*cos(theta)
v_cut = -v_mag * np.sin(theta_rad)
v_par = v_mag * np.cos(theta_rad)

# 3D Vector Display (Anchored at front of arm a-b)
# Red = Cutting (Horizontal), Green = Parallel (Vertical)
fig_3d.add_trace(go.Scatter3d(x=[ax, ax + v_cut], y=[1.8, 1.8], z=[az, az],
                         mode='lines', line=dict(color='red', width=10), name="v sinθ (Cutting)"))

fig_3d.add_trace(go.Scatter3d(x=[ax + v_cut], y=[1.8, 1.8], z=[az, az + v_par],
                         mode='lines', line=dict(color='limegreen', width=5), name="v cosθ (Parallel)"))

fig_3d.add_trace(go.Scatter3d(x=[ax, ax + v_cut], y=[1.8, 1.8], z=[az, az + v_par],
                         mode='lines', line=dict(color='black', width=3), name="Total v"))

# Arms
fig_3d.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az], mode='lines', line=dict(color='gold', width=12), name="Arm a-b"))
fig_3d.add_trace(go.Scatter3d(x=[-ax, -ax], y=[-1.8, 1.8], z=[-az, -az], mode='lines', line=dict(color='gold', width=12), name="Arm c-d"))

# Vertical Flux Lines (Visual Reference)
for xf in np.linspace(-1.5, 1.5, 6):
    fig_3d.add_trace(go.Scatter3d(x=[xf, xf], y=[0, 0], z=[1.8, -1.8],
                             mode='lines', line=dict(color='rgba(150,150,150,0.2)', width=1), showlegend=False))

fig_3d.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'), 
                  margin=dict(l=0,r=0,b=0,t=0), height=600)

# --- 2. Corrected 2D Waveform ---
angles = np.linspace(0, 360, 500)
# e is proportional to the cutting component (sin theta)
v_out = np.sin(np.radians(angles))
current_emf = np.sin(theta_rad)

fig_wave = go.Figure()
fig_wave.add_trace(go.Scatter(x=angles, y=v_out, line=dict(color='rgba(200,200,200,0.3)', width=2)))
# The Red indicator on the waveform matches the Red Cutting vector in 3D
fig_wave.add_trace(go.Scatter(x=[theta_deg, theta_deg], y=[0, current_emf], 
                             mode='lines+markers', line=dict(color='red', width=6), 
                             name="Induced e.m.f (Cutting Output)"))

fig_wave.update_layout(title="Output e.m.f (Tracks Red Vector)", 
                    xaxis=dict(title="Angle θ", tickvals=[0, 90, 180, 270, 360]),
                    yaxis=dict(range=[-1.2, 1.2]), height=400, template="plotly_white")

# --- Layout ---
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(fig_3d, use_container_width=True)
with c2:
    st.plotly_chart(fig_wave, use_container_width=True)
    st.latex(rf"e = B \cdot l \cdot v \cdot \sin({theta_deg}^\circ) = {current_emf:.2f} \text{{ units}}")
