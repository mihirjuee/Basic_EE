import matplotlib
matplotlib.use('Agg') # MUST BE LINE 1
import matplotlib.pyplot as plt

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io

# --- Page Config ---
st.set_page_config(page_title="Parallel RLC Analyzer", layout="wide")

# --- Calculations ---
def calculate_parallel_rlc(V, f, r, l_mh, c_uf):
    omega = 2 * np.pi * f
    L, C = l_mh / 1000, c_uf / 1e6
    xl = omega * L if (omega * L) > 0 else 1e-9
    xc = 1 / (omega * C) if (omega * C) > 0 else 1e9
    
    ir, il, ic = V/r, V/xl, V/xc
    i_net_react = ic - il
    i_total = np.sqrt(ir**2 + i_net_react**2)
    z = V / i_total if i_total > 0 else 0
    phase = np.degrees(np.arctan2(i_net_react, ir))
    
    return ir, il, ic, i_total, z, phase

# --- Diagram Generators ---
def get_circuit_diagram(V, r_val, l_val, c_val):

    d = schemdraw.Drawing(show=False)
    d.config(unit=2)

    # --- Main loop (SAFE sequential layout) ---
    d += elm.SourceSin().label(f'{V}V', loc='left')
    d += elm.Line().right().length(1)

    d += elm.Resistor().down().label(f'{r_val} Ω', loc='right')
    d += elm.Line().right().length(2)

    d += elm.Inductor().up().label(f'{l_val} mH', loc='right')
    d += elm.Line().left().length(2)

    d += elm.Capacitor().up().label(f'{c_val} μF', loc='right')

    d += elm.Line().left().length(1)

    # --- Convert to image safely ---
    buf = io.BytesIO()
    d.save(buf)
    buf.seek(0)

    return buf

def get_phasor_diagram(ir, il, ic):
    fig = go.Figure()
    vecs = [
        (ir, 0, 'Ir (Resistive)', 'green'),
        (0, ic, 'Ic (Capacitive)', 'blue'),
        (0, -il, 'Il (Inductive)', 'red'),
        (ir, ic - il, 'I Total', 'black')
    ]
    for x, y, name, color in vecs:
        fig.add_annotation(
            ax=0, ay=0, axref='x', ayref='y',
            x=x, y=y, xref='x', yref='y',
            showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=4, arrowcolor=color,
            text=name, standoff=5
        )
    limit = max(ir, il, ic, abs(ic-il)) * 1.3
    fig.update_layout(
        xaxis=dict(range=[-limit/3, limit*1.2], title="In-phase (A)", zeroline=True),
        yaxis=dict(range=[-limit, limit], title="Quadrature (A)", zeroline=True),
        height=450, margin=dict(l=20, r=20, t=40, b=20),
        title="Current Phasor Diagram"
    )
    return fig

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")
V_rms = st.sidebar.number_input("Source Voltage (Vrms)", value=120.0)
freq = st.sidebar.number_input("Frequency (Hz)", value=60.0)
R_in = st.sidebar.number_input("Resistance (Ω)", value=50.0)
L_in = st.sidebar.number_input("Inductance (mH)", value=150.0)
C_in = st.sidebar.number_input("Capacitance (μF)", value=40.0)
view_mode = st.sidebar.radio("Display Mode", ["Mobile (Stacked)", "Desktop (Side-by-Side)"])

# Run Calculations
ir, il, ic, itot, z, phase = calculate_parallel_rlc(V_rms, freq, R_in, L_in, C_in)

# --- Main UI ---
st.title("⚡ Parallel RLC Analysis")

if view_mode == "Desktop (Side-by-Side)":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Circuit Schematic")
        st.image(get_circuit_diagram(V_rms, R_in, L_in, C_in))
        st.metric("Total Impedance (Z)", f"{z:.2f} Ω")
    with col2:
        st.subheader("Phasor Analysis")
        st.plotly_chart(get_phasor_diagram(ir, il, ic), use_container_width=True)
        st.metric("Total Current (Itot)", f"{itot:.2f} A", delta=f"{phase:.1f}° Phase")
else:
    # Mobile Stacked View
    st.subheader("Circuit Schematic")
    st.image(get_circuit_diagram(V_rms, R_in, L_in, C_in))
    st.metric("Total Impedance (Z)", f"{z:.2f} Ω")
    
    st.divider()
    
    st.subheader("Phasor Analysis")
    st.plotly_chart(get_phasor_diagram(ir, il, ic), use_container_width=True)
    st.metric("Total Current (Itot)", f"{itot:.2f} A", delta=f"{phase:.1f}° Phase")

with st.expander("Detailed Branch Currents"):
    st.write(f"**Ir:** {ir:.3f} A | **Il:** {il:.3f} A | **Ic:** {ic:.3f} A")
