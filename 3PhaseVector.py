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
    st.title("Unified Voltage & Current Phasors")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Controls")
v_mag = st.sidebar.slider("Voltage Magnitude (V_ph)", 50.0, 240.0, 150.0)
i_mag = st.sidebar.slider("Current Magnitude (I_ph)", 1.0, 100.0, 80.0) # Scaled for visibility
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 30)

# --- MATH ---
rad120 = np.deg2rad(120)
phi = np.deg2rad(phi_deg)
colors = ['#E63946', '#FFB703', '#1D3557'] # Red, Yellow, Blue

def draw_unified_plot(ax, v_vecs, i_vecs, v_labels, i_labels, title):
    ax.set_facecolor('white')
    limit = max(max(np.abs(v_vecs)), max(np.abs(i_vecs))) * 1.3
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    ax.axhline(0, color='black', lw=0.5, alpha=0.3)
    ax.axvline(0, color='black', lw=0.5, alpha=0.3)

    for i in range(3):
        # VOLTAGE: Solid Thick Lines
        ax.annotate('', xy=(v_vecs[i].real, v_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=colors[i], lw=3))
        ax.text(v_vecs[i].real*1.1, v_vecs[i].imag*1.1, v_labels[i], color=colors[i], fontweight='bold')
        
        # CURRENT: Dashed Lines with Offset label
        ax.annotate('', xy=(i_vecs[i].real, i_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1.5, ls='--'))
        ax.text(i_vecs[i].real*1.1, i_vecs[i].imag*1.1, i_labels[i], color=colors[i], fontstyle='italic')

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Star Calculations
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
# Line Voltages for Star
V_line_star = [Van-Vbn, Vbn-Vcn, Vcn-Van]
# Line Currents for Star (Ian lags Van by phi)
I_line_star = [i_mag * np.exp(-1j * (0 + phi)), 
               i_mag * np.exp(-1j * (rad120 + phi)), 
               i_mag * np.exp(1j * (rad120 - phi))]

# Delta Calculations
# Phase Currents for Delta
Iab = i_mag * np.exp(-1j * phi)
Ibc = i_mag * np.exp(-1j * (rad120 + phi))
Ica = i_mag * np.exp(1j * (rad120 - phi))
# Line Currents for Delta
I_line_delta = [Iab-Ica, Ibc-Iab, Ica-Ibc]
# Line Voltage for Delta (Equal to Phase)
V_line_delta = [Van, Vbn, Vcn]

# --- UI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Star System (Y)")
    st.write("Showing Line Voltage ($V_L$) and Line Current ($I_L$)")
    fig1, ax1 = plt.subplots(figsize=(6,6))
    draw_unified_plot(ax1, V_line_star, I_line_star, 
                      ["Vab", "Vbc", "Vca"], ["Ia", "Ib", "Ic"], "Star: V_line & I_line")
    st.pyplot(fig1)

with col2:
    st.subheader("🔺 Delta System (Δ)")
    st.write("Showing Line Voltage ($V_L$) and Line Current ($I_L$)")
    fig2, ax2 = plt.subplots(figsize=(6,6))
    draw_unified_plot(ax2, V_line_delta, I_line_delta, 
                      ["Vab", "Vbc", "Vca"], ["Ia", "Ib", "Ic"], "Delta: V_line & I_line")
    st.pyplot(fig2)

st.info("**Visual Legend:** Thick Solid Lines = Voltage | Thin Dashed Lines = Current")
