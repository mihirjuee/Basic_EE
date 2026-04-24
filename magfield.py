import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rotating Magnetic Field", layout="centered")

st.title("🧲 Rotating Magnetic Field (Visualization)")

st.markdown("""
### 🔹 Concept
A time-varying current creates a **rotating magnetic field effect** in simulation.
Move the slider to see rotation.
""")

# ================= SLIDER =================
theta = st.slider("Phase Angle (ωt)", 0, 360, 0)

theta = np.radians(theta)

# ================= GRID =================
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2) + 1e-6

# ================= ORIGINAL FIELD =================
Bx = -Y / R**2
By = X / R**2

# ================= ROTATION MATRIX =================
Bx_rot = Bx * np.cos(theta) - By * np.sin(theta)
By_rot = Bx * np.sin(theta) + By * np.cos(theta)

# ================= PLOT =================
fig, ax = plt.subplots(figsize=(6, 6))

ax.quiver(X, Y, Bx_rot, By_rot, color='blue')

# center conductor
if np.sin(theta) >= 0:
    ax.text(0, 0, "⊙", fontsize=30, ha='center', va='center', color='red')
else:
    ax.text(0, 0, "⊗", fontsize=30, ha='center', va='center', color='blue')

ax.set_title("Rotating Magnetic Field Visualization")
ax.set_aspect('equal')
ax.grid()

st.pyplot(fig)

st.success("Move slider → Field rotates 🔄")
