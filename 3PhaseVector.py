import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="3-Phase Phasor", layout="centered")

# --- Logo + Title ---
logo = Image.open("logo.png")  # Replace with your logo file
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(logo, width=60)
with col_title:
    st.title("Balanced 3-Phase Phasor Diagrams")

st.markdown("Compare Star (Y) and Delta (Δ) systems interactively.")

# --- Mode Toggle ---
mode = st.toggle("🖥️ Desktop Mode (Side-by-Side View)", value=False)

# --- Input ---
phi_deg = st.slider("Load Power Factor Angle (Φ)", -90, 90, 30)
phi = np.deg2rad(phi_deg)

# --- Math ---
j = 1j
V_mag = 1.5
I_mag = 1.0

# STAR
Van = V_mag * np.exp(j * 0)
Vbn = V_mag * np.exp(-j * np.deg2rad(120))
Vcn = V_mag * np.exp(j * np.deg2rad(120))

Vab_star = Van - Vbn
Vbc_star = Vbn - Vcn
Vca_star = Vcn - Van

Ia_star = I_mag * np.exp(-j * phi)
Ib_star = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ic_star = I_mag * np.exp(j * (np.deg2rad(120) - phi))

# DELTA
Vab_delta = V_mag * 1.732 * np.exp(j * 0)
Vbc_delta = V_mag * 1.732 * np.exp(-j * np.deg2rad(120))
Vca_delta = V_mag * 1.732 * np.exp(j * np.deg2rad(120))

Iab_delta = I_mag * np.exp(-j * phi)
Ibc_delta = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ica_delta = I_mag * np.exp(j * (np.deg2rad(120) - phi))

Ia_delta = Iab_delta - Ica_delta
Ib_delta = Ibc_delta - Iab_delta
Ic_delta = Ica_delta - Ibc_delta

# --- Drawing Functions ---
def draw_vector(ax, c_end, color, label):
    x, y = c_end.real, c_end.imag
    ax.annotate('', xy=(x, y), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color,
                                width=2, headwidth=8))
    ax.text(x*1.1, y*1.1, label, color=color, fontsize=10)

def setup_ax(ax, title):
    ax.set_title(title, fontsize=12)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.grid(True, linestyle=":", alpha=0.4)

# --- Plot Functions ---
def plot_star():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup_ax(ax, "Star (Y)")

    draw_vector(ax, Van, 'red', 'Van')
    draw_vector(ax, Vbn, 'orange', 'Vbn')
    draw_vector(ax, Vcn, 'blue', 'Vcn')

    draw_vector(ax, Ia_star, 'red', 'Ia')
    draw_vector(ax, Ib_star, 'orange', 'Ib')
    draw_vector(ax, Ic_star, 'blue', 'Ic')

    st.pyplot(fig)
    plt.close(fig)

def plot_delta():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup_ax(ax, "Delta (Δ)")

    draw_vector(ax, Vab_delta, 'red', 'Vab')
    draw_vector(ax, Vbc_delta, 'orange', 'Vbc')
    draw_vector(ax, Vca_delta, 'blue', 'Vca')

    draw_vector(ax, Ia_delta, 'red', 'Ia')
    draw_vector(ax, Ib_delta, 'orange', 'Ib')
    draw_vector(ax, Ic_delta, 'blue', 'Ic')

    st.pyplot(fig)
    plt.close(fig)

# --- Layout Logic ---
if mode:
    # Desktop → Side by side
    col1, col2 = st.columns(2)
    with col1:
        plot_star()
    with col2:
        plot_delta()
else:
    # Mobile → Stacked
    plot_star()
    plot_delta()

# --- Info ---
st.markdown("""
### 🔍 Key Insight
- ⭐ **Star:** Line Voltage leads Phase Voltage by **30°**
- 🔺 **Delta:** Line Current lags Phase Current by **30°**
""")
