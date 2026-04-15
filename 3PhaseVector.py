import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="3-Phase Phasor", layout="centered")

# --- Logo + Title ---
logo = Image.open("logo.png")  # Replace if needed
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(logo, width=60)
with col_title:
    st.title("Balanced 3-Phase Phasor Diagrams")

st.markdown("Complete 3-phase visualization with parallelogram construction.")

# --- Toggle ---
mode = st.toggle("🖥️ Desktop Mode", value=False)

# --- Input ---
phi_deg = st.slider("Power Factor Angle (Φ)", -90, 90, 30)
phi = np.deg2rad(phi_deg)

# --- Math ---
j = 1j
V = 1.5
I = 1.0

# STAR voltages
Van = V*np.exp(j*0)
Vbn = V*np.exp(-j*np.deg2rad(120))
Vcn = V*np.exp(j*np.deg2rad(120))

Vab = Van - Vbn
Vbc = Vbn - Vcn
Vca = Vcn - Van

Ia = I*np.exp(-j*phi)
Ib = I*np.exp(-j*(np.deg2rad(120)+phi))
Ic = I*np.exp(j*(np.deg2rad(120)-phi))

# DELTA currents
Iab = I*np.exp(-j*phi)
Ibc = I*np.exp(-j*(np.deg2rad(120)+phi))
Ica = I*np.exp(j*(np.deg2rad(120)-phi))

Ia_d = Iab - Ica
Ib_d = Ibc - Iab
Ic_d = Ica - Ibc

# --- Draw Functions ---
def draw_vector(ax, c, color, label):
    ax.annotate('', xy=(c.real, c.imag), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color,
                                width=2, headwidth=8))
    ax.text(c.real*1.1, c.imag*1.1, label, color=color, fontsize=10)

def draw_para(ax, v1, v2, color):
    ax.plot([v1.real, v1.real+v2.real],
            [v1.imag, v1.imag+v2.imag],
            linestyle='--', color=color, alpha=0.6)

    ax.plot([v2.real, v1.real+v2.real],
            [v2.imag, v1.imag+v2.imag],
            linestyle='--', color=color, alpha=0.6)

def setup(ax, title):
    ax.set_title(title)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.grid(True, linestyle=":", alpha=0.4)

# Colors (R-Y-B)
cA = 'red'
cB = 'orange'
cC = 'blue'

# --- STAR ---
def plot_star():
    fig, ax = plt.subplots(figsize=(5,5))
    setup(ax, "Star (Y): Line Voltages")

    # Phase voltages
    draw_vector(ax, Van, cA, 'Van')
    draw_vector(ax, Vbn, cB, 'Vbn')
    draw_vector(ax, Vcn, cC, 'Vcn')

    # Parallelograms
    draw_para(ax, Van, -Vbn, cA)
    draw_para(ax, Vbn, -Vcn, cB)
    draw_para(ax, Vcn, -Van, cC)

    # Line voltages
    draw_vector(ax, Vab, cA, 'Vab')
    draw_vector(ax, Vbc, cB, 'Vbc')
    draw_vector(ax, Vca, cC, 'Vca')

    st.pyplot(fig)
    plt.close(fig)

# --- DELTA ---
def plot_delta():
    fig, ax = plt.subplots(figsize=(5,5))
    setup(ax, "Delta (Δ): Line Currents")

    # Phase currents
    draw_vector(ax, Iab, cA, 'Iab')
    draw_vector(ax, Ibc, cB, 'Ibc')
    draw_vector(ax, Ica, cC, 'Ica')

    # Parallelograms
    draw_para(ax, Iab, -Ica, cA)
    draw_para(ax, Ibc, -Iab, cB)
    draw_para(ax, Ica, -Ibc, cC)

    # Line currents
    draw_vector(ax, Ia_d, cA, 'Ia')
    draw_vector(ax, Ib_d, cB, 'Ib')
    draw_vector(ax, Ic_d, cC, 'Ic')

    st.pyplot(fig)
    plt.close(fig)

# --- Layout ---
if mode:
    col1, col2 = st.columns(2)
    with col1:
        plot_star()
    with col2:
        plot_delta()
else:
    plot_star()
    plot_delta()

# --- Notes ---
st.markdown("""
### 🔍 Full 3-Phase Insight

⭐ **Star (Y):**
- Vab = Van − Vbn  
- Vbc = Vbn − Vcn  
- Vca = Vcn − Van  

🔺 **Delta (Δ):**
- Ia = Iab − Ica  
- Ib = Ibc − Iab  
- Ic = Ica − Ibc  

👉 Each dotted shape = **Parallelogram Law**
""")
