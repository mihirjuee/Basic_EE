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

st.markdown("Visualizing how line quantities are formed using parallelogram law.")

# --- Toggle ---
mode = st.toggle("🖥️ Desktop Mode", value=False)

# --- Input ---
phi_deg = st.slider("Power Factor Angle (Φ)", -90, 90, 30)
phi = np.deg2rad(phi_deg)

# --- Math ---
j = 1j
V_mag = 1.5
I_mag = 1.0

# STAR
Van = V_mag * np.exp(j * 0)
Vbn = V_mag * np.exp(-j * np.deg2rad(120))
Vcn = V_mag * np.exp(j * np.deg2rad(120))

Vab = Van - Vbn
Vbc = Vbn - Vcn
Vca = Vcn - Van

Ia = I_mag * np.exp(-j * phi)
Ib = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ic = I_mag * np.exp(j * (np.deg2rad(120) - phi))

# DELTA
Vab_d = V_mag * 1.732 * np.exp(j * 0)
Vbc_d = V_mag * 1.732 * np.exp(-j * np.deg2rad(120))
Vca_d = V_mag * 1.732 * np.exp(j * np.deg2rad(120))

Iab = I_mag * np.exp(-j * phi)
Ibc = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ica = I_mag * np.exp(j * (np.deg2rad(120) - phi))

Ia_d = Iab - Ica
Ib_d = Ibc - Iab
Ic_d = Ica - Ibc

# --- Draw Functions ---
def draw_vector(ax, c, color, label):
    ax.annotate('', xy=(c.real, c.imag), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color,
                                width=2, headwidth=8))
    ax.text(c.real*1.1, c.imag*1.1, label, color=color, fontsize=10)

def draw_parallelogram(ax, v1, v2, color):
    # v1 -> v1+v2
    ax.plot([v1.real, v1.real + v2.real],
            [v1.imag, v1.imag + v2.imag],
            linestyle='--', color=color, alpha=0.6)

    # v2 -> v1+v2
    ax.plot([v2.real, v1.real + v2.real],
            [v2.imag, v1.imag + v2.imag],
            linestyle='--', color=color, alpha=0.6)

def setup(ax, title):
    ax.set_title(title)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.grid(True, linestyle=":", alpha=0.4)

# --- STAR PLOT ---
def plot_star():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup(ax, "Star (Y): Line Voltage Formation")

    # Phase voltages
    draw_vector(ax, Van, 'red', 'Van')
    draw_vector(ax, -Vbn, 'orange', '-Vbn')

    # Parallelogram (Van + (-Vbn) = Vab)
    draw_parallelogram(ax, Van, -Vbn, 'red')

    # Resultant
    draw_vector(ax, Vab, 'red', 'Vab')

    st.pyplot(fig)
    plt.close(fig)

# --- DELTA PLOT ---
def plot_delta():
    fig, ax = plt.subplots(figsize=(5, 5))
    setup(ax, "Delta (Δ): Line Current Formation")

    # Phase currents
    draw_vector(ax, Iab, 'red', 'Iab')
    draw_vector(ax, -Ica, 'blue', '-Ica')

    # Parallelogram (Iab + (-Ica) = Ia)
    draw_parallelogram(ax, Iab, -Ica, 'red')

    # Resultant
    draw_vector(ax, Ia_d, 'red', 'Ia')

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

# --- Explanation ---
st.markdown("""
### 🔍 Understanding the Construction

#### ⭐ Star (Y)
- Line voltage is vector difference:
  **Vab = Van − Vbn**
- Shown using **parallelogram (dotted lines)**

#### 🔺 Delta (Δ)
- Line current is vector difference:
  **Ia = Iab − Ica**
- Again formed using **parallelogram law**

---

👉 These dotted lines help students *visually understand* how line quantities are derived.
""")
