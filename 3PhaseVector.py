import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="3-Phase Simulator", layout="centered")

# --- HEADER ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=70)  # Replace if needed
with col2:
    st.markdown("## ⚡ 3-Phase Phasor Simulation Tool")

st.markdown("Interactive visualization of **Star (Y)** and **Delta (Δ)** systems.")

# --- MODE ---
desktop_mode = st.toggle("🖥️ Desktop View", value=False)

# --- CONTROL PANEL ---
st.markdown("### 🎛️ Controls")
phi_deg = st.slider("Power Factor Angle (Φ)", -90, 90, 30)
phi = np.deg2rad(phi_deg)

# --- CONSTANTS ---
j = 1j
V = 1.5
I = 1.0

# --- STAR SYSTEM ---
Van = V*np.exp(j*0)
Vbn = V*np.exp(-j*np.deg2rad(120))
Vcn = V*np.exp(j*np.deg2rad(120))

Vab = Van - Vbn
Vbc = Vbn - Vcn
Vca = Vcn - Van

# --- DELTA SYSTEM ---
Iab = I*np.exp(-j*phi)
Ibc = I*np.exp(-j*(np.deg2rad(120)+phi))
Ica = I*np.exp(j*(np.deg2rad(120)-phi))

Ia = Iab - Ica
Ib = Ibc - Iab
Ic = Ica - Ibc

# --- COLORS (Professional EE Standard) ---
COLORS = {
    "A": "#E63946",  # Red
    "B": "#E9C46A",  # Yellow
    "C": "#1D3557"   # Blue
}

# --- DRAW FUNCTIONS ---
def draw_vector(ax, c, color, label, lw=2):
    ax.annotate('', xy=(c.real, c.imag), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', lw=lw, color=color))
    ax.text(c.real*1.1, c.imag*1.1, label, color=color, fontsize=10, weight='bold')

def draw_para(ax, v1, v2, color):
    ax.plot([v1.real, v1.real+v2.real],
            [v1.imag, v1.imag+v2.imag],
            linestyle='--', color=color, alpha=0.5)

    ax.plot([v2.real, v1.real+v2.real],
            [v2.imag, v1.imag+v2.imag],
            linestyle='--', color=color, alpha=0.5)

def setup_axis(ax, title):
    ax.set_title(title, fontsize=13, weight='bold')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, linestyle=":", alpha=0.4)

# --- STAR PLOT ---
def plot_star():
    fig, ax = plt.subplots(figsize=(5,5))
    setup_axis(ax, "⭐ Star (Y) - Line Voltage Formation")

    # Phase voltages
    draw_vector(ax, Van, COLORS["A"], "Van")
    draw_vector(ax, Vbn, COLORS["B"], "Vbn")
    draw_vector(ax, Vcn, COLORS["C"], "Vcn")

    # Parallelograms
    draw_para(ax, Van, -Vbn, COLORS["A"])
    draw_para(ax, Vbn, -Vcn, COLORS["B"])
    draw_para(ax, Vcn, -Van, COLORS["C"])

    # Line voltages
    draw_vector(ax, Vab, COLORS["A"], "Vab", lw=3)
    draw_vector(ax, Vbc, COLORS["B"], "Vbc", lw=3)
    draw_vector(ax, Vca, COLORS["C"], "Vca", lw=3)

    st.pyplot(fig)
    plt.close(fig)

# --- DELTA PLOT ---
def plot_delta():
    fig, ax = plt.subplots(figsize=(5,5))
    setup_axis(ax, "🔺 Delta (Δ) - Line Current Formation")

    # Phase currents
    draw_vector(ax, Iab, COLORS["A"], "Iab")
    draw_vector(ax, Ibc, COLORS["B"], "Ibc")
    draw_vector(ax, Ica, COLORS["C"], "Ica")

    # Parallelograms
    draw_para(ax, Iab, -Ica, COLORS["A"])
    draw_para(ax, Ibc, -Iab, COLORS["B"])
    draw_para(ax, Ica, -Ibc, COLORS["C"])

    # Line currents
    draw_vector(ax, Ia, COLORS["A"], "Ia", lw=3)
    draw_vector(ax, Ib, COLORS["B"], "Ib", lw=3)
    draw_vector(ax, Ic, COLORS["C"], "Ic", lw=3)

    st.pyplot(fig)
    plt.close(fig)

# --- LAYOUT ---
st.markdown("### 📊 Simulation Output")

if desktop_mode:
    col1, col2 = st.columns(2)
    with col1:
        plot_star()
    with col2:
        plot_delta()
else:
    plot_star()
    plot_delta()

# --- LEGEND PANEL ---
st.markdown("""
### 🎨 Phase Color Legend
- 🔴 Phase A  
- 🟡 Phase B  
- 🔵 Phase C  

---

### 📘 Key Concepts
- ⭐ Star: **Line Voltage = Vector Difference of Phase Voltages**
- 🔺 Delta: **Line Current = Vector Difference of Phase Currents**
- Dotted lines show **Parallelogram Law**
""")
