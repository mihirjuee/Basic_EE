import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="RLC Circuit Pro", layout="wide")

# --- Functions for Graphics ---

def draw_schematic():
    """Draws a professional RLC series circuit schematic."""
    fig, ax = plt.subplots(figsize=(8, 3))
    # Main loop wires
    ax.plot([0, 0, 2], [0, 4, 4], 'k-', lw=1.5)   
    ax.plot([8, 10, 10, 0], [4, 4, 0, 0], 'k-', lw=1.5) 
    
    # AC Source
    circle = plt.Circle((0, 2), 0.5, color='black', fill=False, lw=2)
    ax.add_patch(circle)
    ax.text(-0.15, 1.8, "~", fontsize=25)
    ax.text(-1.5, 2, "Vs", fontsize=12, fontweight='bold')

    # Resistor R
    ax.add_patch(plt.Rectangle((2, 3.7), 1.5, 0.6, facecolor='white', edgecolor='black', lw=2))
    ax.text(2.5, 4.5, "R", fontsize=12, fontweight='bold')

    # Inductor L (simplified coils)
    for i in range(3):
        ax.add_patch(plt.Circle((4.5 + i*0.4, 4), 0.25, color='black', fill=False, lw=1.5))
    ax.text(4.9, 4.5, "L", fontsize=12, fontweight='bold')

    # Capacitor C
    ax.plot([7.5, 7.5], [3.3, 4.7], 'k-', lw=3)
    ax.plot([8.0, 8.0], [3.3, 4.7], 'k-', lw=3)
    ax.text(7.6, 4.8, "C", fontsize=12, fontweight='bold')

    ax.set_xlim(-2, 12)
    ax.set_ylim(-1, 6)
    ax.axis('off')
    return fig

def draw_phasors(vr, vl, vc, vs, phase_deg):
    """Draws the phasor diagram with voltage vectors."""
    fig, ax = plt.subplots(figsize=(6, 6))
    max_val = max(vr, vl, vc, vs) * 1.2
    
    # Reference axis
    ax.axhline(0, color='gray', lw=1, ls='--')
    ax.axvline(0, color='gray', lw=1, ls='--')

    # VR - Horizontal (In phase with Current)
    ax.quiver(0, 0, vr, 0, angles='xy', scale_units='xy', scale=1, color='red', label=f'Vr ({vr:.1f}V)')
    # VL - Vertical Up
    ax.quiver(0, 0, 0, vl, angles='xy', scale_units='xy', scale=1, color='blue', label=f'Vl ({vl:.1f}V)')
    # VC - Vertical Down
    ax.quiver(0, 0, 0, -vc, angles='xy', scale_units='xy', scale=1, color='green', label=f'Vc ({vc:.1f}V)')
    # Vs - Resultant
    ax.quiver(0, 0, vr, (vl-vc), angles='xy', scale_units='xy', scale=1, color='black', width=0.015, label=f'Vs ({vs:.1f}V)')

    ax.set_xlim(-max_val/5, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_title(f"Phasor Diagram (Phase: {phase_deg:.1f}°)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

# --- Main App Logic ---

st.title("🔌 Series RLC Analyzer & Phasor Generator")

with st.sidebar:
    st.header("Input Parameters")
    V_rms = st.slider("Source Voltage (Vrms)", 10, 500, 230)
    freq = st.slider("Frequency (Hz)", 1, 200, 50)
    R = st.number_input("Resistance (Ω)", value=100.0)
    L_mH = st.number_input("Inductance (mH)", value=300.0)
    C_uF = st.number_input("Capacitance (µF)", value=30.0)

# Physics Engine
L = L_mH / 1000
C = C_uF / 1e6
omega = 2 * np.pi * freq

XL = omega * L
XC = 1 / (omega * C)
X_net = XL - XC
Z = np.sqrt(R**2 + X_net**2)
I_rms = V_rms / Z
phase_rad = np.arctan2(X_net, R)
phase_deg = np.degrees(phase_rad)

# Voltages
VR = I_rms * R
VL = I_rms * XL
VC = I_rms * XC

# --- UI Tabs ---
tab1, tab2, tab3 = st.tabs(["🏠 Circuit Overview", "📈 Phasor Analysis", "🔢 Step-by-Step Math"])

with tab1:
    st.subheader("Circuit Schematic")
    st.pyplot(draw_schematic())
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Impedance (Z)", f"{Z:.2f} Ω")
    col2.metric("RMS Current (I)", f"{I_rms:.3f} A")
    col3.metric("Phase Angle", f"{phase_deg:.2f}°")

with tab2:
    st.subheader("Vector Representation")
    st.pyplot(draw_phasors(VR, VL, VC, V_rms, phase_deg))
    
    if XL > XC:
        st.info("💡 **Inductive Circuit**: Voltage leads current (ELI).")
    elif XC > XL:
        st.info("💡 **Capacitive Circuit**: Current leads voltage (ICE).")
    else:
        st.success("🎯 **Resonance**: $X_L = X_C$. The circuit acts as purely resistive.")

with tab3:
    st.subheader("Calculated Values")
    st.latex(rf"X_L = 2\pi f L = {XL:.2f} \Omega")
    st.latex(rf"X_C = \frac{{1}}{{2\pi f C}} = {XC:.2f} \Omega")
    st.latex(rf"Z = \sqrt{{R^2 + (X_L - X_C)^2}} = {Z:.2f} \Omega")
    
    st.write("### Component Voltages")
    st.write(f"- Voltage across Resistor ($V_R$): **{VR:.2f} V**")
    st.write(f"- Voltage across Inductor ($V_L$): **{VL:.2f} V**")
    st.write(f"- Voltage across Capacitor ($V_C$): **{VC:.2f} V**")
