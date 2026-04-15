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
    limit = max(max(np.abs(v_line_star)), max(np.abs(i_line_delta))) * 1.3
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    ax.axhline(0, color='black', lw=0.5, alpha=0.3)
    ax.axvline(0, color='black', lw=0.5, alpha=0.3)

    for i in range(3):
        # 1. PARALLELOGRAM CONSTRUCTION
        # In Star, we show Voltage construction. In Delta, we show Current construction.
        if is_star:
            # Vab = Van - Vbn
            comp1 = p_vecs[i] # Van
            comp2 = -p_vecs[(i+1)%3] # -Vbn
            res = l_vecs[i] # Vab
        else:
            # Ia = Iab - Ica (Phase branches)
            # For Delta current, we use the phase currents as components
            p_curr = i_vecs[i] # Iab
            neg_p_curr = -i_vecs[(i-1)%3] # -Ica
            res = l_vecs[i] # Ia
            comp1, comp2 = p_curr, neg_p_curr

        # Draw dotted construction lines
        ax.plot([comp1.real, res.real], [comp1.imag, res.imag], 'k--', lw=0.8, alpha=0.2)
        ax.plot([comp2.real, res.real], [comp2.imag, res.imag], 'k--', lw=0.8, alpha=0.2)
        ax.plot([0, comp2.real], [0, comp2.imag], 'k:', lw=1, alpha=0.1)

        # 2. DRAW VECTORS
        # Voltage (Solid)
        v_vec = v_vecs_star[i] if is_star else l_vecs[i] # This is just for labelling logic
        ax.annotate('', xy=(l_vecs[i].real, l_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=colors[i], lw=3))
        
        # Current (Dashed)
        curr_vec = i_vecs[i]
        ax.annotate('', xy=(curr_vec.real, curr_vec.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1.5, ls='--'))

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Base Phase Voltages (Used for both)
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
v_phases = [Van, Vbn, Vcn]

# --- STAR (Y) ---
v_line_star = [Van-Vbn, Vbn-Vcn, Vcn-Van]
# Line current in star = Phase current (lags Van by phi)
i_line_star = [i_mag * np.exp(-1j*(0+phi)), 
               i_mag * np.exp(-1j*(rad120+phi)), 
               i_mag * np.exp(1j*(rad120-phi))]

# --- DELTA (Δ) ---
# Phase currents in Delta
i_ph_delta = [i_mag * np.exp(-1j*phi), 
              i_mag * np.exp(-1j*(rad120+phi)), 
              i_mag * np.exp(1j*(rad120-phi))]
# Line currents in Delta
i_line_delta = [i_ph_delta[0]-i_ph_delta[2], 
                i_ph_delta[1]-i_ph_delta[0], 
                i_ph_delta[2]-i_ph_delta[1]]
v_line_delta = v_phases # V_L = V_ph

# --- UI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Star: Voltage Subtraction")
    fig1, ax1 = plt.subplots(figsize=(6,6))
    # We pass phase voltages to build line voltage parallelograms
    draw_unified_with_para(ax1, v_phases, v_line_star, i_line_star, "Star (Y) Connection", is_star=True)
    st.pyplot(fig1)

with col2:
    st.subheader("🔺 Delta: Current Subtraction")
    fig2, ax2 = plt.subplots(figsize=(6,6))
    # We pass phase currents to build line current parallelograms
    draw_unified_with_para(ax2, v_line_delta, i_line_delta, i_ph_delta, "Delta (Δ) Connection", is_star=False)
    st.pyplot(fig2)

st.markdown("""
---
### 💡 How to read these diagrams:
1. **Solid Lines:** Line Voltages ($V_{ab}, V_{bc}, V_{ca}$).
2. **Dashed Lines:** Line Currents ($I_a, I_b, I_c$).
3. **Parallelograms:** * In **Star**, they show how phase voltages $V_{an}$ and $-V_{bn}$ create $V_{ab}$.
    * In **Delta**, they show how phase currents $I_{ab}$ and $-I_{ca}$ create $I_a$.
""")
