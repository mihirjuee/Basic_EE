import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIG ---
st.set_page_config(page_title="AC V & I Analysis", layout="wide")

# --- MOBILE TOGGLE ---
is_mobile = st.toggle("📱 Mobile Layout", value=False)

# --- HEADER (RESPONSIVE) ---
if is_mobile:
    st.image("logo.png", width=80)
    st.title("⚡ Voltage & Current Visualization")
else:
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("logo.png", width=60)
    with col2:
        st.title("⚡ Voltage & Current Visualization")

# --- SIDEBAR ---
st.sidebar.header("Signal Parameters")

V_m = st.sidebar.slider("Voltage Amplitude ($V_m$)", 1.0, 10.0, 8.0)
I_m = st.sidebar.slider("Current Amplitude ($I_m$)", 1.0, 10.0, 5.0)
phi_deg = st.sidebar.slider("Phase Shift (φ in degrees)", -180, 180, -90)
theta_deg = st.sidebar.slider("Theta (θ in degrees)", 0, 360, 0)

# --- COMPUTATION ---
theta_rad = np.deg2rad(theta_deg)
phi_rad = np.deg2rad(phi_deg)

t_axis = np.linspace(0, 360, 500)

v_wave = V_m * np.sin(np.deg2rad(t_axis))
i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)

v_inst = V_m * np.sin(theta_rad)
i_inst = I_m * np.sin(theta_rad + phi_rad)

pf = np.cos(phi_rad)

# --- POWER FACTOR DISPLAY ---
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

# --- RESPONSIVE FIGURE ---
if is_mobile:
    fig = make_subplots(
        rows=2, cols=1,
        specs=[[{'type': 'polar'}], [{'type': 'xy'}]],
        vertical_spacing=0.25
    )
    polar_row, wave_row = 1, 2
    wave_col = 1
    fig_height = 750
else:
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'polar'}, {'type': 'xy'}]],
        column_widths=[0.4, 0.6]
    )
    polar_row, wave_row = 1, 1
    wave_col = 2
    fig_height = 520

# --- VOLTAGE VECTOR ---
fig.add_trace(go.Scatterpolar(
    r=[0, V_m],
    theta=[0, theta_deg],
    mode='lines',
    line=dict(color='crimson', width=5),
    name='Voltage'
), row=polar_row, col=1)

fig.add_annotation(
    x=theta_deg,
    y=V_m,
    ax=theta_deg - 5,
    ay=V_m - 1,
    xref="polar",
    yref="polar",
    axref="polar",
    ayref="polar",
    showarrow=True,
    arrowhead=3,
    arrowsize=1.5,
    arrowwidth=3,
    arrowcolor="crimson"
)

# --- CURRENT VECTOR ---
fig.add_trace(go.Scatterpolar(
    r=[0, I_m],
    theta=[0, theta_deg + phi_deg],
    mode='lines',
    line=dict(color='dodgerblue', width=5),
    name='Current'
), row=polar_row, col=1)

fig.add_annotation(
    x=theta_deg + phi_deg,
    y=I_m,
    ax=theta_deg + phi_deg - 5,
    ay=I_m - 1,
    xref="polar",
    yref="polar",
    axref="polar",
    ayref="polar",
    showarrow=True,
    arrowhead=3,
    arrowsize=1.5,
    arrowwidth=3,
    arrowcolor="dodgerblue"
)

# --- LABELS ---
fig.add_annotation(
    x=theta_deg,
    y=V_m,
    text="V",
    showarrow=False,
    font=dict(size=14, color="crimson"),
    xref="polar",
    yref="polar"
)

fig.add_annotation(
    x=theta_deg + phi_deg,
    y=I_m,
    text="I",
    showarrow=False,
    font=dict(size=14, color="dodgerblue"),
    xref="polar",
    yref="polar"
)

# --- WAVEFORMS ---
fig.add_trace(go.Scatter(
    x=t_axis,
    y=v_wave,
    line=dict(color='crimson', width=2),
    name='Voltage'
), row=wave_row, col=wave_col)

fig.add_trace(go.Scatter(
    x=t_axis,
    y=i_wave,
    line=dict(color='dodgerblue', width=2),
    name='Current'
), row=wave_row, col=wave_col)

# --- INSTANT POINTS ---
fig.add_trace(go.Scatter(
    x=[theta_deg],
    y=[v_inst],
    mode='markers',
    marker=dict(size=10, color='crimson'),
    name='V(t)'
), row=wave_row, col=wave_col)

fig.add_trace(go.Scatter(
    x=[theta_deg],
    y=[i_inst],
    mode='markers',
    marker=dict(size=10, color='dodgerblue'),
    name='I(t)'
), row=wave_row, col=wave_col)

# --- LAYOUT ---
fig.update_layout(
    height=fig_height,
    margin=dict(t=20, b=20, l=10, r=10),
    plot_bgcolor='white',
    font=dict(size=12 if is_mobile else 14),
    showlegend=True,
    polar=dict(
        radialaxis=dict(range=[0, 11])
    )
)

# --- AXES ---
fig.update_xaxes(
    title="Phase Angle (°)",
    range=[0, 360],
    showline=True,
    linewidth=2,
    linecolor='black',
    ticks='outside',
    showgrid=True,
    row=wave_row, col=wave_col
)

fig.update_yaxes(
    title="Amplitude",
    range=[-11, 11],
    showline=True,
    linewidth=2,
    linecolor='black',
    ticks='outside',
    showgrid=True,
    row=wave_row, col=wave_col
)

# --- DISPLAY ---
st.plotly_chart(fig, use_container_width=True, config={
    "responsive": True,
    "displayModeBar": False
})
