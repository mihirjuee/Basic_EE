import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIG ---
st.set_page_config(page_title="AC V & I Analysis", layout="wide")

# --- TITLE ---
st.title("⚡ AC Fundamentals: Voltage & Current Visualization")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Signal Parameters")

V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phi_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)

# Manual theta control
theta_deg = st.sidebar.slider("Theta (θ in degrees)", 0, 360, 0)

# --- COMPUTATION ---
theta_rad = np.deg2rad(theta_deg)
phi_rad = np.deg2rad(phi_deg)

t_axis = np.linspace(0, 360, 500)

v_wave = V_m * np.sin(np.deg2rad(t_axis))
i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)

v_inst = V_m * np.sin(theta_rad)
i_inst = I_m * np.sin(theta_rad + phi_rad)

# --- POWER FACTOR ---
pf = np.cos(phi_rad)

col1, col2 = st.columns(2)
col1.metric("Power Factor", f"{pf:.2f}")

if phi_deg > 0:
    col2.info("Current is Leading ⚡")
elif phi_deg < 0:
    col2.info("Current is Lagging ⚡")
else:
    col2.success("Unity Power Factor")

# --- EQUATIONS ---
st.latex(r"v(t) = V_m \sin(\omega t)")
st.latex(r"i(t) = I_m \sin(\omega t + \phi)")

# --- CREATE FIGURE ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'polar'}, {'type': 'xy'}]],
    column_widths=[0.4, 0.6]
)

# --- VOLTAGE VECTOR (BOLD) ---
fig.add_trace(go.Scatterpolar(
    r=[0, V_m],
    theta=[0, theta_deg],
    mode='lines',
    line=dict(color='crimson', width=6),
    name='Voltage'
), row=1, col=1)

fig.add_trace(go.Scatterpolar(
    r=[V_m],
    theta=[theta_deg],
    mode='markers+text',
    marker=dict(size=16, color='crimson', symbol='triangle-up'),
    text=["V"],
    textposition="top center",
    showlegend=False
), row=1, col=1)

# --- CURRENT VECTOR (BOLD) ---
fig.add_trace(go.Scatterpolar(
    r=[0, I_m],
    theta=[0, theta_deg + phi_deg],
    mode='lines',
    line=dict(color='dodgerblue', width=6),
    name='Current'
), row=1, col=1)

fig.add_trace(go.Scatterpolar(
    r=[I_m],
    theta=[theta_deg + phi_deg],
    mode='markers+text',
    marker=dict(size=16, color='dodgerblue', symbol='triangle-up'),
    text=["I"],
    textposition="top center",
    showlegend=False
), row=1, col=1)

# --- WAVEFORMS ---
fig.add_trace(go.Scatter(
    x=t_axis,
    y=v_wave,
    line=dict(color='crimson', width=3),
    opacity=0.7,
    name='Voltage Wave'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=t_axis,
    y=i_wave,
    line=dict(color='dodgerblue', width=3),
    opacity=0.7,
    name='Current Wave'
), row=1, col=2)

# --- INSTANTANEOUS POINTS ---
fig.add_trace(go.Scatter(
    x=[theta_deg],
    y=[v_inst],
    mode='markers',
    marker=dict(size=14, color='crimson'),
    name='V(t)'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=[theta_deg],
    y=[i_inst],
    mode='markers',
    marker=dict(size=14, color='dodgerblue'),
    name='I(t)'
), row=1, col=2)

# --- LAYOUT ---
fig.update_layout(
    height=520,
    margin=dict(t=30, b=30),
    plot_bgcolor='white',
    polar=dict(
        radialaxis=dict(range=[0, 11], tickfont=dict(size=12)),
        angularaxis=dict(tickfont=dict(size=12))
    ),
    font=dict(size=14)
)

# --- IMPROVED AXES (VERY CLEAR) ---
fig.update_xaxes(
    title="Phase Angle (Degrees)",
    range=[0, 360],
    showline=True,
    linewidth=3,
    linecolor='black',
    mirror=True,
    ticks='outside',
    tickwidth=2,
    tickcolor='black',
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    zeroline=True,
    zerolinewidth=3,
    zerolinecolor='black',
    row=1, col=2
)

fig.update_yaxes(
    title="Amplitude",
    range=[-11, 11],
    showline=True,
    linewidth=3,
    linecolor='black',
    mirror=True,
    ticks='outside',
    tickwidth=2,
    tickcolor='black',
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    zeroline=True,
    zerolinewidth=3,
    zerolinecolor='black',
    row=1, col=2
)

# --- DISPLAY ---
st.plotly_chart(fig, use_container_width=True)
