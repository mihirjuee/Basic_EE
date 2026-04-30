# ==========================================================
# CLEAN 3D VISUALIZATION: TWO PARALLEL CURRENT-CARRYING CONDUCTORS
# IMPROVED:
# ✅ Arrowheads embedded INTO dotted circular flux path
# ✅ No separate clumsy arrows
# ✅ Smooth directional magnetic field loops
# ==========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Clean 3D Parallel Conductors", layout="wide")

st.title("⚡ Clean 3D Diagram: Two Parallel Current-Carrying Conductors")

# ---------------- INPUTS ----------------
st.sidebar.header("Input Parameters")

I1 = st.sidebar.slider("Current in Conductor 1 (A)", 1.0, 100.0, 10.0)
I2 = st.sidebar.slider("Current in Conductor 2 (A)", 1.0, 100.0, 10.0)
d = st.sidebar.slider("Distance Between Conductors (m)", 0.5, 5.0, 2.0)

direction = st.sidebar.radio(
    "Current Direction",
    ["Same Direction", "Opposite Direction"]
)

interaction = "Attraction" if direction == "Same Direction" else "Repulsion"

# ---------------- FIGURE ----------------
fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(111, projection='3d')

# Wire positions
x1, y1 = -d/2, 0
x2, y2 = d/2, 0

# Wire length
z = np.linspace(-5, 5, 100)

# Draw conductors
ax.plot([x1]*len(z), [y1]*len(z), z, linewidth=5)
ax.plot([x2]*len(z), [y2]*len(z), z, linewidth=5)

# Current direction
if direction == "Same Direction":
    dir1, dir2 = 1, 1
else:
    dir1, dir2 = 1, -1

# Current arrows
ax.quiver(x1, y1, -4, 0, 0, 3*dir1, arrow_length_ratio=0.25, linewidth=2)
ax.quiver(x2, y2, -4 if dir2 == 1 else 4, 0, 0, 3*dir2, arrow_length_ratio=0.25, linewidth=2)

# ---------------- FUNCTION TO DRAW CLEAN FLUX LOOPS ----------------
def draw_flux_loops(xc, yc, current_dir):
    theta = np.linspace(0, 2*np.pi, 400)

    # Right-hand rule
    theta_plot = theta if current_dir == 1 else -theta

    for zpos in [-3, 0, 3]:
        r = 0.75

        x_circle = xc + r * np.cos(theta_plot)
        y_circle = yc + r * np.sin(theta_plot)
        z_circle = np.ones_like(theta_plot) * zpos

        # Main dotted loop
        ax.plot(
            x_circle,
            y_circle,
            z_circle,
            linestyle='dashed',
            linewidth=2
        )

        # Embedded arrowhead by replacing small section with thick arrow-like segment
        arrow_idx = 80

        # Short directional segment
        ax.plot(
            x_circle[arrow_idx:arrow_idx+8],
            y_circle[arrow_idx:arrow_idx+8],
            z_circle[arrow_idx:arrow_idx+8],
            linewidth=4
        )

        # Arrowhead wings
        px = x_circle[arrow_idx+7]
        py = y_circle[arrow_idx+7]
        pz = z_circle[arrow_idx+7]

        dx = x_circle[arrow_idx+7] - x_circle[arrow_idx+4]
        dy = y_circle[arrow_idx+7] - y_circle[arrow_idx+4]

        mag = np.sqrt(dx**2 + dy**2)
        dx /= mag
        dy /= mag

        # Perpendicular vectors for arrowhead
        wing = 0.12

        left_x = px - 0.25*dx + wing*dy
        left_y = py - 0.25*dy - wing*dx

        right_x = px - 0.25*dx - wing*dy
        right_y = py - 0.25*dy + wing*dx

        ax.plot([left_x, px], [left_y, py], [pz, pz], linewidth=3)
        ax.plot([right_x, px], [right_y, py], [pz, pz], linewidth=3)

# Draw magnetic fields
draw_flux_loops(x1, y1, dir1)
draw_flux_loops(x2, y2, dir2)

# ---------------- FORCE ARROWS ----------------
if interaction == "Attraction":
    ax.quiver(x1, 1.8, 0, 1.2, 0, 0, arrow_length_ratio=0.25, linewidth=3)
    ax.quiver(x2, 1.8, 0, -1.2, 0, 0, arrow_length_ratio=0.25, linewidth=3)
else:
    ax.quiver(x1, 1.8, 0, -1.2, 0, 0, arrow_length_ratio=0.25, linewidth=3)
    ax.quiver(x2, 1.8, 0, 1.2, 0, 0, arrow_length_ratio=0.25, linewidth=3)

# ---------------- LABELS ----------------
ax.text(x1, 0, 5.7, f"I₁ = {I1} A", fontsize=12)
ax.text(x2, 0, 5.7, f"I₂ = {I2} A", fontsize=12)

# ---------------- STYLING ----------------
ax.set_title(f"{interaction} Between Conductors with Embedded Flux Direction", pad=20)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Length")

ax.set_xlim(-4, 4)
ax.set_ylim(-3, 3)
ax.set_zlim(-5, 5)

# Cleaner perspective
ax.view_init(elev=25, azim=45)

st.pyplot(fig)

# ---------------- CALCULATIONS ----------------
mu0 = 4 * np.pi * 1e-7
F_per_length = (mu0 * I1 * I2) / (2 * np.pi * d)

st.subheader("📘 Results")
st.write(f"### Interaction: **{interaction}**")
st.write(f"### Force per unit length: **{F_per_length:.6e} N/m**")

st.latex(r"\frac{F}{L}=\frac{\mu_0 I_1 I_2}{2\pi d}")

st.success("Arrowheads are now integrated into the dotted flux path for a cleaner diagram.")
