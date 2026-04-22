import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(page_title="RLC Resonance Pro", layout="wide")

# =========================
# 🎨 IEEE STYLE UI
# =========================
st.markdown("""
<style>
.stApp {background-color: #f4f6f9;}
.main {color: #1a1a1a; font-family: 'Segoe UI', sans-serif;}
h1, h2, h3 {color: #003366;}
section[data-testid="stSidebar"] {background-color: #ffffff;}
section[data-testid="stSidebar"] * {color: #333 !important;}
div[data-testid="stMetric"] {
    background-color: white;
    padding: 12px;
    border-radius: 10px;
    border-left: 5px solid #003366;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ RLC Series Resonance Lab")

# =========================
# 🎛️ INPUTS
# =========================
st.sidebar.header("🔧 Circuit Parameters")

R = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)
L_mH = st.sidebar.slider("Inductance (mH)", 1, 100, 10)
C_uF = st.sidebar.slider("Capacitance (uF)", 1, 500, 50, format="%.2f")

# Convert to Farads for calculation
L = L_mH * 1e-3
C = C_uF * 1e-6
# =========================
# ⚡ RESONANCE
# =========================
f_res = 1 / (2 * np.pi * np.sqrt(L * C))
w_res = 2 * np.pi * f_res

# =========================
# 🔄 VARIABLE FREQUENCY SUPPLY
# =========================
st.sidebar.subheader("🔄 Variable Frequency Supply")
V = st.sidebar.slider("Supply Voltage (V)", 10.0, 500.0, 230.0)

f_input = st.sidebar.slider(
    "Supply Frequency (Hz)",
    1.0,
    float(5 * f_res),
    float(f_res)
)

w_input = 2 * np.pi * f_input

# =========================
# 📈 FREQUENCY SWEEP
# =========================
f = np.linspace(1, 5 * f_res, 500)
w = 2 * np.pi * f

Xl = w * L
Xc = 1 / (w * C)

Z = np.sqrt(R**2 + (Xl - Xc)**2)
I = V / Z
P = I**2 * R

# =========================
# ⚡ BANDWIDTH & Q
# =========================
Q = w_res * L / R
BW = f_res / Q
f1 = f_res - BW/2
f2 = f_res + BW/2

# =========================
# ⚡ PERFORMANCE @ SELECTED FREQUENCY
# =========================
Xl_in = w_input * L
Xc_in = 1 / (w_input * C)

Z_in = complex(R, Xl_in - Xc_in)
Z_mag = abs(Z_in)

I_in = V / Z_mag
P_in = I_in**2 * R
pf = R / Z_mag

# =========================
# 📊 METRICS
# =========================
st.subheader("⚡ Key Parameters")

c1, c2, c3 = st.columns(3)
c1.metric("Resonant Frequency (Hz)", f"{f_res:.2f}")
c2.metric("Quality Factor (Q)", f"{Q:.2f}")
c3.metric("Bandwidth (Hz)", f"{BW:.2f}")

# =========================
# 🔌 CIRCUIT DIAGRAM
# =========================
import io

st.subheader("🔌 RLC Circuit")

d = schemdraw.Drawing(unit=3)

# Source
d += elm.SourceSin().label(f"{V:.2f} V\n{f_input:.2f} Hz")

# Elements
d += elm.Resistor().right().label(f"{R:.2f} Ω")
d += elm.Inductor().right().label(f"{L_mH:.2f} mH")
d += elm.Capacitor().right().label(f"{C_uF:.2f} uF")

# Return path
d += elm.Line().down()
d += elm.Line().left().length(9)


# 🔥 Convert to image buffer (IMPORTANT FIX)
buf = io.BytesIO()
d.save(buf)   # Save drawing as image
buf.seek(0)

# Display in Streamlit
st.image(buf)



# =========================
# 📈 FREQUENCY RESPONSE
# =========================
st.subheader("📈 Frequency Response")

fig, ax = plt.subplots()

ax.plot(f, Z, label="Impedance")
ax.plot(f, I, label="Current")
#ax.plot(f, P, label="Power")

ax.axvline(f_res, linestyle='--', label="Resonance")
ax.axvline(f1, linestyle=':', label="f1")
ax.axvline(f2, linestyle=':', label="f2")

# Operating point
ax.axvline(f_input, linewidth=2, label="Operating Point")

ax.fill_between(f, 0, max(I), where=(f >= f1) & (f <= f2), alpha=0.2)

ax.set_xlabel("Frequency (Hz)")
ax.legend()
ax.grid()

st.pyplot(fig)

# =========================
# ⚡ LIVE PERFORMANCE
# =========================
st.subheader("⚡ Performance at Selected Frequency")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Frequency (Hz)", f"{f_input:.2f}")
c2.metric("Current (A)", f"{I_in:.2f}")
c3.metric("Power (W)", f"{P_in:.2f}")
c4.metric("Power Factor", f"{pf:.2f}")

# =========================
# 🧠 REGION DETECTION
# =========================
if abs(f_input - f_res) < 0.05 * f_res:
    st.success("✅ Operating at Resonance")
elif f_input < f_res:
    st.info("🔵 Capacitive Region (XC > XL)")
else:
    st.warning("🟠 Inductive Region (XL > XC)")

# =========================
# 📐 PHASOR DIAGRAM
# =========================
st.subheader("📐 Phasor Diagram")

Xl_ph = w_input * L
Xc_ph = 1 / (w_input * C)

Z_ph = complex(R, Xl_ph - Xc_ph)
I_ph = V / abs(Z_ph)

VR = I_ph * R
VL = I_ph * Xl_ph
VC = I_ph * Xc_ph

fig2, ax2 = plt.subplots()

# VR
ax2.arrow(0, 0, VR, 0, head_width=0.5)
ax2.text(VR, 0, "VR")

# VL
ax2.arrow(0, 0, 0, VL, head_width=0.5)
ax2.text(0, VL, "VL")

# VC
ax2.arrow(0, 0, 0, -VC, head_width=0.5)
ax2.text(0, -VC, "VC")

# Resultant voltage
ax2.arrow(0, 0, VR, VL - VC, head_width=0.5, color='black')
ax2.text(VR, VL - VC, "V")

ax2.set_title("Voltage Phasor")
ax2.set_aspect('equal')
ax2.grid()

st.pyplot(fig2)

# =========================
# 📘 THEORY
# =========================
st.markdown("""
### 📘 Key Concepts

- At resonance: **XL = XC**
- Impedance is minimum → **Z = R**
- Current is maximum  
- Power factor = unity  

### ⚡ Bandwidth
- Frequency range where power ≥ 50% of maximum  

### 🎯 Quality Factor
- Higher Q → sharper resonance curve  
""")
