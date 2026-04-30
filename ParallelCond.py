# ==========================================================
# 3D VISUALIZATION: TWO PARALLEL CURRENT-CARRYING CONDUCTORS
# UPDATED:
# ✅ Circular magnetic flux lines now include direction arrows
# ✅ Right-hand rule visualization
# ✅ Same / Opposite current direction
# ==========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="3D Parallel Conductors", layout="wide")

st.title("⚡ 3D Diagram: Two Parallel Current-Carrying Conductors")

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
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Wire positions
x1, y1 = -d/2, 0
x2, y2 = d/2, 0

# Wire length
z = np.linspace(-5, 5, 100)

# Draw wires
ax.plot([x1]*len(z), [y1]*len(z), z, linewidth=4)
ax.plot([x2]*len(z), [y2]*len(z), z, linewidth=4)

# Current arrows
if direction == "Same Direction":
    dir1, dir2 = 1, 1
else:
    dir1, dir2 = 1, -1

ax.quiver(x1, y1, -4, 0, 0, 3*dir1, arrow_length_ratio=0.2)
ax.quiver(x2, y2, -4 if dir2 == 1 else 4, 0, 0, 3*dir2, arrow_length_ratio=0.2)

# ---------------- FUNCTION TO DRAW MAGNETIC FIELD ----------------
def draw_flux_loops(xc, yc, current_dir):
    theta = np.linspace(0, 2*np.pi, 200)

    # Right-hand rule:
    # Up current => CCW viewed from top
    # Down current => CW viewed from top
    if current_dir == 1:
        theta_plot = theta
    else:
        theta_plot = -theta

    for zpos in [-3, 0, 3]:
        r = 0.6

        x_circle = xc + r * np.cos(theta_plot)
        y_circle = yc + r * np.sin(theta_plot)
        z_circle = np.ones_like(theta_plot) * zpos

        # Plot circular field
        ax.plot(x_circle, y_circle, z_circle, linestyle='dashed')

        # Add directional arrows at intervals
        for t in np.linspace(0, len(theta_plot)-2, 8, dtype=int):
            dx = x_circle[t+1] - x_circle[t]
            dy = y_circle[t+1] - y_circle[t]
            dz = 0

            ax.quiver(
                x_circle[t], y_circle[t], z_circle[t],
                dx, dy, dz,
                length=1,
                normalize=True,
                arrow_length_ratio=0.4
            )

# Draw flux for both wires
draw_flux_loops(x1, y1, dir1)
draw_flux_loops(x2, y2, dir2)

# ---------------- FORCE ARROWS ----------------
if interaction == "Attraction":
    ax.quiver(x1, 1.5, 0, 1, 0, 0, arrow_length_ratio=0.2)
    ax.quiver(x2, 1.5, 0, -1, 0, 0, arrow_length_ratio=0.2)
else:
    ax.quiver(x1, 1.5, 0, -1, 0, 0, arrow_length_ratio=0.2)
    ax.quiver(x2, 1.5, 0, 1, 0, 0, arrow_length_ratio=0.2)

# Labels
ax.text(x1, 0, 5.5, f"I₁ = {I1} A")
ax.text(x2, 0, 5.5, f"I₂ = {I2} A")

# ---------------- STYLING ----------------
ax.set_title(f"{interaction} Between Conductors with Magnetic Flux Direction")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Length")

ax.set_xlim(-4, 4)
ax.set_ylim(-3, 3)
ax.set_zlim(-5, 5)

st.pyplot(fig)

# ---------------- CALCULATIONS ----------------
mu0 = 4 * np.pi * 1e-7
F_per_length = (mu0 * I1 * I2) / (2 * np.pi * d)

st.subheader("📘 Results")
st.write(f"### Interaction: **{interaction}**")
st.write(f"### Force per unit length: **{F_per_length:.6e} N/m**")

st.latex(r"\frac{F}{L}=\frac{\mu_0 I_1 I_2}{2\pi d}")

st.info("Flux direction follows Right-Hand Thumb Rule")
