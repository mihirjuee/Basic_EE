import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================================
# PAGE CONFIGURATION
# =========================================
st.set_page_config(
    page_title="Inductance Simulation Lab",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# CUSTOM CSS FOR MOBILE + CLEAN UI
# =========================================
st.markdown("""
<style>
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
h1 {
    font-size: 2.3rem !important;
    color: #0F172A;
    text-align: center;
}
h2, h3 {
    color: #1D4ED8;
}
.stMetric {
    background-color: #F8FAFC;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
.footer {
    text-align: center;
    padding: 15px;
    font-size: 1.1rem;
    font-weight: bold;
    color: #0F172A;
    margin-top: 30px;
    border-top: 2px solid #CBD5E1;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================
st.title("🧲 Inductance Simulation Lab")
st.markdown("### Explore Self-Inductance vs Mutual Inductance Dynamically")

# =========================================
# SIDEBAR INPUTS
# =========================================
st.sidebar.header("🔧 System Parameters")

# Coil 1
st.sidebar.subheader("Primary Coil")
N1 = st.sidebar.slider("Turns in Coil 1 (N1)", 10, 500, 150, 10)
di1_dt = st.sidebar.slider("Current Change Rate di/dt (A/s)", -50, 50, 20, 5)

# Coil 2
st.sidebar.subheader("Secondary Coil")
N2 = st.sidebar.slider("Turns in Coil 2 (N2)", 10, 500, 200, 10)

# Coupling
st.sidebar.subheader("Magnetic Coupling")
k = st.sidebar.slider("Coupling Coefficient (k)", 0.0, 1.0, 0.6, 0.05)

# =========================================
# CONSTANTS
# =========================================
mu_0 = 4 * np.pi * 1e-7
mu_r = 1000
A = 5e-4
l = 0.1

# =========================================
# CALCULATIONS
# =========================================
L1 = (mu_r * mu_0 * N1**2 * A) / l
L2 = (mu_r * mu_0 * N2**2 * A) / l

M = k * np.sqrt(L1 * L2)

# EMFs
emf_self = -L1 * di1_dt
emf_mutual = -M * di1_dt

# Flux Linkage
flux1 = L1 * di1_dt
flux2 = M * di1_dt

# =========================================
# FORMULAS SECTION
# =========================================
st.markdown("### 📘 Governing Equations")
st.latex(r"L = \frac{\mu N^2 A}{l}")
st.latex(r"M = k\sqrt{L_1L_2}")
st.latex(r"e = -L\frac{di}{dt}, \quad e_2 = -M\frac{di}{dt}")

# =========================================
# DASHBOARD
# =========================================
col1, col2 = st.columns(2)

with col1:
    st.header("🔹 Self-Inductance")
    st.metric("Self-Inductance L₁", f"{L1*1000:.2f} mH")
    st.metric("Back EMF e₁", f"{emf_self:.3f} V")
    st.metric("Flux Linkage λ₁", f"{flux1:.4f} Wb-turn")
    st.info("Current change in Coil 1 induces voltage within itself opposing the change (Lenz’s Law).")

with col2:
    st.header("🔸 Mutual Inductance")
    st.metric("Mutual Inductance M", f"{M*1000:.2f} mH")
    st.metric("Induced EMF e₂", f"{emf_mutual:.3f} V")
    st.metric("Flux Linkage λ₂", f"{flux2:.4f} Wb-turn")
    st.info("Changing flux from Coil 1 links Coil 2 and induces voltage across it.")

# =========================================
# COIL VISUALIZATION
# =========================================
st.markdown("---")
st.header("🌀 Coil Coupling Visualization")

fig1, ax1 = plt.subplots(figsize=(8, 3))
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 4)

# Coil 1
for i in range(5):
    circle1 = plt.Circle((2 + i*0.3, 2), 0.15, fill=False, linewidth=2, color='blue')
    ax1.add_patch(circle1)

# Coil 2
for i in range(5):
    circle2 = plt.Circle((6 + i*0.3, 2), 0.15, fill=False, linewidth=2, color='orange')
    ax1.add_patch(circle2)

# Flux lines
for y in [1.5, 2, 2.5]:
    ax1.arrow(3.8, y, 1.8, 0, head_width=0.1, head_length=0.2,
              fc='green', ec='green', linestyle='--')

ax1.text(2.2, 2.6, "Coil 1", color="blue", fontsize=12)
ax1.text(6.2, 2.6, "Coil 2", color="orange", fontsize=12)
ax1.text(4.5, 3.0, f"k = {k:.2f}", color="green", fontsize=12)

ax1.axis('off')
st.pyplot(fig1)

# =========================================
# WAVEFORMS
# =========================================
st.markdown("---")
st.header("📈 Dynamic Waveform Analysis")

t = np.linspace(0, 0.1, 500)
f = 50

# Current profile
current = np.sin(2 * np.pi * f * t) * (di1_dt / (2 * np.pi * f))
di_dt_profile = di1_dt * np.cos(2 * np.pi * f * t)

# Voltages
v_self = -L1 * di_dt_profile
v_mutual = -M * di_dt_profile

fig2, ax = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

# Current
ax[0].plot(t*1000, current, linewidth=2, label="Primary Current i₁(t)")
ax[0].set_ylabel("Current (A)")
ax[0].legend()
ax[0].grid(True)

# Self voltage
ax[1].plot(t*1000, v_self, linewidth=2, label="Self-Induced Voltage e₁")
ax[1].set_ylabel("Voltage (V)")
ax[1].legend()
ax[1].grid(True)

# Mutual voltage
ax[2].plot(t*1000, v_mutual, linewidth=2, linestyle='--', label="Mutual-Induced Voltage e₂")
ax[2].set_ylabel("Voltage (V)")
ax[2].set_xlabel("Time (ms)")
ax[2].legend()
ax[2].grid(True)

plt.tight_layout()
st.pyplot(fig2)

# =========================================
# COMPARISON INSIGHT
# =========================================
st.markdown("---")
st.header("⚡ Key Learning")
if k < 0.3:
    st.warning("Weak magnetic coupling → Low mutual inductance")
elif k < 0.7:
    st.info("Moderate coupling → Partial flux linkage")
else:
    st.success("Strong coupling → Transformer-like operation")

# =========================================
# FOOTER
# =========================================
st.markdown(
    '<div class="footer">🚀 Adjust turns, coupling, and di/dt to master inductance concepts interactively</div>',
    unsafe_allow_html=True
)
