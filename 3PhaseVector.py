import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Phasor Lab Pro", layout="wide")

# --- LOGO & HEADER ---
col1, col2 = st.columns([1, 8])
with col1:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("⚡") # Fallback icon if logo.png is missing
with col2:
    st.title("Comprehensive 3-Phase Phasor Simulator")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ System Parameters")
    v_rms = st.slider("Voltage Magnitude", 100.0, 240.0, 120.0)
    i_rms = st.slider("Current Magnitude", 1.0, 20.0, 10.0)
    pf_angle = st.slider("Power Factor Angle (θ°)", -90, 90, 30)
    st.info("θ > 0: Lagging (Inductive)\n\nθ < 0: Leading (Capacitive)")

# --- CALCULATIONS ---
theta = np.deg2rad(pf_angle)
rad120 = np.deg2rad(120)

# 1. VOLTAGE IN DELTA (V_line = V_phase)
Vab = v_rms * np.exp(1j * 0)
Vbc = v_rms * np.exp(-1j * rad120)
Vca = v_rms * np.exp(1j * rad120)

# 2. CURRENT IN STAR (I_line = I_phase)
# Currents typically lag/lead the voltage reference
Ia = i_rms * np.exp(-1j * theta)
Ib = i_rms * np.exp(-1j * (rad120 + theta))
Ic = i_rms * np.exp(1j * (rad120 - theta))

# --- PLOTTING ---
COLORS = {"A": "#FF4B4B", "B": "#FFBD45", "C": "#1C83E1"}

def plot_phasors(vectors, labels, title, unit):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#161b22')
    
    limit = max(np.abs(vectors)) * 1.5
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    # Grid and Circles
    ax.add_artist(plt.Circle((0,0), np.abs(vectors[0]), color='white', fill=False, alpha=0.2, ls='--'))
    ax.axhline(0, color='white', alpha=0.3)
    ax.axvline(0, color='white', alpha=0.3)
    
    for v, col, lab in zip(vectors, COLORS.values(), labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=3, mutation_scale=20))
        ax.text(v.real*1.2, v.imag*1.2, f"{lab}\n{np.abs(v):.1f}{unit}", 
                color=col, fontsize=10, fontweight='bold', ha='center')

    ax.set_title(title, color='white', fontsize=14, pad=20)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- LAYOUT ---
col_v, col_i = st.columns(2)

with col_v:
    st.subheader("🔺 Delta Connection (Voltage)")
    st.write("In Delta, Line Voltage = Phase Voltage")
    fig_v = plot_phasors([Vab, Vbc, Vca], ["Vab", "Vbc", "Vca"], "Voltage Vectors (Δ)", "V")
    st.pyplot(fig_v)

with col_i:
    st.subheader("⭐ Star Connection (Current)")
    st.write("In Star, Line Current = Phase Current")
    fig_i = plot_phasors([Ia, Ib, Ic], ["Ia", "Ib", "Ic"], "Current Vectors (Y)", "A")
    st.pyplot(fig_i)

# --- THEORY SUMMARY ---
with st.expander("📖 View Relationships"):
    st.markdown("""
    **For Delta (Δ) Voltage:**
    - $V_{Line} = V_{Phase}$
    - $V_{ab}$ is used as the 0° reference here.
    
    **For Star (Y) Current:**
    - $I_{Line} = I_{Phase}$
    - $I_a$ lags the voltage reference by the Power Factor angle $\\theta$.
    """)
