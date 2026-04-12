import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="narrow")
st.title("Balanced 3-Phase Phasor Diagrams: Star vs. Delta")
st.markdown("Compare the Voltage and Current relationships under a balanced load (R-Y-B Sequence).")

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

Vab_star = Van - Vbn
Vbc_star = Vbn - Vcn
Vca_star = Vcn - Van

Ia_star = I_mag * np.exp(-j * phi)
Ib_star = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ic_star = I_mag * np.exp(j * (np.deg2rad(120) - phi))

# DELTA (Δ) Calculations (Reference: Vab = 0°)
Vab_delta = V_mag * 1.732 * np.exp(j * 0) 
Vbc_delta = V_mag * 1.732 * np.exp(-j * np.deg2rad(120))
Vca_delta = V_mag * 1.732 * np.exp(j * np.deg2rad(120))

Iab_delta = I_mag * np.exp(-j * phi)
Ibc_delta = I_mag * np.exp(-j * (np.deg2rad(120) + phi))
Ica_delta = I_mag * np.exp(j * (np.deg2rad(120) - phi))

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

def draw_parallelogram(ax, c1, c2, color):
    ax.plot([c1.real, c1.real + c2.real], [c1.imag, c1.imag + c2.imag], color=color, linestyle='--', alpha=0.5, linewidth=1.5)
    ax.plot([c2.real, c1.real + c2.real], [c2.imag, c1.imag + c2.imag], color=color, linestyle='--', alpha=0.5, linewidth=1.5)

def draw_angle_arc(ax, c_ref, c_target, radius, color, label, center=0j):
    ang1 = np.angle(c_ref)
    ang2 = np.angle(c_target)
    
    ang1 = ang1 % (2 * np.pi)
    ang2 = ang2 % (2 * np.pi)
    if abs(ang1 - ang2) > np.pi:
        if ang1 > ang2:
            ang2 += 2 * np.pi
        else:
            ang1 += 2 * np.pi
            
    start_ang = min(ang1, ang2)
    end_ang = max(ang1, ang2)
    
    theta = np.linspace(start_ang, end_ang, 50)
    x = center.real + radius * np.cos(theta)
    y = center.imag + radius * np.sin(theta)
    ax.plot(x, y, color=color, linestyle=':', linewidth=1.5)
    
    mid_ang = (start_ang + end_ang) / 2
    lx = center.real + (radius + 0.3) * np.cos(mid_ang)
    ly = center.imag + (radius + 0.3) * np.sin(mid_ang)
    
    ax.text(lx, ly, label, color=color, fontsize=11, fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# --- Standard R-Y-B Color Palette ---
c_A = '#E63946' # Red
c_B = '#D4AC0D' # Golden Yellow
c_C = '#1D3557' # Blue
c_V = 'blue'    # Standard Voltage Blue

# --- Plot 1: STAR (Y) System ---
ax1.set_title("Star (Y) Connection\nLine Voltage shifts 30° | Currents remain equal", fontsize=14, pad=20)

draw_vector(ax1, -Vbn, c_B, r'$-V_{bn}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax1, -Vcn, c_C, r'$-V_{cn}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax1, -Van, c_A, r'$-V_{an}$', width=0.8, linestyle=':', alpha=0.6)

draw_vector(ax1, Van, c_A, r'$V_{an}$')
draw_vector(ax1, Vbn, c_B, r'$V_{bn}$')
draw_vector(ax1, Vcn, c_C, r'$V_{cn}$')

draw_parallelogram(ax1, Van, -Vbn, c_A)
draw_parallelogram(ax1, Vbn, -Vcn, c_B)
draw_parallelogram(ax1, Vcn, -Van, c_C)

draw_vector(ax1, Vab_star, c_A, r'$V_{ab}$', width=1.5)
draw_vector(ax1, Vbc_star, c_B, r'$V_{bc}$', width=1.5)
draw_vector(ax1, Vca_star, c_C, r'$V_{ca}$', width=1.5)

draw_vector(ax1, Ia_star, c_A, r'$I_a = I_{an}$', width=1.5)
draw_vector(ax1, Ib_star, c_B, r'$I_b = I_{bn}$', width=1.5)
draw_vector(ax1, Ic_star, c_C, r'$I_c = I_{cn}$', width=1.5)

# Add Angle Arcs for Star (Using Phase A as the example)
draw_angle_arc(ax1, Van, Vab_star, 0.6, c_V, r'$30^\circ$')
draw_angle_arc(ax1, Van, Ia_star, 0.9, c_A, r'$\Phi$')

# --- Plot 2: DELTA (Δ) System ---
ax2.set_title("Delta (Δ) Connection\nLine Current shifts -30° | Voltages remain equal", fontsize=14, pad=20)

draw_vector(ax2, Vab_delta, c_A, r'$V_{ab}$', width=1.5)
draw_vector(ax2, Vbc_delta, c_B, r'$V_{bc}$', width=1.5)
draw_vector(ax2, Vca_delta, c_C, r'$V_{ca}$', width=1.5)

draw_vector(ax2, -Ica_delta, c_C, r'$-I_{ca}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax2, -Iab_delta, c_A, r'$-I_{ab}$', width=0.8, linestyle=':', alpha=0.6)
draw_vector(ax2, -Ibc_delta, c_B, r'$-I_{bc}$', width=0.8, linestyle=':', alpha=0.6)

draw_vector(ax2, Iab_delta, c_A, r'$I_{ab}$')
draw_vector(ax2, Ibc_delta, c_B, r'$I_{bc}$')
draw_vector(ax2, Ica_delta, c_C, r'$I_{ca}$')

draw_parallelogram(ax2, Iab_delta, -Ica_delta, c_A)
draw_parallelogram(ax2, Ibc_delta, -Iab_delta, c_B)
draw_parallelogram(ax2, Ica_delta, -Ibc_delta, c_C)

draw_vector(ax2, Ia_delta, c_A, r'$I_a$', width=1.5)
draw_vector(ax2, Ib_delta, c_B, r'$I_b$', width=1.5)
draw_vector(ax2, Ic_delta, c_C, r'$I_c$', width=1.5)

# Add Angle Arcs for Delta (Using Phase A as the example)
draw_angle_arc(ax2, Vab_delta, Iab_delta, 0.6, c_V, r'$\Phi$')
draw_angle_arc(ax2, Iab_delta, Ia_delta, 1.2, c_A, r'$30^\circ$')

st.pyplot(fig)

st.markdown("""
### Phase Color Key & Angles
* **<span style="color:#E63946">Phase A</span>:** Red Vectors 
* **<span style="color:#D4AC0D">Phase B</span>:** Yellow Vectors 
* **<span style="color:#1D3557">Phase C</span>:** Blue Vectors
* Notice how the 30° shift applies to the voltage in the Star system, but applies to the current in the Delta system!
""", unsafe_allow_html=True)
