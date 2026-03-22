import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Balanced 3-Phase Phasor Diagrams: Star vs. Delta")
st.markdown("Compare the Voltage and Current relationships under a balanced load.")

# --- Interactive Control ---
# Slider to adjust the load power factor angle (positive = lagging, negative = leading)
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

# Star Line Voltages (V_L leads V_ph by 30°, mag * sqrt(3))
Vab_star = Van - Vbn
Vbc_star = Vbn - Vcn
Vca_star = Vcn - Van

# Star Currents (I_L = I_ph, lags V_ph by phi)
Ia_star = I_mag * np.exp(-j * phi)
Ib_star = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ic_star = I_mag * np.exp(j * (np.deg2rad(120) - phi))


# DELTA (Δ) Calculations (Reference: Vab = 0°)
Vab_delta = V_mag * 1.732 * np.exp(j * 0) # Scaled up slightly for visual comparison
Vbc_delta = V_mag * 1.732 * np.exp(-j * np.deg2rad(120))
Vca_delta = V_mag * 1.732 * np.exp(j * np.deg2rad(120))

# Delta Phase Currents (lags phase voltage by phi)
Iab_delta = I_mag * np.exp(-j * phi)
Ibc_delta = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ica_delta = I_mag * np.exp(j * (np.deg2rad(120) - phi))

# Delta Line Currents (I_L lags I_ph by 30°, mag * sqrt(3))
Ia_delta = Iab_delta - Ica_delta
Ib_delta = Ibc_delta - Iab_delta
Ic_delta = Ica_delta - Ibc_delta


# --- Plotting Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

for ax in [ax1, ax2]:
    ax.axis('off')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)

def draw_vector(ax, c_end, color, label, label_offset=(0.1, 0.1), width=1.0, linestyle='-'):
    x_end, y_end = c_end.real, c_end.imag
    ax.annotate('', xy=(x_end, y_end), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color, width=width, headwidth=width*6, shrinkA=0, shrinkB=0, linestyle=linestyle))
    ax.plot([], [], color=color, label=label, linewidth=width+1, linestyle=linestyle)
    ax.text(x_end + label_offset[0], y_end + label_offset[1], label, fontsize=12, color=color, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

def draw_dashed_link(ax, c_start, c_end, color):
    ax.plot([c_start.real, c_end.real], [c_start.imag, c_end.imag], color=color, linestyle=':', alpha=0.5)

# --- Plot 1: STAR (Y) System ---
ax1.set_title("Star (Y) Connection\nLine Voltage shifts 30° | Currents remain equal", fontsize=14, pad=20)

# Phase Voltages
draw_vector(ax1, Van, 'dodgerblue', r'$V_{an}$')
draw_vector(ax1, Vbn, 'dodgerblue', r'$V_{bn}$')
draw_vector(ax1, Vcn, 'dodgerblue', r'$V_{cn}$')

# Line Voltages
draw_vector(ax1, Vab_star, 'blue', r'$V_{ab}$', width=1.5)
draw_vector(ax1, Vbc_star, 'blue', r'$V_{bc}$', width=1.5)
draw_vector(ax1, Vca_star, 'blue', r'$V_{ca}$', width=1.5)

# Currents (Line = Phase)
draw_vector(ax1, Ia_star, 'crimson', r'$I_a = I_{an}$', width=1.5)
draw_vector(ax1, Ib_star, 'crimson', r'$I_b = I_{bn}$', width=1.5)
draw_vector(ax1, Ic_star, 'crimson', r'$I_c = I_{cn}$', width=1.5)

# Subtraction links for visual proof
draw_dashed_link(ax1, Van, Vab_star, 'blue')
draw_dashed_link(ax1, -Vbn, Vab_star, 'blue')


# --- Plot 2: DELTA (Δ) System ---
ax2.set_title("Delta (Δ) Connection\nLine Current shifts -30° | Voltages remain equal", fontsize=14, pad=20)

# Voltages (Line = Phase)
draw_vector(ax2, Vab_delta, 'blue', r'$V_{ab}$', width=1.5)
draw_vector(ax2, Vbc_delta, 'blue', r'$V_{bc}$', width=1.5)
draw_vector(ax2, Vca_delta, 'blue', r'$V_{ca}$', width=1.5)

# Phase Currents
draw_vector(ax2, Iab_delta, 'darkorange', r'$I_{ab}$')
draw_vector(ax2, Ibc_delta, 'darkorange', r'$I_{bc}$')
draw_vector(ax2, Ica_delta, 'darkorange', r'$I_{ca}$')

# Line Currents
draw_vector(ax2, Ia_delta, 'crimson', r'$I_a$', width=1.5)
draw_vector(ax2, Ib_delta, 'crimson', r'$I_b$', width=1.5)
draw_vector(ax2, Ic_delta, 'crimson', r'$I_c$', width=1.5)

# Subtraction links for visual proof (Ia = Iab - Ica)
draw_dashed_link(ax2, Iab_delta, Ia_delta, 'crimson')
draw_dashed_link(ax2, -Ica_delta, Ia_delta, 'crimson')

st.pyplot(fig)

st.markdown("""
### Core Observations
* **Star System (Left):** The Phase Voltages (light blue) form the inner star. The Line Voltages (dark blue) form the outer star, scaled by $\sqrt{3}$ and rotated exactly $30^\circ$ counter-clockwise. The currents strictly follow the phase voltages.
* **Delta System (Right):** The Voltages (dark blue) serve as the rigid reference. The Phase Currents (orange) lag behind them based on the slider. The Line Currents (red) are the vector subtraction of the phase currents, making them $\sqrt{3}$ larger and shifting them exactly $30^\circ$ clockwise relative to the phase currents.
""")
