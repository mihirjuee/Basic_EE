import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
import io

# --- Page Config ---
st.set_page_config(page_title="Parallel RLC Analyzer", layout="wide")

# --- UI Sidebar (Inputs) ---
st.sidebar.header("Circuit Parameters")
V_rms = st.sidebar.number_input("Source Voltage (Vrms)", value=120.0)
freq = st.sidebar.number_input("Frequency (Hz)", value=60.0)
R = st.sidebar.number_input("Resistance (Ω)", value=50.0)
L_mH = st.sidebar.number_input("Inductance (mH)", value=150.0)
C_uF = st.sidebar.number_input("Capacitance (μF)", value=40.0)

# View Toggle
view_mode = st.sidebar.radio("Display Mode", ["Mobile (Stacked)", "Desktop (Side-by-Side)"])

# --- Calculations ---
def calculate_parallel_rlc(V, f, r, l_mh, c_uf):
    omega = 2 * np.pi * f
    L, C = l_mh / 1000, c_uf / 1e6
    xl, xc = omega * L, 1 / (omega * C)
    
    ir, il, ic = V/r, V/xl, V/xc
    i_net_react = ic - il
    i_total = np.sqrt(ir**2 + i_net_react**2)
    z = V / i_total
    phase = np.degrees(np.arctan2(i_net_react, ir))
    
    return ir, il, ic, i_total, z, phase

ir, il, ic, itot, z, phase = calculate_parallel_rlc(V_rms, freq, R, L_mH, C_uF)

# --- Circuit Diagram Function ---
def get_circuit_diagram():
    with schemdraw.Drawing(show=False) as d:
        d += elm.SourceSin().label(f'{V_rms}V')
        d += elm.Line().right().length(1)
        d += (top := elm.Line().right().length(3))
        d += elm.Resistor().at(top.start).down().label(f'R\n{R}Ω')
        d += elm.Inductor().at(top.center).down().label(f'L\n{L_mH}mH')
        d += elm.Capacitor().at(top.end).down().label(f'C\n{C_uF}μF')
        d += elm.Line().at(d.here).left().length(3)
        d += elm.Line().left().length(1)
        buf = io.BytesIO()
        d.save(buf, format='png')
        return buf

# --- Phasor Diagram Function ---
def get_phasor_diagram():
    fig = go.Figure()
    # Define vectors
    vecs = [
        (ir, 0, 'Ir', 'green'),
        (0, ic, 'Ic', 'blue'),
        (0, -il, 'Il', 'red'),
        (ir, ic - il, 'I Total', 'black')
    ]
    for x, y, name, color in vecs:
        fig.add_annotation(
            ax=0, ay=0, axref='x', ayref='y',
            x=x, y=y, xref='x', yref='y',
            showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=4, arrowcolor=color,
            text=name, standoff=5
        )
    limit = max(ir, il, ic) * 1.3
    fig.update_layout(
        xaxis=dict(range=[-limit/2, limit*1.2], title="In-phase (A)"),
        yaxis=dict(range=[-limit, limit], title="Quadrature (A)"),
        height=450, margin=dict(l=20, r=20, t=40, b=20),
        title="Current Phasor Diagram"
    )
    return fig

# --- Main App Layout ---
st.title("⚡ Parallel RLC Analysis")

if view_mode == "Desktop (Side-by-Side)":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Circuit Schematic")
        st.image(get_circuit_diagram())
        st.metric("Total Impedance (Z)", f"{z:.2f} Ω")
    with col2:
        st.subheader("Phasor Analysis")
        st.plotly_chart(get_phasor_diagram(), use_container_width=True)
        st.metric("Total Current (Itot)", f"{itot:.2f} A", delta=f"{phase:.1f}° Phase")
else:
    # Mobile View: Stacked
    st.subheader("Circuit Schematic")
    st.image(get_circuit_diagram())
    
    st.subheader("Phasor Analysis")
    st.plotly_chart(get_phasor_diagram(), use_container_width=True)
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Impedance", f"{z:.2f} Ω")
    col_m2.metric("Total Current", f"{itot:.2f} A")

# Data Table
with st.expander("View Full Calculations"):
    st.table({
        "Parameter": ["Resistive Current (Ir)", "Inductive Current (Il)", "Capacitive Current (Ic)", "Phase Angle"],
        "Value": [f"{ir:.3f} A", f"{il:.3f} A", f"{ic:.3f} A", f"{phase:.2f}°"]
    })
