import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Transformer Phasor Diagram: V₂ Reference")
st.markdown("Constructing the diagram with the secondary terminal voltage as the horizontal reference.")

step = st.slider("Select Construction Step", 1, 8, 1)

step_texts = {
    1: "**Step 1: The Reference.** We define the secondary terminal voltage ($V_2$) as our perfectly horizontal reference at 0°.",
    2: "**Step 2: Secondary Current.** For a lagging inductive load, the current ($I_2$) lags behind the voltage by the load angle $\phi_2$.",
    3: "**Step 3: Secondary Drops & EMF.** $E_2 = V_2 + I_2R_2 + I_2X_2$. The resistive drop is parallel to $I_2$, and the reactive drop is perpendicular.",
    4: "**Step 4: Mutual Flux.** Induced EMF lags the core flux by 90°. Therefore, we draw the mutual flux ($\Phi$) 90° ahead of $E_2$. We also draw primary $E_1$.",
    5: "**Step 5: Balancing Current.** The primary balancing current ($I_2^\prime$) is drawn exactly 180° opposite to $I_2$.",
    6: "**Step 6: No-Load & Total Current.** $I_0$ is built around $\Phi$. The total primary current is $I_1 = I_2^\prime + I_0$.",
    7: "**Step 7: Primary EMF.** We map $-E_1$, which is exactly 180° opposite to the induced EMF $E_1$.",
    8: "**Step 8: Primary Voltage Drops.** The supply voltage $V_1 = (-E_1) + I_1R_1 + I_1X_1$. The angle between $V_1$ and $I_1$ is the primary power factor angle $\phi_1$."
}

st.info(step_texts[step])

fig, ax = plt.subplots(figsize=(10, 10))
ax.axis('off')
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)

# --- Helper Functions ---
def draw_vector(c_end, color, label, label_offset=(0.1, 0.1), width=1.0, c_start=0j):
    x_start, y_start = c_start.real, c_start.imag
    x_end, y_end = c_end.real, c_end.imag
    
    ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(facecolor=color, edgecolor=color, width=width, headwidth=width*6, shrinkA=0, shrinkB=0))
    ax.plot([], [], color=color, label=label, linewidth=width+1)
    ax.text(x_end + label_offset[0], y_end + label_offset[1], label, fontsize=13, color=color, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1.5))

def draw_parallelogram(c1, c2, color='gray', c_start=0j):
    x_start, y_start = c_start.real, c_start.imag
    ax.plot([x_start + c1.real, x_start + c1.real + c2.real], 
            [y_start + c1.imag, y_start + c1.imag + c2.imag], color=color, linestyle='--', alpha=0.5, linewidth=1)
    ax.plot([x_start + c2.real, x_start + c1.real + c2.real], 
            [y_start + c2.imag, y_start + c1.imag + c2.imag], color=color, linestyle='--', alpha=0.5, linewidth=1)

def draw_angle_arc(c_ref, c_target, radius, color, label, center=0j):
    ang1 = np.angle(c_ref)
    ang2 = np.angle(c_target)
    
    # Normalize angles to trace the shortest path
    ang1 = ang1 % (2 * np.pi)
    ang2 = ang2 % (2 * np.pi)
    if abs(ang1 - ang2) > np.pi:
        if ang1 > ang2:
            ang2 += 2 * np.pi
        else:
            ang1 += 2 * np.pi
            
    start_ang = min(ang1, ang2)
    end_ang = max(ang1, ang2)
    
    # Draw the curved dotted line
    theta = np.linspace(start_ang, end_ang, 50)
    x = center.real + radius * np.cos(theta)
    y = center.imag + radius * np.sin(theta)
    ax.plot(x, y, color=color, linestyle=':', linewidth=1.5)
    
    # Place the label precisely in the middle of the arc
    mid_ang = (start_ang + end_ang) / 2
    lx = center.real + (radius + 0.25) * np.cos(mid_ang)
    ly = center.imag + (radius + 0.25) * np.sin(mid_ang)
    
    ax.text(lx, ly, label, color=color, fontsize=13, fontweight='bold', ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

# --- Complex Number Vector Math ---
j = 1j

V2 = 1.5 + 0j
phi2 = np.deg2rad(30) 
I2 = 1.0 * np.exp(-j * phi2) 

I2r2 = 0.4 * I2             
I2x2 = 0.5 * I2 * np.exp(j * np.deg2rad(90)) 
E2 = V2 + I2r2 + I2x2
E1 = E2 * 1.1 

Phi_dir = E2 / np.abs(E2) * np.exp(j * np.deg2rad(90))
Phi = Phi_dir * 2.0

I2_prime = -I2 *(1/1.1)
Im = Phi_dir * 0.6
Ic = Phi_dir * np.exp(j * np.deg2rad(90)) * 0.4
I0 = Im + Ic
I1 = I2_prime + I0

neg_E1 = -E1
I1r1 = I1 * 0.3
I1x1 = I1 * np.exp(j * np.deg2rad(90)) * 0.4
V1 = neg_E1 + I1r1 + I1x1


# --- Drawing Logic ---
if step >= 1:
    draw_vector(V2, 'forestgreen', r'$V_2$', (0.05, 0.05), width=1.5)

if step >= 2:
    draw_vector(I2, 'crimson', r'$I_2$', (0.05, -0.15), width=1.0)
    draw_angle_arc(V2, I2, 0.7, 'crimson', r'$\phi_2$')

if step >= 3:
    draw_vector(V2 + I2r2, 'darkorange', r'$I_2r_2$', (0.05, -0.15), width=0.8, c_start=V2)
    draw_vector(E2, 'darkorange', r'$I_2x_2$', (0.05, 0.05), width=0.8, c_start=V2+I2R2)
    draw_vector(E2, 'dodgerblue', r'$E_2$', (-0.2, 0.05), width=1.0)

if step >= 4:
    draw_vector(Phi, 'black', r'$\Phi$', (0.05, 0.05), width=1.0)
    draw_vector(E1, 'dodgerblue', r'$E_1$', (-0.2, 0.05), width=1.0) 
    draw_angle_arc(E2, Phi, 0.4, 'black', r'$90^\circ$')

if step >= 5:
    draw_vector(I2_prime, 'crimson', r'$I_2^\prime$', (-0.2, 0.05), width=1.0)
    ax.plot([I2.real, I2_prime.real], [I2.imag, I2_prime.imag], color='crimson', linestyle=':', alpha=0.4, linewidth=1)

if step >= 6:
    draw_vector(Im, 'gray', r'$I_m$', (0.05, 0.05), width=0.8)
    draw_vector(Ic, 'gray', r'$I_c$', (-0.2, -0.1), width=0.8)
    draw_parallelogram(Im, Ic)
    draw_vector(I0, 'purple', r'$I_0$', (-0.2, 0.05), width=1.0)
    draw_parallelogram(I2_prime, I0)
    draw_vector(I1, 'red', r'$I_1$', (-0.2, 0.05), width=1.5)

if step >= 7:
    draw_vector(neg_E1, 'dodgerblue', r'$-E_1$', (0.05, -0.15), width=1.0)

if step >= 8:
    draw_vector(neg_E1 + I1r1, 'darkorange', r'$I_1R_1$', (0.05, 0.05), width=0.8, c_start=neg_E1)
    draw_vector(V1, 'darkorange', r'$I_1x_1$', (0.05, 0.05), width=0.8, c_start=neg_E1+I1R1)
    draw_vector(V1, 'forestgreen', r'$V_1$', (0.05, 0.05), width=1.5)
    draw_angle_arc(V1, I1, 1.2, 'forestgreen', r'$\phi_1$')

ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
st.pyplot(fig)
