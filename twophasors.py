# --- PLOT ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'polar'}, {'type': 'xy'}]],
    column_widths=[0.4, 0.6]
)

# --- Voltage Vector (BOLD) ---
fig.add_trace(go.Scatterpolar(
    r=[0, V_m],
    theta=[0, theta_deg],
    mode='lines',
    line=dict(color='crimson', width=6),  # thicker
    name='Voltage'
), row=1, col=1)

fig.add_trace(go.Scatterpolar(
    r=[V_m],
    theta=[theta_deg],
    mode='markers+text',
    marker=dict(size=16, color='crimson', symbol='triangle-up'),  # bigger arrow
    text=["V"],
    textposition="top center",
    showlegend=False
), row=1, col=1)

# --- Current Vector (BOLD) ---
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

# --- Waveforms (BOLDER) ---
fig.add_trace(go.Scatter(
    x=t_axis, y=v_wave,
    line=dict(color='crimson', width=3),  # thicker
    opacity=0.6,
    name='Voltage Wave'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=t_axis, y=i_wave,
    line=dict(color='dodgerblue', width=3),
    opacity=0.6,
    name='Current Wave'
), row=1, col=2)

# --- Instantaneous Points (BIGGER) ---
fig.add_trace(go.Scatter(
    x=[theta_deg], y=[v_inst],
    mode='markers',
    marker=dict(size=14, color='crimson'),
    name='V(t)'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=[theta_deg], y=[i_inst],
    mode='markers',
    marker=dict(size=14, color='dodgerblue'),
    name='I(t)'
), row=1, col=2)

# --- Layout Enhancements ---
fig.update_layout(
    height=520,
    margin=dict(t=30, b=30),
    polar=dict(
        radialaxis=dict(range=[0, 11], tickfont=dict(size=12)),
        angularaxis=dict(tickfont=dict(size=12))
    ),
    font=dict(size=14)  # overall font bigger
)

fig.update_xaxes(title="Phase Angle (Degrees)", title_font=dict(size=14), row=1, col=2)
fig.update_yaxes(range=[-11, 11], title_font=dict(size=14), row=1, col=2)
