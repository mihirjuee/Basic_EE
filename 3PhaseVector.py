import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Phasor Lab Pro", layout="wide")

# --- CUSTOM THEMEING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚡ System Parameters")
    v_rms = st.slider("Phase Voltage (V_ph)", 100.0, 240.0, 120.0)
    i_rms = st.slider("Phase Current (I_ph)", 1.0, 20.0, 10.0)
    pf_angle = st.slider("Power Factor Angle (θ)", -90, 90, 30)
    st.divider()
    st.caption("Positive θ: Lagging (Inductive)")
    st.caption("Negative θ: Leading (Capacitive)")

# --- MATHEMATICAL ENGINE ---
theta = np.deg2rad(pf_angle)
rad120 = np.deg2rad(120)

# STAR (Y) CALCULATIONS
# Phase Voltages
Van = v_rms * np.exp(j*0 if 'j' in locals() else 1j*0)
Vbn = v_rms * np.exp(-1j * rad120)
Vcn = v_rms * np.exp(1j * rad120)
# Line Voltages (V_line = V_ph * sqrt(3) at +30deg shift)
Vab, Vbc, Vca = Van - Vbn, Vbn - Vcn, Vcn - Van

# DELTA (Δ) CALCULATIONS
# Phase Currents
Iab = i_rms * np.exp(-1j * theta)
Ibc = i_rms * np.exp(-1j * (rad120 + theta))
Ica = i_rms * np.exp(1j * (rad120 - theta))
# Line Currents (I_line = I_ph * sqrt(3) at -30deg shift from phase)
Ia, Ib, Ic = Iab - Ica, Ibc - Iab, Ica - Ibc

# --- PLOTTING ENGINE ---
COLORS = {"A": "#FF4B4B", "B": "#FFBD45", "C": "#1C83E1"}

def draw_phasor_set(ax, phase_vecs, line_vecs, p_labels, l_labels, title):
    ax.set_title(title, fontsize=14, color='white', fontweight='bold')
    ax.set_facecolor('#161b22')
    
    # Calculate limits based on max vector length
    limit = max(np.abs(line_vecs)) * 1.3
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    
    # Grid and Circles
    circles = [np.abs(phase_vecs[0]), np.abs(line_vecs[0])]
    for c in circles:
        ax.add_artist(plt.Circle((0,0), c, color='white', fill=False, alpha=0.1, ls='--'))
    
    ax.axhline(0, color='white', alpha=0.2); ax.axvline(0, color='white', alpha=0.2)
    
    # Draw Phase Vectors (Thinner)
    for v, col, lab in zip(phase_vecs, COLORS.values(), p_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.5, alpha=0.7))
        ax.text(v.real*1.1, v.imag*1.1, lab, color=col, fontsize=9)

    # Draw Line Vectors (Thicker)
    for v, col, lab in zip(line_vecs, COLORS.values(), l_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=3))
        ax.text(v.real*1.1, v.imag*1.1, lab, color=col, fontsize=11, fontweight='bold')
    
    ax.set_aspect('equal')
    ax.axis('off')

# --- DISPLAY UI ---
st.title("🌐 3-Phase Comprehensive Phasor Simulator")

tab1, tab2 = st.tabs(["📊 Phasor Visualizer", "📝 Mathematical Proofs"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig_v, ax_v = plt.subplots(figsize=(6,6), facecolor='#0e1117')
        draw_phasor_set(ax_v, [Van, Vbn, Vcn], [Vab, Vbc, Vca], 
                       ["Van", "Vbn", "Vcn"], ["Vab", "Vbc", "Vca"], "VOLTAGE (Star Connection)")
        st.pyplot(fig_v)
        
        st.info(f"**Line Voltage:** {np.abs(Vab):.1f} V (≈ √3 × {v_rms:.1f} V)")

    with col2:
        fig_i, ax_i = plt.subplots(figsize=(6,6), facecolor='#0e1117')
        draw_phasor_set(ax_i, [Iab, Ibc, Ica], [Ia, Ib, Ic], 
                       ["Iab", "Ibc", "Ica"], ["Ia", "Ib", "Ic"], "CURRENT (Delta Connection)")
        st.pyplot(fig_i)
        
        st.info(f"**Line Current:** {np.abs(Ia):.1f} A (≈ √3 × {i_rms:.1f} A)")

with tab2:
    st.subheader("Key Transformation Equations")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Star Connection (Voltage Focus)")
        st.latex(r"V_{line} = \sqrt{3} \cdot V_{phase} \angle 30^\circ")
        st.latex(rf"V_{{ab}} = {np.abs(Vab):.2f} \angle 30^\circ")
    with c2:
        st.markdown("### Delta Connection (Current Focus)")
        st.latex(r"I_{line} = \sqrt{3} \cdot I_{phase} \angle -30^\circ")
        st.latex(rf"I_{{a}} = {np.abs(Ia):.2f} \angle {-30-pf_angle}^\circ")
