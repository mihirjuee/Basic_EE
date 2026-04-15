import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Phasor Relations", layout="wide")

# --- HEADER WITH LOGO ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("⚡ **LOGO**")

with col_title:
    st.title("3-Phase Phase & Line Relationships")

# --- CONTROLS ---
st.sidebar.header("Parameters")
v_mag = st.sidebar.slider("Voltage Magnitude (V_ph)", 50, 240, 120)
i_mag = st.sidebar.slider("Current Magnitude (I_ph)", 1, 20, 10)
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 0)

# --- MATH CONSTANTS ---
rad120 = np.deg2rad(120)
phi = np.deg2rad(phi_deg)

# --- PLOTTING FUNCTION ---
def draw_detailed_phasor(ax, p_vecs, l_vecs, p_labels, l_labels, title, unit, is_voltage=True):
    ax.set_facecolor('white')
    limit = max(np.abs(l_vecs)) * 1.4
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    
    # Draw Axes
    ax.axhline(0, color='black', lw=1, alpha=0.3)
    ax.axvline(0, color='black', lw=1, alpha=0.3)
    
    colors = ['#d62728', '#bcbd22', '#1f77b4'] # Red, Yellow, Blue
    
    # 1. Draw Phase Vectors
    for v, col, lab in zip(p_vecs, colors, p_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.5))
        ax.text(v.real*1.1, v.imag*1.1, lab, color=col, fontweight='bold')

    # 2. Draw Parallelogram for Phase A Line Vector
    # For Star: Vab = Van - Vbn | For Delta: Ia = Iab - Ica
    v1 = p_vecs[0]
    v2_neg = -p_vecs[2] if not is_voltage else -p_vecs[1]
    
    # Dotted lines for parallelogram
    ax.plot([v1.real, l_vecs[0].real], [v1.imag, l_vecs[0].imag], 'k--', lw=1, alpha=0.4)
    ax.plot([v2_neg.real, l_vecs[0].real], [v2_neg.imag, l_vecs[0].imag], 'k--', lw=1, alpha=0.4)
    ax.plot([0, v2_neg.real], [0, v2_neg.imag], 'k:', lw=1, alpha=0.4) # Negative vector reference

    # 3. Draw Line Vectors
    for v, col, lab in zip(l_vecs, colors, l_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=3))
        ax.text(v.real*1.15, v.imag*1.15, lab, color=col, fontweight='extra bold', fontsize=12)

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Star Voltage (Line = Phase1 - Phase2)
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
Vab, Vbc, Vca = Van-Vbn, Vbn-Vcn, Vcn-Van

# Delta Current (Line = Phase_branch1 - Phase_branch2)
Iab = i_mag * np.exp(-1j * phi)
Ibc = i_mag * np.exp(-1j * (rad120 + phi))
Ica = i_mag * np.exp(1j * (rad120 - phi))
Ia, Ib, Ic = Iab-Ica, Ibc-Iab, Ica-Ibc

# --- UI LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Star: Phase vs Line Voltage")
    fig1, ax1 = plt.subplots(figsize=(6,6))
    draw_detailed_phasor(ax1, [Van, Vbn, Vcn], [Vab, Vbc, Vca], 
                        ["Van", "Vbn", "Vcn"], ["Vab", "Vbc", "Vca"], 
                        "Voltage Relations (Star)", "V", is_voltage=True)
    st.pyplot(fig1)
    st.latex(r"|V_{L}| = \sqrt{3}|V_{ph}| \angle 30^\circ")

with col2:
    st.subheader("🔺 Delta: Phase vs Line Current")
    fig2, ax2 = plt.subplots(figsize=(6,6))
    draw_detailed_phasor(ax2, [Iab, Ibc, Ica], [Ia, Ib, Ic], 
                        ["Iab", "Ibc", "Ica"], ["Ia", "Ib", "Ic"], 
                        "Current Relations (Delta)", "A", is_voltage=False)
    st.pyplot(fig2)
    st.latex(r"|I_{L}| = \sqrt{3}|I_{ph}| \angle -30^\circ")

st.info("**Visual Note:** The dotted lines show the vector subtraction construction. In Star, Line Voltage leads Phase Voltage by 30°. In Delta, Line Current lags Phase Current by 30°.")
