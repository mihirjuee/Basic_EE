import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="3-Phase Phasor Lab", layout="wide", page_icon="⚡")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_密=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Simulation Settings")
    phi_deg = st.slider("Power Factor Angle (Φ)", -90, 90, 30, help="Lagging (+) or Leading (-)")
    v_mag = st.slider("Voltage Magnitude (V)", 0.5, 2.5, 1.5)
    show_para = st.checkbox("Show Parallelogram Construction", value=True)
    desktop_mode = st.toggle("🖥️ Side-by-Side View", value=True)
    
    st.divider()
    st.info("The dotted lines represent the vector subtraction: $\\vec{V}_{line} = \\vec{V}_{p1} - \\vec{V}_{p2}$")

# --- MATHEMATICAL ENGINE ---
phi = np.deg2rad(phi_deg)
j = 1j

# Star Calculation (Voltages)
Van = v_mag * np.exp(j*0)
Vbn = v_mag * np.exp(-j * np.deg2rad(120))
Vcn = v_mag * np.exp(j * np.deg2rad(120))

Vab, Vbc, Vca = Van - Vbn, Vbn - Vcn, Vcn - Van

# Delta Calculation (Currents)
I_base = 1.0
Iab = I_base * np.exp(-j * phi)
Ibc = I_base * np.exp(-j * (np.deg2rad(120) + phi))
Ica = I_base * np.exp(j * (np.deg2rad(120) - phi))

Ia, Ib, Ic = Iab - Ica, Ibc - Iab, Ica - Ibc

# --- PLOTTING HELPERS ---
COLORS = {"A": "#FF4B4B", "B": "#FFBD45", "C": "#1C83E1"}

def draw_vector(ax, complex_num, color, label, lw=2, zorder=3):
    ax.annotate('', xy=(complex_num.real, complex_num.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', lw=lw, color=color, mutation_scale=20), zorder=zorder)
    # Offset label slightly from tip
    ax.text(complex_num.real*1.15, complex_num.imag*1.15, label, 
            color=color, fontsize=11, weight='bold', ha='center')

def setup_axis(ax, title):
    ax.set_title(title, fontsize=14, color='white', pad=20)
    ax.set_facecolor('#0e1117')
    limit = 4.5
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    # Draw unit circles for scale
    circle = plt.Circle((0, 0), v_mag, color='white', fill=False, alpha=0.1, linestyle='--')
    ax.add_artist(circle)
    ax.axhline(0, color='white', linewidth=0.5, alpha=0.3)
    ax.axvline(0, color='white', linewidth=0.5, alpha=0.3)
    ax.grid(True, linestyle=":", alpha=0.2)
    ax.set_aspect('equal')
    ax.axis('off')

# --- PLOT FUNCTIONS ---
def create_phasor_plot(system_type):
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#0e1117')
    
    if system_type == "Star":
        setup_axis(ax, "⭐ STAR (Y): Phase to Line Voltage")
        # Phases
        draw_vector(ax, Van, COLORS["A"], "Van")
        draw_vector(ax, Vbn, COLORS["B"], "Vbn")
        draw_vector(ax, Vcn, COLORS["C"], "Vcn")
        # Lines
        draw_vector(ax, Vab, COLORS["A"], "Vab", lw=4)
        draw_vector(ax, Vbc, COLORS["B"], "Vbc", lw=4)
        draw_vector(ax, Vca, COLORS["C"], "Vca", lw=4)
        if show_para:
            ax.plot([Van.real, Vab.real], [Van.imag, Vab.imag], '--', color='gray', alpha=0.5)
            ax.plot([-Vbn.real, Vab.real], [-Vbn.imag, Vab.imag], '--', color='gray', alpha=0.5)

    else:
        setup_axis(ax, "🔺 DELTA (Δ): Phase to Line Current")
        draw_vector(ax, Iab, COLORS["A"], "Iab")
        draw_vector(ax, Ibc, COLORS["B"], "Ibc")
        draw_vector(ax, Ica, COLORS["C"], "Ica")
        draw_vector(ax, Ia, COLORS["A"], "Ia", lw=4)
        draw_vector(ax, Ib, COLORS["B"], "Ib", lw=4)
        draw_vector(ax, Ic, COLORS["C"], "Ic", lw=4)
        if show_para:
            ax.plot([Iab.real, Ia.real], [Iab.imag, Ia.imag], '--', color='gray', alpha=0.5)

    return fig

# --- MAIN UI ---
st.title("⚡ 3-Phase Phasor Analysis Lab")

# Metric Row
m1, m2, m3 = st.columns(3)
m1.metric("Line Voltage Magnitude", f"{np.abs(Vab):.2f} V", f"√3 × {v_mag}")
m2.metric("Line Current Magnitude", f"{np.abs(Ia):.2f} A", f"√3 × {I_base}")
m3.metric("Phase Shift", f"{phi_deg}°")

st.divider()

if desktop_mode:
    col1, col2 = st.columns(2)
    with col1: st.pyplot(create_phasor_plot("Star"))
    with col2: st.pyplot(create_phasor_plot("Delta"))
else:
    st.pyplot(create_phasor_plot("Star"))
    st.pyplot(create_phasor_plot("Delta"))

# --- MATH EXPLORER ---
with st.expander("📝 View Live Vector Equations"):
    st.latex(rf"V_{{ab}} = V_{{an}} - V_{{bn}} = {v_mag}\angle 0^\circ - {v_mag}\angle -120^\circ = {np.abs(Vab):.2f}\angle 30^\circ")
    st.latex(rf"I_{{a}} = I_{{ab}} - I_{{ca}} = {I_base}\angle {-phi_deg}^\circ - {I_base}\angle {120-phi_deg}^\circ")
