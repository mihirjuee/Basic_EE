import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Transformer Phasor Diagram: Step-by-Step")
st.markdown("Constructing the practical transformer phasor diagram with a lagging load.")

# The slider drives the state machine
step = st.slider("Select Construction Step", 1, 7, 1)

# --- Explanatory Text for Each Step ---
step_texts = {
    1: "**Step 1: The Mutual Flux.** We begin with the core flux (Φ) as our horizontal reference at 0°.",
    2: "**Step 2: Induced EMFs.** Faraday's Law dictates that induced voltages (E₁ and E₂) lag the flux that created them by 90°.",
    3: "**Step 3: No-Load Current.** Even unloaded, the primary draws current (I₀) to magnetize the core (Iₘ) and supply core losses (I꜀).",
    4: "**Step 4: Secondary Load Current.** A lagging (inductive) load is connected. The secondary current (I₂) lags behind the secondary voltage (E₂).",
    5: "**Step 5: Load Balancing Current.** To counteract the demagnetizing effect of I₂, the primary instantly draws a balancing current (I₁') exactly 180° opposite to I₂.",
    6: "**Step 6: Total Primary Current.** The total current drawn from the supply (I₁) is the vector sum of the no-load current (I₀) and the balancing current (I₁').",
    7: "**Step 7: Terminal Voltages.** We add the voltage drops (IR and IX). The supply voltage (V₁) must overcome the opposing EMF (-E₁) plus primary drops. The terminal voltage (V₂) is E₂ minus secondary drops."
}

st.info(step_texts[step])

# --- Plotting Setup ---
fig, ax = plt.subplots(figsize=(10, 10))

# Center the axes
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xticks([]) # Hide tick marks for a cleaner look
ax.set_yticks([])

# Helper function to draw crisp arrows
def draw_vector(x, y, color, label, label_offset=(0.1, 0.1), width=2):
    ax.annotate('', xy=(x, y), xytext=(0, 0),
                arrowprops=dict(facecolor=color, edgecolor=color, width=width, headwidth=10, shrinkA=0, shrinkB=0))
    # Draw invisible line for the legend
    ax.plot([], [], color=color, label=label, linewidth=width+1)
    # Put text label near the tip
    ax.text(x + label_offset[0], y + label_offset[1], label, fontsize=14, color=color, fontweight='bold')

# Helper function to draw dashed lines for vector addition
def draw_parallelogram(x1, y1, x2, y2, color='gray'):
    ax.plot([x1, x1+x2], [y1, y1+y2], color=color, linestyle='--', alpha=0.7)
    ax.plot([x2, x1+x2], [y2, y1+y2], color=color, linestyle='--', alpha=0.7)

# --- Vector Coordinates (Illustrative for clear teaching) ---
phi_x, phi_y = 1.5, 0
e1_x, e1_y = 0, -1.5
e2_x, e2_y = 0, -1.0
im_x, im_y = 0.4, 0
ic_x, ic_y = 0, 0.3
i0_x, i0_y = im_x + ic_x, im_y + ic_y
i2_x, i2_y = -0.5, -0.86 # Lagging E2
i1p_x, i1p_y = -i2_x, -i2_y # 180 degrees from I2
i1_x, i1_y = i0_x + i1p_x, i0_y + i1p_y
neg_e1_x, neg_e1_y = -e1_x, -e1_y
v1_x, v1_y = 0.3, 1.7 # Offset from -E1
v2_x, v2_y = 0.1, -0.8 # Offset from E2

# --- Draw vectors based on the selected step ---
if step >= 1:
    draw_vector(phi_x, phi_y, 'black', r'$\Phi$', (0.05, 0.05))

if step >= 2:
    draw_vector(e1_x, e1_y, 'dodgerblue', r'$E_1$', (0.05, -0.1))
    draw_vector(e2_x, e2_y, 'dodgerblue', r'$E_2$', (0.05, -0.1))

if step >= 3:
    draw_vector(im_x, im_y, 'gray', r'$I_m$', (0, -0.15))
    draw_vector(ic_x, ic_y, 'gray', r'$I_c$', (-0.2, 0))
    draw_parallelogram(im_x, im_y, ic_x, ic_y)
    draw_vector(i0_x, i0_y, 'purple', r'$I_0$', (0.05, 0.05))

if step >= 4:
    draw_vector(i2_x, i2_y, 'crimson', r'$I_2$', (-0.1, -0.15))

if step >= 5:
    draw_vector(i1p_x, i1p_y, 'crimson', r'$I_1^\prime$', (0.05, 0.05))
    # Draw dashed line connecting I2 and I1' to prove 180 degrees
    ax.plot([i2_x, i1p_x], [i2_y, i1p_y], color='crimson', linestyle=':', alpha=0.5)

if step >= 6:
    draw_parallelogram(i0_x, i0_y, i1p_x, i1p_y)
    draw_vector(i1_x, i1_y, 'red', r'$I_1$', (0.05, 0.05), width=3)

if step >= 7:
    draw_vector(neg_e1_x, neg_e1_y, 'dodgerblue', r'$-E_1$', (-0.2, 0.05))
    draw_vector(v1_x, v1_y, 'forestgreen', r'$V_1$', (0.05, 0.05), width=3)
    draw_vector(v2_x, v2_y, 'forestgreen', r'$V_2$', (0.05, -0.1), width=3)
    # Draw simplified voltage drop lines
    ax.plot([neg_e1_x, v1_x], [neg_e1_y, v1_y], color='gray', linestyle='--')
    ax.plot([e2_x, v2_x], [e2_y, v2_y], color='gray', linestyle='--')

ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
st.pyplot(fig)
