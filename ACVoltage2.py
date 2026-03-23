import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="AC Generator Physics Pro", layout="wide")

st.title("AC Generator: Component Mapping")
st.markdown("The **Red Component** ($v \sin \\theta$) in the 3D model directly determines the **Amplitude** on the waveform.")

# --- Sidebar ---
theta_deg = st.sidebar.slider("Rotation Angle (θ)", 0, 360, 45, 1)
theta_rad = np.radians(theta_deg)

# --- 1. Realistic 3D Model Logic ---
fig_3d = go.Figure()

# Helper for Pole Shoes
def draw_pole_shoe(x_offset, color, label):
    phi = np.linspace(-np.pi/3, np.pi/3, 20)
    y_range = np.linspace(-2, 2, 10)
    Phi, Y = np.meshgrid(phi, y_range)
    Z = 2 * np.sin(Phi)
    X = x_offset + 0.4 * np.cos(Phi) * np.sign(-x_offset)
    fig_3d.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale=[[0, color], [1, color]], 
                             showscale=False, opacity=0.5, name=label))

draw_pole_shoe(-2.2, 'red', 'North Pole')
draw_pole_shoe(2.2, 'blue', 'South Pole')

# Conductor Geometry
r = 1.2
v_mag = 1.5
ax, az = r * np.cos(theta_rad), r * np.sin(theta_rad)
vax, vaz = -v_mag * np.sin(theta_rad), v_mag * np.cos(theta_rad)
cx, cz = -ax, -az

# 3D Velocity Components at Conductor 'a'
fig_3d.add_trace(go.Scatter3d(x=[ax, ax+vax], y=[1.8, 1.8], z=[az, az],
                         mode='lines', line=dict(color='red', width=10), name="Cutting Component (v sinθ)"))
fig_3d.add_trace(go.Scatter3d(x=[ax+vax, ax+vax], y=[1.8, 1.8], z=[az, az+vaz],
                         mode='lines', line=dict(color='lime', width=5), name="Parallel Component (v cosθ)"))
fig_3d.add_trace(go.Scatter3d(x=[ax, ax+vax], y=[1.8, 1.8], z=[az, az+vaz],
                         mode='lines', line=dict(color='black', width=3), name="Total Velocity v"))

# Coil Arms
fig_3d.add_trace(go.Scatter3d(x=[ax, ax], y=[-1.8, 1.8], z=[az, az], mode='lines', line=dict(color='gold', width=12), name="Arm a-b"))
fig_3d.add_trace(go.Scatter3d(x=[cx, cx], y=[-1.8, 1.8], z=[cz, cz], mode='lines', line=dict(color='gold', width=12), name="Arm c-d"))

fig_3d.update_layout(scene=dict(xaxis_range=[-3,3], yaxis_range=[-3,3], zaxis_range=[-3,3], aspectmode='cube'), height=600, margin=dict(l=0,r=0,b=0,t=0))

# --- 2. Annotated 2D Waveform ---
angles = np.linspace(0, 360, 500)
v_out = np.sin(np.radians(angles))
current_v = np.sin(theta_rad)

fig_wave = go.Figure()

# Background Waveform
fig_wave.add_trace(go.Scatter(x=angles, y=v_out, line=dict(color='rgba(200,200,200,0.5)', width=2), name="Path"))

# The "Active" Component segment on the Y-axis
fig_wave.add_trace(go.Scatter(x=[theta_deg, theta_deg], y=[0, current_v], 
                             mode='lines+markers', line=dict(color='red', width=6), 
                             marker=dict(size=10), name="Induced e.m.f (v sinθ)"))

# Labels and Annotations
fig_wave.add_annotation(x=theta_deg, y=current_v, text=f"e = {current_v:.2f} V", 
                        showarrow=True, arrowhead=2, bgcolor="yellow")

fig_wave.update_layout(
    title="Output Waveform: Induced Voltage vs Angle",
    xaxis=dict(title="Angle θ (Degrees)", tickvals=[0, 90, 180, 270, 360], gridcolor='lightgray'),
    yaxis=dict(title="Voltage Magnitude", range=[-1.2, 1.2], gridcolor='lightgray'),
    plot_bgcolor='white', height=450
)

# --- UI Layout ---
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(fig_3d, use_container_width=True)
with c2:
    st.plotly_chart(fig_wave, use_container_width=True)
    
    # Detailed Physics Readout
    st.subheader("Component Values")
    st.markdown(f"""
    * <span style='color:red; font-weight:bold;'>Induced Component (v sinθ): {abs(current_v):.2f}</span>
    * <span style='color:green; font-weight:bold;'>Parallel Component (v cosθ): {abs(np.cos(theta_rad)):.2f}</span>
    """, unsafe_allow_html=True)
