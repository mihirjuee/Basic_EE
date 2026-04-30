# ==========================================================
# 3D VISUALIZATION: TWO PARALLEL CURRENT-CARRYING CONDUCTORS
# Shows:
# ✅ Two long parallel conductors
# ✅ Current direction (same/opposite)
# ✅ Attraction / Repulsion
# ✅ 3D magnetic field circles
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

# ---------------- 3D FIGURE ----------------
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Wire positions
x1, y1 = -d/2, 0
x2, y2 = d/2, 0

# Length of wires
z = np.linspace(-5, 5, 100)

# Draw wires
ax.plot([x1]*len(z), [y1]*len(z), z, linewidth=4, label="Conductor 1")
ax.plot([x2]*len(z), [y2]*len(z), z, linewidth=4, label="Conductor 2")

# Current arrows
if direction == "Same Direction":
    ax.quiver(x1, y1, -4, 0, 0, 3, arrow_length_ratio=0.2)
    ax.quiver(x2, y2, -4, 0, 0, 3, arrow_length_ratio=0.2)
else:
    ax.quiver(x1, y1, -4, 0, 0, 3, arrow_length_ratio=0.2)
    ax.quiver(x2, y2, 4, 0, 0, -3, arrow_length_ratio=0.2)

# ---------------- MAGNETIC FIELD LOOPS ----------------
theta = np.linspace(0, 2*np.pi, 100)

for zpos in [-3, 0, 3]:
    r = 0.5
    
    # Around conductor 1
    x_circle1 = x1 + r*np.cos(theta)
    y_circle1 = y1 + r*np.sin(theta)
    z_circle1 = np.ones_like(theta) * zpos
    ax.plot(x_circle1, y_circle1, z_circle1, linestyle='dashed')
    
    # Around conductor 2
    x_circle2 = x2 + r*np.cos(theta)
    y_circle2 = y2 + r*np.sin(theta)
    z_circle2 = np.ones_like(theta) * zpos
    ax.plot(x_circle2, y_circle2, z_circle2, linestyle='dashed')

# ---------------- FORCE ARROWS ----------------
if interaction == "Attraction":
    ax.quiver(x1, 1.2, 0, 1, 0, 0, arrow_length_ratio=0.2)
    ax.quiver(x2, 1.2, 0, -1, 0, 0, arrow_length_ratio=0.2)
else:
    ax.quiver(x1, 1.2, 0, -1, 0, 0, arrow_length_ratio=0.2)
    ax.quiver(x2, 1.2, 0, 1, 0, 0, arrow_length_ratio=0.2)

# Labels
ax.text(x1, 0, 5.5, f"I₁={I1}A")
ax.text(x2, 0, 5.5, f"I₂={I2}A")

# ---------------- STYLE ----------------
ax.set_title(f"{interaction} between Conductors")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Length of Conductors")

ax.set_xlim(-4, 4)
ax.set_ylim(-3, 3)
ax.set_zlim(-5, 5)

st.pyplot(fig)

# ---------------- THEORY ----------------
mu0 = 4 * np.pi * 1e-7
F_per_length = (mu0 * I1 * I2) / (2 * np.pi * d)

st.subheader("📘 Results")
st.write(f"### Interaction: **{interaction}**")
st.write(f"### Force per unit length: **{F_per_length:.6e} N/m**")

st.latex(r"\frac{F}{L}=\frac{\mu_0 I_1 I_2}{2\pi d}")

st.info("Same Direction → Attraction | Opposite Direction → Repulsion")
