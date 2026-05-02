# ============================================================
# AMPERE'S CIRCUITAL LAW VISUALIZER & MAGNETIC FIELD SIMULATOR
# Streamlit App
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ampere's Circuital Law Visualizer",
    page_icon="🧲",
    layout="wide"
)

# ---------------- CONSTANTS ----------------
mu0 = 4 * np.pi * 1e-7

# ---------------- TITLE ----------------
st.title("🧲 Ampere’s Circuital Law Visualizer")
st.markdown("### Explore magnetic fields for different current geometries using Ampere’s Law")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ System Parameters")

geometry = st.sidebar.selectbox(
    "Select Geometry",
    ["Straight Conductor", "Solenoid", "Toroid"]
)

I = st.sidebar.slider("Current I (A)", 0.1, 100.0, 10.0)

if geometry == "Straight Conductor":
    r = st.sidebar.slider("Distance from conductor r (m)", 0.01, 1.0, 0.1)

elif geometry == "Solenoid":
    N = st.sidebar.slider("Number of Turns N", 10, 1000, 200)
    L = st.sidebar.slider("Length of Solenoid L (m)", 0.1, 5.0, 1.0)
    mu_r = st.sidebar.slider("Relative Permeability μr", 1, 5000, 100)

elif geometry == "Toroid":
    N = st.sidebar.slider("Number of Turns N", 10, 1000, 300)
    r = st.sidebar.slider("Mean Radius r (m)", 0.05, 2.0, 0.3)
    mu_r = st.sidebar.slider("Relative Permeability μr", 1, 5000, 500)

# ---------------- MAIN DISPLAY ----------------
col1, col2 = st.columns([1, 1])

# ============================================================
# STRAIGHT CONDUCTOR
# ============================================================
if geometry == "Straight Conductor":
    H = I / (2 * np.pi * r)
    B = mu0 * H

    with col1:
        st.subheader("📘 Formula")
        st.latex(r"\oint \vec{H}\cdot d\vec{l}=I_{enc}")
        st.latex(r"H=\frac{I}{2\pi r}")
        st.latex(r"B=\mu_0 H")

        st.metric("Magnetic Field Intensity H (A/m)", f"{H:.4f}")
        st.metric("Flux Density B (Tesla)", f"{B:.8f}")

    with col2:
        st.subheader("🌀 Magnetic Field Around Straight Conductor")

        fig, ax = plt.subplots(figsize=(6, 6))

        theta = np.linspace(0, 2*np.pi, 300)

        for radius in np.linspace(0.2, 1.0, 5):
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            ax.plot(x, y)

        ax.scatter(0, 0, s=200, marker='o')
        ax.text(0, 0, "I", ha='center', va='center', color='white')

        ax.set_aspect('equal')
        ax.set_title("Circular Magnetic Field Lines")
        ax.grid(True)

        st.pyplot(fig)

# ============================================================
# SOLENOID
# ============================================================
elif geometry == "Solenoid":
    n = N / L
    H = n * I
    B = mu0 * mu_r * H

    with col1:
        st.subheader("📘 Formula")
        st.latex(r"H=nI")
        st.latex(r"n=\frac{N}{L}")
        st.latex(r"B=\mu_0 \mu_r H")

        st.metric("Turns per meter n", f"{n:.2f}")
        st.metric("Magnetic Field Intensity H (A/m)", f"{H:.2f}")
        st.metric("Flux Density B (Tesla)", f"{B:.6f}")

    with col2:
        st.subheader("🧲 Solenoid Magnetic Field")

        fig, ax = plt.subplots(figsize=(10, 4))

        # Draw coils
        x = np.linspace(0, L, N)
        y = np.sin(2 * np.pi * N * x / L) * 0.2
        ax.plot(x, y)

        # Field arrows
        for pos in np.linspace(0.1, L-0.1, 12):
            ax.arrow(pos, 0, 0.15, 0,
                     head_width=0.05,
                     head_length=0.05)

        ax.set_xlim(-0.2, L+0.2)
        ax.set_ylim(-0.5, 0.5)
        ax.set_title("Uniform Magnetic Field Inside Solenoid")
        ax.grid(True)

        st.pyplot(fig)

# ============================================================
# TOROID
# ============================================================
elif geometry == "Toroid":
    H = (N * I) / (2 * np.pi * r)
    B = mu0 * mu_r * H

    with col1:
        st.subheader("📘 Formula")
        st.latex(r"H=\frac{NI}{2\pi r}")
        st.latex(r"B=\mu_0 \mu_r H")

        st.metric("Magnetic Field Intensity H (A/m)", f"{H:.2f}")
        st.metric("Flux Density B (Tesla)", f"{B:.6f}")

    with col2:
        st.subheader("🔄 Toroidal Magnetic Field")

        fig, ax = plt.subplots(figsize=(6, 6))

        theta = np.linspace(0, 2*np.pi, 300)

        # Outer and inner radius
        r_outer = 1.0
        r_inner = 0.5

        x_outer = r_outer * np.cos(theta)
        y_outer = r_outer * np.sin(theta)

        x_inner = r_inner * np.cos(theta)
        y_inner = r_inner * np.sin(theta)

        ax.plot(x_outer, y_outer)
        ax.plot(x_inner, y_inner)

        # Magnetic field loops
        for radius in np.linspace(r_inner + 0.05, r_outer - 0.05, 6):
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            ax.plot(x, y, linestyle='--')

        ax.set_aspect('equal')
        ax.set_title("Toroidal Closed Magnetic Path")
        ax.grid(True)

        st.pyplot(fig)

# ---------------- THEORY SECTION ----------------
st.markdown("---")
st.header("📚 About Ampere’s Circuital Law")

st.write("""
Ampere’s Circuital Law states that the line integral of magnetic field intensity (H)
around any closed path equals the total current enclosed.

### General Equation:
""")

st.latex(r"\oint \vec{H}\cdot d\vec{l}=I_{enc}")

st.write("""
### Key Applications:
- Straight conductors
- Solenoids
- Toroids
- Magnetic circuits

### Important Insight:
Ampere’s Law works best for highly symmetrical magnetic field distributions.
""")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚡ Developed for Electrical Engineering Visualization | AmpereX")
