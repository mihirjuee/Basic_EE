import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Full Phasor Lab", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #000000; }
    p, h1, h2, h3, span { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & LOGO ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=100)
    except:
        st.markdown("### ⚡ **EE-LAB**")
with col_title:
    st.title("Complete 3-Phase Star & Delta Relationships")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Controls")
v_mag = st.sidebar.slider("Voltage Magnitude (V_ph)", 50.0, 240.0, 120.0)
i_mag = st.sidebar.slider("Current Magnitude (I_ph)", 1.0, 20.0, 10.0)
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 30)

# --- MATH CONSTANTS ---
rad120 = np.deg2rad(120)
phi = np.deg2rad(phi_deg)
colors = ['#E63946', '#FFB703', '#1D3557'] # Red, Yellow, Blue

# --- UNIVERSAL PLOTTING FUNCTION ---
def draw_phasors(ax, p_vecs, l_vecs, p_labels, l_labels, title, draw_para=True, is_voltage=True):
    ax.set_facecolor('white')
    limit = max(np.abs(l_vecs)) * 1.5
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    ax.axhline(0, color='black', lw=0.8, alpha=0.2)
    ax.axvline(0, color='black', lw=0.8, alpha=0.2)

    # 1. Parallelogram Logic (Only if magnitudes differ, i.e., Star Voltage or Delta Current)
    if draw_para:
        for i in range(3):
            p_vec = p_vecs[i]
            neg_vec = -p_vecs[(i + 1) % 3] if is_voltage else -p_vecs[(i - 1) % 3]
            resultant = l_vecs[i]
            ax.plot([p_vec.real, resultant.real], [p_vec.imag, resultant.imag], 'k--', lw=0.8, alpha=0.3)
            ax.plot([neg_vec.real, resultant.real], [neg_vec.imag, resultant.imag], 'k--', lw=0.8, alpha=0.3)
            ax.plot([0, neg_vec.real], [0, neg_vec.imag], 'k:', lw=1, alpha=0.2)

    # 2. Draw Vectors
    for i in range(3):
        # Phase (Thinner)
        ax.annotate('', xy=(p_vecs[i].real, p_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1.5, alpha=0.6))
        # Line (Thicker)
        ax.annotate('', xy=(l_vecs[i].real, l_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=colors[i], lw=3.5))
        # Labels
        ax.text(l_vecs[i].real*1.2, l_vecs[i].imag*1.2, l_labels[i], color=colors[i], fontweight='bold')

    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Voltages
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
V_line_star = [Van-Vbn, Vbn-Vcn, Vcn-Van]  # V_L = sqrt(3)V_ph
V_line_delta = [Van, Vbn, Vcn]             # V_L = V_ph

# Currents
I_ph = i_mag * np.exp(-1j * phi)
Ian = I_ph; Ibn = I_ph * np.exp(-1j * rad120); Icn = I_ph * np.exp(1j * rad120)
Iab = I_ph; Ibc = I_ph * np.exp(-1j * rad120); Ica = I_ph * np.exp(1j * rad120)

I_line_star = [Ian, Ibn, Icn]             # I_L = I_ph
I_line_delta = [Iab-Ica, Ibc-Iab, Ica-Ibc] # I_L = sqrt(3)I_ph

# --- UI LAYOUT ---
st.markdown("### 📊 Star (Y) Connection")
c1, c2 = st.columns(2)
with c1:
    fig1, ax1 = plt.subplots(figsize=(5,5))
    draw_phasors(ax1, [Van, Vbn, Vcn], V_line_star, ["Van", "Vbn", "Vcn"], ["Vab", "Vbc", "Vca"], "Voltage (V_L = √3 V_ph)", True, True)
    st.pyplot(fig1)
with c2:
    fig2, ax2 = plt.subplots(figsize=(5,5))
    draw_phasors(ax2, [Ian, Ibn, Icn], I_line_star, ["", "", ""], ["Ia", "Ib", "Ic"], "Current (I_L = I_ph)", False, False)
    st.pyplot(fig2)

st.divider()

st.markdown("### 📊 Delta (Δ) Connection")
c3, c4 = st.columns(2)
with c3:
    fig3, ax3 = plt.subplots(figsize=(5,5))
    draw_phasors(ax3, [Iab, Ibc, Ica], I_line_delta, ["Iab", "Ibc", "Ica"], ["Ia", "Ib", "Ic"], "Current (I_L = √3 I_ph)", True, False)
    st.pyplot(fig3)
with c4:
    fig4, ax4 = plt.subplots(figsize=(5,5))
    draw_phasors(ax4, [Van, Vbn, Vcn], V_line_delta, ["", "", ""], ["Vab", "Vbc", "Vca"], "Voltage (V_L = V_ph)", False, True)
    st.pyplot(fig4)
