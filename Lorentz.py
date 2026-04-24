import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ================= PAGE =================
st.set_page_config(page_title="Lorentz Force Simulator", layout="centered")

st.title("⚡ Force on Current-Carrying Conductor (Lorentz Force)")

st.markdown("""
### 🔹 Concept
A current-carrying conductor placed in a magnetic field experiences a force:
""")

st.latex(r"F = B I L \sin\theta")

# ================= INPUT =================
st.sidebar.header("🔧 Controls")

I = st.sidebar.slider("Current (A)", 0.0, 10.0, 5.0, step=0.5)
B = st.sidebar.slider("Magnetic Field (T)", 0.0, 5.0, 1.0, step=0.1)
L = st.sidebar.slider("Length of Conductor (m)", 0.1, 5.0, 1.0, step=0.1)
theta = st.sidebar.slider("Angle θ (degrees)", 0, 180, 90)

theta_rad = np.radians(theta)

# ================= FORCE =================
F = B * I * L * np.sin(theta_rad)

# direction (simple sign logic)
direction = "Upward ⬆️" if np.sin(theta_rad) >= 0 else "Downward ⬇️"

# ================= DISPLAY =================
st.subheader("📊 Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Force (N)", f"{F:.2f}")

with col2:
    st.metric("Direction", direction)

# ================= DIAGRAM =================
st.subheader("📐 Visual Representation")

fig, ax = plt.subplots(figsize=(6, 5))

# conductor (wire)
ax.plot([0, L], [0, 0], linewidth=5)

# magnetic field (into page = ×)
for x in np.linspace(0, L, 5):
    ax.text(x, 1, "×", fontsize=20, ha='center')

# force arrow
ax.arrow(L/2, 0, 0, F*0.2, head_width=0.1, color='red')
ax.text(L/2, F*0.2 + 0.1, "F", color='red')

# labels
ax.text(0, -0.2, "I →", fontsize=12)

ax.set_title("Lorentz Force on Conductor")
ax.set_xlim(-0.5, L+0.5)
ax.set_ylim(-1, 2)
ax.grid()

st.pyplot(fig)

# ================= INTERPRETATION =================
st.subheader("📘 Interpretation")

st.markdown("""
- Force is maximum at 90°  
- Force is zero at 0° or 180°  
- Direction follows Fleming’s Left-Hand Rule  
""")

st.success("Lorentz Force Simulation Ready ⚡")
