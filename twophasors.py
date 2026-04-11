@st.fragment(run_every=0.01 if st.session_state.running else None)
def render_animation():
    # 1. CONTROLS & LOGIC (Keep the same as before)
    btn_cols = st.columns(2)
    if btn_cols[0].button("▶️ Play"):
        st.session_state.running = True
        st.rerun()
    if btn_cols[1].button("⏸️ Pause"):
        st.session_state.running = False
        st.rerun()

    if st.session_state.running:
        st.session_state.theta_step = (st.session_state.theta_step + speed) % 360

    theta_deg = st.session_state.theta_step
    theta_rad = np.deg2rad(theta_deg)
    phi_rad = np.deg2rad(phi_deg)
    
    t_axis = np.linspace(0, 360, 400)
    v_wave = V_m * np.sin(np.deg2rad(t_axis))
    i_wave = I_m * np.sin(np.deg2rad(t_axis) + phi_rad)
    
    v_inst = V_m * np.sin(theta_rad)
    i_inst = I_m * np.sin(theta_rad + phi_rad)

    # 2. CREATE FIGURE
    fig = make_subplots(
        rows=1, cols=2, 
        specs=[[{'type': 'polar'}, {'type': 'xy'}]],
        column_widths=[0.4, 0.6]
    )

    # Voltage Vector (Line only)
    fig.add_trace(go.Scatterpolar(r=[0, V_m], theta=[0, theta_deg], mode='lines', 
                                 line=dict(color='crimson', width=4), name='Voltage'), row=1, col=1)
    
    # Current Vector (Line only)
    fig.add_trace(go.Scatterpolar(r=[0, I_m], theta=[0, theta_deg + phi_deg], mode='lines', 
                                 line=dict(color='dodgerblue', width=4), name='Current'), row=1, col=1)

    # 3. ADD ARROW TIPS USING ANNOTATIONS
    # Voltage Arrow
    fig.add_annotation(
        dict(ax=0, ay=0, axref='pixel', ayref='pixel',
             x=theta_deg, y=V_m, xref='x1', yref='y1', # x1/y1 refers to polar subplot
             showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor='crimson'),
        row=1, col=1
    )
    # Current Arrow
    fig.add_annotation(
        dict(ax=0, ay=0, axref='pixel', ayref='pixel',
             x=theta_deg + phi_deg, y=I_m, xref='x1', yref='y1',
             showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor='dodgerblue'),
        row=1, col=1
    )

    # 4. WAVEFORMS (Keep the same as before)
    fig.add_trace(go.Scatter(x=t_axis, y=v_wave, line=dict(color='crimson', width=1), opacity=0.3, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[v_inst], mode='markers', marker=dict(size=12, color='crimson'), showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=t_axis, y=i_wave, line=dict(color='dodgerblue', width=1), opacity=0.3, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[i_inst], mode='markers', marker=dict(size=12, color='dodgerblue'), showlegend=False), row=1, col=2)

    fig.update_layout(height=450, polar=dict(radialaxis=dict(range=[0, 10])), showlegend=True)
    fig.update_xaxes(range=[0, 360], row=1, col=2)
    fig.update_yaxes(range=[-11, 11], row=1, col=2)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
