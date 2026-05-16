import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration for Mobile Responsiveness ---
st.set_page_config(
    page_title="Inductance Simulation Lab",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to optimize mobile view, cards, and clean typography
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { font-size: 2.2rem !important; color: #1E3A8A; text-align: center; }
    h2 { font-size: 1.5rem !important; color: #1E40AF; }
    .stSlider { padding-bottom: 1rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #047857; }
    .footer { text-align: center; padding: 20px; font-size: 1.1rem; font-weight: bold; margin-top: 30px; border-top: 1px solid #e0e0e0; }
    </style>
""", unsafe_unsafe_html=True)

st.title("🧲 Inductance Simulation Lab")
st.write("Explore the differences between Self-Inductance and Mutual Inductance dynamically.")

# --- Sidebar Inputs ---
st.sidebar.header("🔧 System Parameters")

st.sidebar.subheader("Coil 1 (Primary)")
N1 = st.sidebar.slider("Number of Turns (N1)", min_value=10, max_value=500, value=150, step=10)
di1_dt = st.sidebar.slider("Current Change Rate di1/dt (A/s)", min_value=-50, max_value=50, value=20, step=5)

st.sidebar.subheader("Coil 2 (Secondary)")
N2 = st.sidebar.slider("Number of Turns (N2)", min_value=10, max_value=500, value=200, step=10)

st.sidebar.subheader("Magnetic Coupling")
k = st.sidebar.slider("Coupling Coefficient (k)", min_value=0.0, max_value=1.0, value=0.6, step=0.05)

# --- Physical Constants ---
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space
A = 5e-4                # Cross-sectional area in m^2 (fixed)
l = 0.1                 # Length of coil in m (fixed)

# --- Core Calculations ---
# Self-Inductance: L = (mu_0 * N^2 * A) / l
# (Using an idealized iron core multiplier for visualization clarity, e.g., mu_r = 1000)
mu_r = 1000 
L1 = (mu_r * mu_0 * (N1**2) * A) / l
L2 = (mu_r * mu_0 * (N2**2) * A) / l

# Mutual Inductance: M = k * sqrt(L1 * L2)
M = k * np.sqrt(L1 * L2)

# Induced EMFs (Faraday's Law)
emf_self = -L1 * di1_dt
emf_mutual = -M * di1_dt

# --- Dashboard Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔹 Self-Inductance (Coil 1)")
    st.metric(label="Self-Inductance (L1)", value=f"{L1*1000:.2f} mH")
    st.metric(label="Induced Back-EMF (e1)", value=f"{emf_self:.2f} V")
    
    # Textual representation of the single coil system
    st.info("**Mechanism:** The changing current within Coil 1 creates a self-opposing magnetic flux inside its own turns.")

with col2:
    st.header("🔸 Mutual Inductance (Coil 1 ➔ 2)")
    st.metric(label="Mutual Inductance (M)", value=f"{M*1000:.2f} mH")
    st.metric(label="Induced Secondary EMF (e2)", value=f"{emf_mutual:.2f} V")
    
    # Textual representation of the dual coil coupling system
    st.info("**Mechanism:** The expanding/collapsing magnetic flux from Coil 1 links across space to pass through the turns of Coil 2.")

st.markdown("---")

# --- Visualization Section ---
st.header("📈 Waveform & Flux Linkage Visualization")

# Time vector for simulation
t = np.linspace(0, 0.1, 500)
# Assuming a sinusoidal current profile to show dynamic phase relationships
f = 50 # 50 Hz frequency
current = np.sin(2 * np.pi * f * t) * (di1_dt / (2 * np.pi * f))
# Derivative of current (di/dt)
di_dt_profile = di1_dt * np.cos(2 * np.pi * f * t)

# Induced voltages profiles
v_self = -L1 * di_dt_profile
v_mutual = -M * di_dt_profile

# Matplotlib Plot
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
fig.patch.set_facecolor('#f9f9f9')

# Top Plot: Primary Current
ax[0].plot(t * 1000, current, color='#1E3A8A', linewidth=2, label="Primary Current i1(t)")
ax[0].set_ylabel("Current (A)", color='#1E3A8A')
ax[0].grid(True, linestyle='--', alpha=0.6)
ax[0].legend(loc="upper right")
ax[0].set_title("Input Current Profile vs Induced Voltages", fontsize=12, fontweight='bold')

# Bottom Plot: Induced Voltages
ax[1].plot(t * 1000, v_self, color='#047857', linewidth=2, label="Self-Induced Voltage e1 (Back-EMF)")
ax[1].plot(t * 1000, v_mutual, color='#B45309', linewidth=2, linestyle='--', label="Mutually Induced Voltage e2")
ax[1].set_ylabel("Induced Voltage (V)")
ax[1].set_xlabel("Time (ms)")
ax[1].grid(True, linestyle='--', alpha=0.6)
ax[1].legend(loc="upper right")

plt.tight_layout()
st.pyplot(fig)

# --- Interactive Footer ---
st.markdown('<div class="footer">Try the simulator now</div>', unsafe_allow_html=True)
