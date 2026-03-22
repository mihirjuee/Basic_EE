import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Balanced 3-Phase Phasor Diagrams: Star vs. Delta")
st.markdown("Compare the Voltage and Current relationships under a balanced load.")

# --- Interactive Control ---
phi_deg = st.slider("Load Power Factor Angle (Φ in degrees)", -90, 90, 30, 5)
phi = np.deg2rad(phi_deg)

# --- Complex Number Math ---
j = 1j
V_mag = 1.5
I_mag = 1.0

# STAR (Y) Calculations (Reference: Van = 0°)
Van = V_mag * np.exp(j * 0)
Vbn = V_mag * np.exp(-j * np.deg2rad(120))
Vcn = V_mag * np.exp(j * np.deg2rad(120))

# Star Line Voltages
Vab_star = Van - Vbn
Vbc_star = Vbn - Vcn
Vca_star = Vcn - Van

# Star Currents
Ia_star = I_mag * np.exp(-j * phi)
Ib_star = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ic_star = I_mag * np.exp(j * (np.deg2rad(120) - phi))

# DELTA (Δ) Calculations (Reference: Vab = 0°)
Vab_delta = V_mag * 1.732 * np.exp(j * 0) 
Vbc_delta = V_mag * 1.732 * np.exp(-j * np.deg2rad(120))
Vca_delta = V_mag * 1.732 * np.exp(j * np.deg2rad(120))

# Delta Phase Currents
Iab_delta = I_mag * np.exp(-j * phi)
Ibc_delta = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ica_delta = I_mag * np.exp(j * (np.deg2rad(120) - phi))

# Delta Line Currents
Ia_delta = Iab_delta - Ica_delta
Ib_delta = Ibc_delta - Iab_delta
Ic_delta = Ica_delta - Ibc_delta

# --- Plotting Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

for ax in [ax1, ax2]:
    ax.axis('off')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)

def draw_vector(ax, c_end, color, label, label_offset=(0.1, 0.1), width=1.0, linestyle='-', alpha=1.0):
    x_end, y_end = c_end.real, c_end.imag
    ax.annotate('', xy=(x_end, y_end), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color, width=width, headwidth=width*6, shrinkA=0, shrinkB=0, linestyle=linestyle, alpha=alpha))
    ax.plot([], [], color=color, label=label, linewidth=width+1, linestyle=linestyle, alpha=alpha)
    ax.text(x_end + label_offset[0], y_end + label_offset[1], label, fontsize=12, color=color, fontweight='bold', alpha=alpha,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

def draw_parallelogram(ax, c1, c2, color='gray'):
    # Draws the two missing sides of the parallelogram
    ax.plot([c1.real, c1.real + c2.real], [c1.imag, c1.imag + c2.imag], color=color, linestyle='--', alpha=0.5, linewidth=1.5)
    ax.plot([c2.real, c1.real + c2.real], [c2.imag, c1.imag + c2.imag], color=color, linestyle='--', alpha=0.5, linewidth=1.5)

# --- Plot 1: STAR (Y) System ---
ax1.set_title("Star (Y) Connection\nLine Voltage shifts 30° | Currents remain equal", fontsize=14, pad=20)

# 1. Draw inverse phase voltages (faintly) for the parallelogram
draw_vector(ax1, -Vbn, 'dodgerblue', r'$-V_{bn}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax1, -Vcn, 'dodgerblue', r'$-V_{cn}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax1, -Van, 'dodgerblue', r'$-V_{an}$', width=0.8, linestyle=':', alpha=0.6)

# 2. Draw standard phase voltages
draw_vector(ax1, Van, 'dodgerblue', r'$V_{an}$')
draw_vector(ax1, Vbn, 'dodgerblue', r'$V_{bn}$')
draw_vector(ax1, Vcn, 'dodgerblue', r'$V_{cn}$')

# 3. Draw full parallelograms for voltages
draw_parallelogram(ax1, Van, -Vbn, 'blue')
draw_parallelogram(ax1, Vbn, -Vcn, 'blue')
draw_parallelogram(ax1, Vcn, -Van, 'blue')

# 4. Draw resultant line voltages
draw_vector(ax1, Vab_star, 'blue', r'$V_{ab}$', width=1.5)
draw_vector(ax1, Vbc_star, 'blue', r'$V_{bc}$', width=1.5)
draw_vector(ax1, Vca_star, 'blue', r'$V_{ca}$', width=1.5)

# 5. Draw currents
draw_vector(ax1, Ia_star, 'crimson', r'$I_a = I_{an}$', width=1.5)
draw_vector(ax1, Ib_star, 'crimson', r'$I_b = I_{bn}$', width=1.5)
draw_vector(ax1, Ic_star, 'crimson', r'$I_c = I_{cn}$', width=1.5)

# --- Plot 2: DELTA (Δ) System ---
ax2.set_title("Delta (Δ) Connection\nLine Current shifts -30° | Voltages remain equal", fontsize=14, pad=20)

# 1. Draw standard voltages
draw_vector(ax2, Vab_delta, 'blue', r'$V_{ab}$', width=1.5)
draw_vector(ax2, Vbc_delta, 'blue', r'$V_{bc}$', width=1.5)
draw_vector(ax2, Vca_delta, 'blue', r'$V_{ca}$', width=1.5)

# 2. Draw inverse phase currents (faintly) for the parallelogram
draw_vector(ax2, -Ica_delta, 'darkorange', r'$-I_{ca}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax2, -Iab_delta, 'darkorange', r'$-I_{ab}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax2, -Ibc_delta, 'darkorange', r'$-I_{bc}$', width=0.8, linestyle=':', alpha=0.6)

# 3. Draw standard phase currents
draw_vector(ax2, Iab_delta, 'darkorange', r'$I_{ab}$')
draw_vector(ax2, Ibc_delta, 'darkorange', r'$I_{bc}$')
draw_vector(ax2, Ica_delta, 'darkorange', r'$I_{ca}$')

# 4. Draw full parallelograms for currents
draw_parallelogram(ax2, Iab_delta, -Ica_delta, 'crimson')
draw_parallelogram(ax2, Ibc_delta, -Iab_delta, 'crimson')
draw_parallelogram(ax2, Ica_delta, -Ibc_delta, 'crimson')

# 5. Draw resultant line currents
draw_vector(ax2, Ia_delta, 'crimson', r'$I_a$', width=1.5)
draw_vector(ax2, Ib_delta, 'crimson', r'$I_b$', width=1.5)
draw_vector(ax2, Ic_delta, 'crimson', r'$I_c$', width=1.5)

st.pyplot(fig)

st.markdown("""
### Core Observations
* **Star System (Left):** The Phase Voltages (light blue) form the inner star. The Line Voltages (dark blue) form the outer star, scaled by $\sqrt{3}$ and rotated exactly $30^\circ$ counter-clockwise. The currents strictly follow the phase voltages.
* **Delta System (Right):** The Voltages (dark blue) serve as the rigid reference. The Phase Currents (orange) lag behind them based on the slider. The Line Currents (red) are the vector subtraction of the phase currents, making them $\sqrt{3}$ larger and shifting them exactly $30^\circ$ clockwise relative to the phase currents.
""")
