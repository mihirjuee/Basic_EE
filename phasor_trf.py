import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Transformer Phasor Diagram: Step-by-Step")
st.markdown("Constructing the practical transformer phasor diagram with series voltage drops.")

# The slider drives the state machine (Now 8 steps!)
step = st.slider("Select Construction Step", 1, 8, 1)

# --- Explanatory Text for Each Step ---
step_texts = {
    1: "**Step 1: The Mutual Flux.** We begin with the core flux (Φ) as our horizontal reference.",
    2: "**Step 2: Induced EMFs.** Faraday's Law dictates that induced voltages ($E_1$ and $E_2$) lag the flux that created them by 90°.",
    3: "**Step 3: No-Load Current.** Even unloaded, the primary draws current ($I_0$) to magnetize the core ($I_m$) and supply core losses ($I_c$).",
    4: "**Step 4: Secondary Load Current.** A lagging (inductive) load is connected. The secondary current ($I_2$) lags behind the secondary voltage.",
    5: "**Step 5: Load Balancing Current.** To counteract the demagnetizing effect of $I_2$, the primary instantly draws a balancing current ($I_1'$) exactly 180° opposite to $I_2$.",
    6: "**Step 6: Total Primary Current.** The total current drawn from the supply ($I_1$) is the vector sum of the no-load current ($I_0$) and the balancing current ($I_1'$).",
    7: "**Step 7: Secondary Voltage Drops.** We account for the resistive ($I_2R_2$) and reactive ($I_2X_2$) drops in the secondary winding. The terminal voltage is $V_2 = E_2 - I_2R_2 - I_2X_2$.",
    8: "**Step 8: Primary Voltage Drops.** Finally, we map the supply voltage. It must overcome the opposing induced EMF ($-E_1$) plus the primary winding drops. Therefore, $V_1 = (-E_1) + I_1R_1 + I_1X_1$."
}

st.info(step_texts[step])

# --- Plotting Setup ---
fig, ax = plt.subplots(figsize=(10, 10))

# Completely remove the axes and grid lines for a clean look
ax.axis('off')

# Expanded limits to ensure the series drops fit perfectly on the page
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)

# Helper function to draw crisp arrows from any start point
def draw_vector(x_end, y_end, color, label, label_offset=(0.1, 0.1), width=2, x_start=0, y_start=0):
    ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(facecolor=color, edgecolor=color, width=width, headwidth=9, shrinkA=0, shrinkB=0))
    # Draw invisible line for the legend
    ax.plot([], [], color=color, label=label, linewidth=width+1)
    # Put text label near the tip
    ax.text(x_end + label_offset[0], y_end + label_offset[1], label, fontsize=13, color=color, fontweight='bold')

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
i2_x, i2_y = -0.5, -0.86 
i1p_x, i1p_y = -i2_x, -i2_y 
i1_x, i1_y = i0_x + i1p_x, i0_y + i1p_y
neg_e1_x, neg_e1_y = -e1_x, -e1_y

# -- Calculating the Drop Triangles --
# Primary drops (I1 R1 is parallel to I1, I1 X1 is perpendicular)
i1r1_dx, i1r1_dy = 0.24, 0.32
i1x1_dx, i1x1_dy = -0.40, 0.30
p_drop1_x, p_drop1_y = neg_e1_x + i1r1_dx, neg_e1_y + i1r1_dy
v1_x, v1_y = p_drop1_x + i1x1_dx, p_drop1_y + i1x1_dy

# Secondary drops (I2 R2 is parallel to I2, I2 X2 is perpendicular)
i2r2_dx, i2r2_dy = -0.15, -0.26
i2x2_dx, i2x2_dy = 0.34, -0.20
v2_x, v2_y = e2_x - i2r2_dx - i2x2_dx, e2_y - i2r2_dy - i2x2_dy
s_drop1_x, s_drop1_y = v2_x + i2r2_dx, v2_y + i2r2_dy


# --- Draw vectors based on the selected step ---
if step >= 1:
    draw_vector(phi_x, phi_y, 'black', r'$\Phi$', (0.05, 0.05))

if step >= 2:
    draw_vector(e1_x, e1_y, 'dodgerblue', r'$E_1$', (0.05, -0.1))
    draw_vector(e2_x, e2_y, 'dodgerblue', r'$E_2$', (0.05, -0.2))

if step >= 3:
    draw_vector(im_x, im_y, 'gray', r'$I_m$', (0, -0.15))
    draw_vector(ic_x, ic_y, 'gray', r'$I_c$', (-0.2, 0))
    draw_parallelogram(im_x, im_y, ic_x, ic_y)
    draw_vector(i0_x, i0_y, 'purple', r'$I_0$', (0.05, 0.05))

if step >= 4:
    draw_vector(i2_x, i2_y, 'crimson', r'$I_2$', (-0.1, -0.2))

if step >= 5:
    draw_vector(i1p_x, i1p_y, 'crimson', r'$I_2^\prime$', (0.05, 0.05))
    ax.plot([i2_x, i1p_x], [i2_y, i1p_y], color='crimson', linestyle=':', alpha=0.5)

if step >= 6:
    draw_parallelogram(i0_x, i0_y, i1p_x, i1p_y)
    draw_vector(i1_x, i1_y, 'red', r'$I_1$', (0.05, 0.05), width=3)

if step >= 7:
    # Secondary Side Additions ONLY
    draw_vector(v2_x, v2_y, 'forestgreen', r'$V_2$', (-0.3, 0.05), width=3)
    draw_vector(s_drop1_x, s_drop1_y, 'darkorange', r'$I_2 R_2$', (-0.45, 0.05), width=1.5, x_start=v2_x, y_start=v2_y)
    draw_vector(e2_x, e2_y, 'darkorange', r'$I_2 X_2$', (0.05, 0.05), width=1.5, x_start=s_drop1_x, y_start=s_drop1_y)

if step >= 8:
    # Primary Side Additions ONLY
    draw_vector(neg_e1_x, neg_e1_y, 'dodgerblue', r'$-E_1$', (0.05, -0.1))
    draw_vector(p_drop1_x, p_drop1_y, 'darkorange', r'$I_1 R_1$', (0.05, -0.1), width=1.5, x_start=neg_e1_x, y_start=neg_e1_y)
    draw_vector(v1_x, v1_y, 'darkorange', r'$I_1 X_1$', (-0.2, 0.1), width=1.5, x_start=p_drop1_x, y_start=p_drop1_y)
    draw_vector(v1_x, v1_y, 'forestgreen', r'$V_1$', (-0.3, 0.1), width=3)

# Move legend completely outside the plot area
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
st.pyplot(fig)
