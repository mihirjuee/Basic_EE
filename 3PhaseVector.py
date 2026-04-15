import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG (Mobile First) ---
st.set_page_config(page_title="EE Phasor Lab Pro", layout="centered")

# --- MODE TOGGLE ---
desktop = st.toggle("🖥️ Desktop Mode", value=False)

# --- HEADER ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=80)
    except:
        st.markdown("## ⚡")
with col_title:
    st.title("EE Unified Phasor Lab")

st.caption("Professional visualization of 3-phase systems with vector construction")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎛️ Controls")
    v_mag = st.slider("Voltage Magnitude", 50.0, 240.0, 150.0)
    i_mag = st.slider("Current Magnitude", 1.0, 100.0, 80.0)
    phi_deg = st.slider("Power Factor Angle (Φ°)", -90, 90, 30)
    st.markdown("⚡ Lagging (+) | Leading (-)")

# --- MATH ---
phi = np.deg2rad(phi_deg)
rad120 = np.deg2rad(120)

# Colors (Professional R-Y-B)
COL = ["#E63946", "#FFB703", "#1D3557"]

# Base Voltages
Van = v_mag*np.exp(1j*0)
Vbn = v_mag*np.exp(-1j*rad120)
Vcn = v_mag*np.exp(1j*rad120)
Vph = [Van, Vbn, Vcn]

# --- STAR ---
Vline_star = [Van-Vbn, Vbn-Vcn, Vcn-Van]
Iline_star = [
    i_mag*np.exp(-1j*(0+phi)),
    i_mag*np.exp(-1j*(rad120+phi)),
    i_mag*np.exp(1j*(rad120-phi))
]

# --- DELTA ---
Iph_delta = [
    i_mag*np.exp(-1j*phi),
    i_mag*np.exp(-1j*(rad120+phi)),
    i_mag*np.exp(1j*(rad120-phi))
]

Iline_delta = [
    Iph_delta[0]-Iph_delta[2],
    Iph_delta[1]-Iph_delta[0],
    Iph_delta[2]-Iph_delta[1]
]

# --- DRAW ENGINE ---
def draw_system(ax, is_star=True):
    ax.set_facecolor("white")

    limit = max(v_mag, i_mag) * 2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    # Axis
    ax.axhline(0, lw=0.8, alpha=0.3)
    ax.axvline(0, lw=0.8, alpha=0.3)

    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(3):

        if is_star:
            # Components for Vab = Van - Vbn
            comp1 = Vph[i]
            comp2 = -Vph[(i+1)%3]
            resultant = Vline_star[i]

            current = Iline_star[i]
            voltage = resultant

        else:
            # Components for Ia = Iab - Ica
            comp1 = Iph_delta[i]
            comp2 = -Iph_delta[(i-1)%3]
            resultant = Iline_delta[i]

            current = resultant
            voltage = Vph[i]

        # --- PARALLELOGRAM ---
        ax.plot([comp1.real, resultant.real],
                [comp1.imag, resultant.imag],
                linestyle='--', color=COL[i], alpha=0.5)

        ax.plot([comp2.real, resultant.real],
                [comp2.imag, resultant.imag],
                linestyle='--', color=COL[i], alpha=0.5)

        # --- VOLTAGE VECTOR (SOLID) ---
        ax.annotate('', xy=(voltage.real, voltage.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', lw=3, color=COL[i]))

        ax.text(voltage.real*1.12, voltage.imag*1.12,
                f"V{i+1}", color=COL[i], fontsize=10, weight='bold')

        # --- CURRENT VECTOR (DASHED) ---
        ax.annotate('', xy=(current.real, current.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', lw=2,
                                    linestyle='--', color=COL[i]))

        ax.text(current.real*1.12, current.imag*1.12,
                f"I{i+1}", color=COL[i], fontsize=9)

# --- PLOTS ---
def plot_star():
    fig, ax = plt.subplots(figsize=(5,5))
    draw_system(ax, is_star=True)
    ax.set_title("⭐ Star (Y)\nLine Voltage = Vector Difference", fontsize=13)
    st.pyplot(fig)

def plot_delta():
    fig, ax = plt.subplots(figsize=(5,5))
    draw_system(ax, is_star=False)
    ax.set_title("🔺 Delta (Δ)\nLine Current = Vector Difference", fontsize=13)
    st.pyplot(fig)

# --- LAYOUT ---
st.markdown("### 📊 Simulation")

if desktop:
    c1, c2 = st.columns(2)
    with c1: plot_star()
    with c2: plot_delta()
else:
    plot_star()
    plot_delta()

# --- INFO PANEL ---
st.markdown("""
---
### 🧠 Interpretation Guide

- **Solid vectors → Voltage**
- **Dashed vectors → Current**
- **Dotted lines → Parallelogram construction**

#### ⭐ Star (Y)
- Line voltage is formed by **vector subtraction of phase voltages**

#### 🔺 Delta (Δ)
- Line current is formed by **vector subtraction of phase currents**
""")
