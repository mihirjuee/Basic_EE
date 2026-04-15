import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Unified Phasor Lab", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #000000; }
    p, h1, h2, h3, span { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try: st.image("logo.png", width=100)
    except: st.markdown("### ⚡ **EE-LAB**")
with col_title:
    st.title("Unified Phasors with Parallelogram Geometry")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Controls")
v_mag = st.sidebar.slider("Voltage Magnitude (V_ph)", 50.0, 240.0, 150.0)
i_mag = st.sidebar.slider("Current Magnitude (I_ph)", 1.0, 100.0, 80.0)
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 30)

# --- MATH ---
rad120 = np.deg2rad(120)
phi = np.deg2rad(phi_deg)
colors = ['#E63946', '#FFB703', '#1D3557'] # Red, Yellow, Blue

def draw_unified_with_para(ax, p_vecs, l_vecs, i_vecs, title, is_star=True):
    ax.set_facecolor('white')
    # Set limit based on the largest possible vector (sqrt(3) * magnitude)
    limit = max(v_mag, i_mag) * 2.0
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    ax.axhline(0, color='black', lw=0.5, alpha=0.3)
    ax.axvline(0, color='black', lw=0.5, alpha=0.3)

    v_labels = ["Vab", "Vbc", "Vca"]
    i_labels = ["Ia", "Ib", "Ic"]

    for i in range(3):
        # 1. PARALLELOGRAM CONSTRUCTION
        if is_star:
            comp1 = p_vecs[i] # Van
            comp2 = -p_vecs[(i+1)%3] # -Vbn
            res = l_vecs[i] # Vab
        else:
            comp1 = i_vecs[i] # Iab (branch)
            comp2 = -i_vecs[(i-1)%3] # -Ica (branch)
            res = l_vecs[i] # Ia (line)

        # Draw dotted construction lines
        ax.plot([comp1.real, res.real], [comp1.imag, res.imag], 'k--', lw=0.8, alpha=0.2)
        ax.plot([comp2.real, res.real], [comp2.imag, res.imag], 'k--', lw=0.8, alpha=0.2)
        ax.plot([0, comp2.real], [0, comp2.imag], 'k:', lw=1, alpha=0.1)

        # 2. DRAW VECTORS
        # Voltage (Solid Line)
        # In Star, l_vecs are line voltages. In Delta, v_phases are line voltages.
        v_to_draw = l_vecs[i] if is_star else p_vecs[i] 
        ax.annotate('', xy=(v_to_draw.real, v_to_draw.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=colors[i], lw=3))
        ax.text(v_to_draw.real*1.1, v_to_draw.imag*1.1, v_labels[i], color=colors[i], fontweight='bold')
        
        # Current (Dashed Line)
        # In Star, i_vecs are line currents. In Delta, l_vecs are line currents.
        i_to_draw = i_vecs[i] if is_star else l_vecs[i]
        ax.annotate('', xy=(i_to_draw.real, i_to_draw.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1.5, ls='--'))
        ax.text(i_to_draw.real*1.1, i_to_draw.imag*1.1, i_labels[i], color=colors[i], fontstyle='italic')

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Base Voltages
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
v_phases = [Van, Vbn, Vcn]

# STAR (Y)
v_line_star = [Van-Vbn, Vbn-Vcn, Vcn-Van]
i_line_star = [i_mag * np.exp(-1j*(0+phi)), 
               i_mag * np.exp(-1j*(rad120+phi)), 
               i_mag * np.exp(1j*(rad120-phi))]

# DELTA (Δ)
i_ph_delta = [i_mag * np.exp(-1j*phi), 
              i_mag * np.exp(-1j*(rad120+phi)), 
              i_mag * np.exp(1j*(rad120-phi))]
i_line_delta = [i_ph_delta[0]-i_ph_delta[2], 
                i_ph_delta[1]-i_ph_delta[0], 
                i_ph_delta[2]-i_ph_delta[1]]

# --- UI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Star Connection (Y)")
    fig1, ax1 = plt.subplots(figsize=(6,6))
    draw_unified_with_para(ax1, v_phases, v_line_star, i_line_star, "Star: V_line & I_line", is_star=True)
    st.pyplot(fig1)

with col2:
    st.subheader("🔺 Delta Connection (Δ)")
    fig2, ax2 = plt.subplots(figsize=(6,6))
    # In Delta, Voltage Line = Voltage Phase, so we pass v_phases as l_vecs
    draw_unified_with_para(ax2, v_phases, i_line_delta, i_ph_delta, "Delta: V_line & I_line", is_star=False)
    st.pyplot(fig2)

st.divider()
st.info("**Solid:** Line Voltage | **Dashed:** Line Current | **Dotted Lines:** Vector Subtraction Construction")
