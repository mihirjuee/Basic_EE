# ============================================================
# MAGNETICALLY COUPLED CIRCUIT ANALYZER
# Streamlit App for Mutual Inductance / Dot Convention / KVL
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Magnetically Coupled Circuit Analyzer",
    page_icon="🧲",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🧲 Magnetically Coupled Circuit Analyzer")
st.markdown("### Analyze self inductance, mutual inductance, coupling coefficient, induced voltage, and dot convention")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Circuit Parameters")

L1 = st.sidebar.number_input("Self Inductance L1 (H)", min_value=0.001, value=2.0, step=0.1)
L2 = st.sidebar.number_input("Self Inductance L2 (H)", min_value=0.001, value=1.5, step=0.1)

k = st.sidebar.slider("Coupling Coefficient k", 0.0, 1.0, 0.8)

I1 = st.sidebar.number_input("Primary Current I1 (A)", value=5.0)
I2 = st.sidebar.number_input("Secondary Current I2 (A)", value=2.0)

f = st.sidebar.slider("Frequency (Hz)", 1, 5000, 50)

connection = st.sidebar.selectbox(
    "Connection Type",
    ["Series Aiding", "Series Opposing"]
)

# ---------------- CALCULATIONS ----------------
M = k * np.sqrt(L1 * L2)

omega = 2 * np.pi * f

X_L1 = omega * L1
X_L2 = omega * L2
X_M = omega * M

if connection == "Series Aiding":
    L_eq = L1 + L2 + 2 * M
else:
    L_eq = L1 + L2 - 2 * M

V1_induced = omega * M * I2
V2_induced = omega * M * I1

Energy = 0.5 * L1 * I1**2 + 0.5 * L2 * I2**2 + M * I1 * I2

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1])

# ============================================================
# RESULTS PANEL
# ============================================================
with col1:
    st.subheader("📘 Key Equations")

    st.latex(r"M = k\sqrt{L_1L_2}")
    st.latex(r"V_M = \omega M I")
    st.latex(r"L_{eq}=L_1+L_2\pm2M")

    st.subheader("📊 Computed Results")

    st.metric("Mutual Inductance M (H)", f"{M:.4f}")
    st.metric("Equivalent Inductance Leq (H)", f"{L_eq:.4f}")
    st.metric("Primary Reactance XL1 (Ω)", f"{X_L1:.2f}")
    st.metric("Secondary Reactance XL2 (Ω)", f"{X_L2:.2f}")
    st.metric("Mutual Reactance XM (Ω)", f"{X_M:.2f}")
    st.metric("Induced Voltage in Coil-1 (V)", f"{V1_induced:.2f}")
    st.metric("Induced Voltage in Coil-2 (V)", f"{V2_induced:.2f}")
    st.metric("Stored Magnetic Energy (J)", f"{Energy:.4f}")

# ============================================================
# CIRCUIT DIAGRAM PANEL
# ============================================================
with col2:
    st.subheader("🔄 Dot Convention & Coil Coupling")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Coil 1
    x1 = np.linspace(1, 4, 200)
    y1 = np.sin(8 * np.pi * (x1 - 1)) * 0.2 + 4
    ax.plot(x1, y1, linewidth=2)

    # Coil 2
    x2 = np.linspace(1, 4, 200)
    y2 = np.sin(8 * np.pi * (x2 - 1)) * 0.2 + 2
    ax.plot(x2, y2, linewidth=2)

    # Dot positions
    if connection == "Series Aiding":
        ax.scatter(1, 4, s=100)
        ax.scatter(1, 2, s=100)
    else:
        ax.scatter(1, 4, s=100)
        ax.scatter(4, 2, s=100)

    # Labels
    ax.text(0.5, 4, "L1", fontsize=12)
    ax.text(0.5, 2, "L2", fontsize=12)

    # Magnetic flux arrows
    ax.arrow(4.5, 3.8, 0, -1.2, head_width=0.15, head_length=0.15)
    ax.text(4.7, 3, "Mutual Flux Φm")

    ax.set_xlim(0, 6)
    ax.set_ylim(1, 5)
    ax.axis("off")

    st.pyplot(fig)

# ============================================================
# WAVEFORM ANALYSIS
# ============================================================
st.markdown("---")
st.subheader("📈 Induced Voltage Waveforms")

t = np.linspace(0, 0.05, 1000)

i1_wave = I1 * np.sin(omega * t)
i2_wave = I2 * np.sin(omega * t)

v1_wave = omega * M * I2 * np.cos(omega * t)
v2_wave = omega * M * I1 * np.cos(omega * t)

fig2, ax2 = plt.subplots(figsize=(12, 5))

ax2.plot(t, i1_wave, label="Primary Current i1")
ax2.plot(t, i2_wave, label="Secondary Current i2")
ax2.plot(t, v1_wave, label="Induced Voltage v1")
ax2.plot(t, v2_wave, label="Induced Voltage v2")

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Amplitude")
ax2.set_title("Current & Induced Voltage Waveforms")
ax2.legend()
ax2.grid(True)

st.pyplot(fig2)

# ============================================================
# EDUCATIONAL SECTION
# ============================================================
st.markdown("---")
st.header("📚 Understanding Magnetically Coupled Circuits")

st.write("""
### What is Magnetic Coupling?
When magnetic flux produced by one coil links another coil, mutual inductance exists.

### Key Concepts:
- **L1, L2:** Self inductances
- **M:** Mutual inductance
- **k:** Coupling coefficient (0 to 1)
- **Series Aiding:** Fluxes reinforce
- **Series Opposing:** Fluxes oppose

### Dot Convention:
If current enters dotted terminal of one coil, induced voltage polarity at dotted terminal of second coil depends on coupling orientation.
""")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚡ EE Learning Tool | Mutual Inductance • Dot Convention • Energy Storage")
