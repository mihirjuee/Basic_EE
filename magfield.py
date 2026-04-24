import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ================= PAGE =================
st.set_page_config(page_title="Magnetic Field Simulator", layout="centered")

st.title("🧲 Magnetic Field Around a Current-Carrying Conductor")

st.markdown("""
### 🔹 Concept
- A current-carrying conductor produces a **circular magnetic field**
- Direction follows the **Right-Hand Rule**
""")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (A)", -10.0, 10.0, 5.0, step=0.5)

# ================= GRID =================
x = np.linspace(-5, 5, 25)
y = np.linspace(-5, 5, 25)
X, Y = np.meshgrid(x, y)

# ================= FIELD CALC =================
R = np.sqrt(X**2 + Y**2) + 1e-6

Bx = -I * Y / R**2
By = I * X / R**2

# ================= PLOT =================
fig, ax = plt.subplots(figsize=(6, 6))

# Vector field
ax.quiver(X, Y, Bx, By)

# Conductor at center
if I > 0:
    ax.scatter(0, 0, s=300, c='red')
    ax.text(0, 0, "⊙", fontsize=20, ha='center', va='center')
else:
    ax.scatter(0, 0, s=300, c='blue')
    ax.text(0, 0, "⊗", fontsize=20, ha='center', va='center')

# Labels
ax.set_title("Magnetic Field Lines")
ax.set_xlabel("X")
ax.set_ylabel("Y")

ax.set_aspect('equal')
ax.grid()

# ================= DIRECTION INDICATOR =================
if I > 0:
    direction = "Counterclockwise 🔄 "
    rule = "Thumb → Current (out of page), Fingers → Field"
else:
    direction = "Clockwise 🔁"
    rule = "Thumb → Current (into page), Fingers → Field"

st.pyplot(fig)

# ================= INFO =================
st.subheader("📘 Interpretation")

st.write(f"**Field Direction:** {direction}")
st.write(f"**Right-Hand Rule:** {rule}")

st.markdown("""
👉 Increase current → Stronger magnetic field  
👉 Reverse current → Field direction reverses  
""")

st.success("Interactive Visualization Ready ✅")
