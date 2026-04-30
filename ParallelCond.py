import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="3D Electromagnetism Sim", page_icon="logo.png", layout="wide")

st.title("⚡ Parallel Conductors: Magnetic Flux & Force")
st.markdown("""
This simulation visualizes the magnetic field lines (flux) around two parallel conductors. 
**Right-Hand Rule:** Wrap your right hand around the wire with your thumb in the direction of the current; your fingers curl in the direction of the magnetic field.
""")

# ---------------- INPUTS ----------------
st.sidebar.header("Physical Parameters")

I1 = st.sidebar.slider("Current I₁ (Amperes)", 1.0, 100.0, 20.0)
I2 = st.sidebar.slider("Current I₂ (Amperes)", 1.0, 100.0, 20.0)
d = st.sidebar.slider("Distance 'd' (meters)", 0.5, 5.0, 2.0)

direction = st.sidebar.radio(
    "Current Direction",
    ["Same Direction (Attract)", "Opposite Direction (Repel)"]
)

interaction = "Attraction" if "Same" in direction else "Repulsion"

# ---------------- FIGURE SETUP ----------------
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Wire positions (centered on origin)
x1, y1 = -d/2, 0
x2, y2 = d/2, 0
z_range = np.linspace(-5, 5, 100)

# Draw Conductors (Silver/Grey cylinders)
ax.plot([x1]*100, [y1]*100, z_range, color='gray', linewidth=6, alpha=0.7, label="Conductor 1")
ax.plot([x2]*100, [y2]*100, z_range, color='darkgray', linewidth=6, alpha=0.7, label="Conductor 2")

# Determine directions
dir1 = 1
dir2 = 1 if interaction == "Attraction" else -1

# Main Current Arrows (Vertical)
ax.quiver(x1, y1, -2, 0, 0, 4*dir1, color='black', arrow_length_ratio=0.15, linewidth=3)
ax.quiver(x2, y2, -2*dir2, 0, 0, 4*dir2, color='black', arrow_length_ratio=0.15, linewidth=3)

# ---------------- FUNCTION: EMBEDDED FLUX LOOPS ----------------
def draw_flux_loops(xc, yc, current_dir, color, label_prefix):
    # Create circular path
    theta = np.linspace(0, 2*np.pi, 200)
    
    # Flip rotation based on current direction (Right Hand Rule)
    if current_dir == -1:
        theta = np.flip(theta)

    for i, zpos in enumerate([-3, 0, 3]):
        r = 0.8  # Radius of flux loop
        
        x_c = xc + r * np.cos(theta)
        y_c = yc + r * np.sin(theta)
        z_c = np.ones_like(theta) * zpos

        # 1. Draw the dashed loop
        ax.plot(x_c, y_c, z_c, linestyle='--', color=color, linewidth=1.5, alpha=0.6)

        # 2. Calculate Arrowhead Position (at 90 degrees / index 50)
        idx = 50 
        px, py, pz = x_c[idx], y_c[idx], z_c[idx]
        
        # Tangent vector for arrowhead orientation
        dx = x_c[idx+1] - x_c[idx]
        dy = y_c[idx+1] - y_c[idx]
        
        # Normalize and scale tangent
        mag = np.sqrt(dx**2 + dy**2)
        dx, dy = (dx/mag)*0.3, (dy/mag)*0.3

        # 3. Draw the integrated arrowhead
        ax.quiver(px, py, pz, dx, dy, 0, color=color, pivot='tip', 
                  arrow_length_ratio=0.5, linewidth=2.5)

# Draw Magnetic Fields
draw_flux_loops(x1, y1, dir1, "royalblue", "B1")
draw_flux_loops(x2, y2, dir2, "crimson", "B2")

# ---------------- FORCE VECTORS ----------------
# Force is applied at the center of the wires
f_len = 1.5
if interaction == "Attraction":
    # Arrows pointing inward
    ax.quiver(x1, 0, 0, f_len, 0, 0, color='green', linewidth=4, label="Force (F)")
    ax.quiver(x2, 0, 0, -f_len, 0, 0, color='green', linewidth=4)
else:
    # Arrows pointing outward
    ax.quiver(x1, 0, 0, -f_len, 0, 0, color='green', linewidth=4, label="Force (F)")
    ax.quiver(x2, 0, 0, f_len, 0, 0, color='green', linewidth=4)

# ---------------- PLOT STYLING ----------------
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-5, 5)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Wire Length")
ax.set_title(f"Magnetic Field Interaction: {interaction}", fontsize=16)

# Labels for currents
ax.text(x1, 0, 5.5, f"I₁ = {I1}A", color='blue', fontweight='bold')
ax.text(x2, 0, 5.5, f"I₂ = {I2}A", color='red', fontweight='bold')

# Better viewing angle
ax.view_init(elev=20, azim=30)
st.pyplot(fig)

# ---------------- CALCULATIONS ----------------
mu0 = 4 * np.pi * 1e-7
force_m = (mu0 * I1 * I2) / (2 * np.pi * d)

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Physics Data")
    st.write(f"**Interaction Type:** {interaction}")
    st.write(f"**Force per unit length (F/L):**")
    st.code(f"{force_m:.4e} N/m")

with col2:
    st.subheader("📖 According to Ampere's Law")
    st.latex(r"\frac{F}{L} = \frac{\mu_0 \cdot I_1 \cdot I_2}{2\pi \cdot d}")
    st.caption("Where μ₀ = 4π × 10⁻⁷ T·m/A")
