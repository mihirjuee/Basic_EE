import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# --- PAGE CONFIG ---
st.set_page_config(page_title="3-Phase Phasor Diagram Master", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #000000; }
    p, h1, h2, h3, span { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_l, col_r = st.columns([1, 6])
with col_l:
    try: st.image("logo.png", width=100)
    except: st.markdown("### ⚡")
with col_r:
    st.title("Phasor Diagram: Star (Y) & Delta (Δ)")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Parameters")
v_mag = st.sidebar.slider("Voltage Magnitude", 50.0, 200.0, 120.0)
i_mag = st.sidebar.slider("Current Magnitude", 20.0, 100.0, 60.0)
phi_deg = st.sidebar.slider("Φ (Power Factor Angle)", 0, 60, 30)

# --- MATH SETUP ---
phi = np.deg2rad(phi_deg)
r120 = np.deg2rad(120)
c_map = ['#E63946', '#FFB703', '#1D3557'] # Red, Yellow, Blue/Grey

def draw_phasor_diagram(ax, is_star=True):
    ax.set_facecolor('white')
    limit = 250
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.axis('off')

    # Common components
    Van = v_mag * np.exp(1j * 0)
    Vbn = v_mag * np.exp(-1j * r120)
    Vcn = v_mag * np.exp(1j * r120)
    v_phs = [Van, Vbn, Vcn]

    if is_star:
        ax.set_title("Star (Y) Connection\nLine Voltage shifts 30° | Currents remain equal", pad=20)
        
        # Line Voltages (Vab, Vbc, Vca)
        v_lines = [Van-Vbn, Vbn-Vcn, Vcn-Van]
        v_l_labels = ["$V_{ab}$", "$V_{bc}$", "$V_{ca}$"]
        v_p_labels = ["$V_{an}$", "$V_{bn}$", "$V_{cn}$"]
        neg_labels = ["$-V_{cn}$", "$-V_{an}$", "$-V_{bn}$"]

        for i in range(3):
            col = c_map[i]
            # Phase Voltages
            ax.annotate('', xy=(v_phs[i].real, v_phs[i].imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='-|>', color=col, lw=2))
            ax.text(v_phs[i].real*1.1, v_phs[i].imag*1.1, v_p_labels[i], color=col)

            # Negative Phase Vectors (Dotted)
            neg_v = -v_phs[(i+1)%3]
            ax.annotate('', xy=(neg_v.real, neg_v.imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='->', color=col, lw=1, ls=':', alpha=0.5))
            ax.text(neg_v.real*1.2, neg_v.imag*1.2, f"$-V_{{{['bn','cn','an'][i]}}}$", color=col, alpha=0.5)

            # Line Voltages (Thick Resultants)
            ax.annotate('', xy=(v_lines[i].real, v_lines[i].imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='-|>', color=col, lw=3))
            ax.text(v_lines[i].real*1.1, v_lines[i].imag*1.1, v_l_labels[i], color=col, weight='bold')

            # Parallelogram lines
            ax.plot([v_phs[i].real, v_lines[i].real], [v_phs[i].imag, v_lines[i].imag], color='grey', ls='--', lw=0.8, alpha=0.5)
            ax.plot([neg_v.real, v_lines[i].real], [neg_v.imag, v_lines[i].imag], color='grey', ls='--', lw=0.8, alpha=0.5)

        # Draw 30 degree Arc for Star
        arc = Arc((0,0), 80, 80, theta1=0, theta2=30, edgecolor='blue', ls=':')
        ax.add_patch(arc)
        ax.text(45, 15, "30°", color='blue', fontsize=10)

    else:
        ax.set_title("Delta (Δ) Connection\nLine Current shifts -30° | Voltages remain equal", pad=20)
        
        # Line Voltages (Vab, Vbc, Vca) - Fixed at 0, -120, 120
        v_l_labels = ["$V_{ab}$", "$V_{bc}$", "$V_{ca}$"]
        for i in range(3):
            ax.annotate('', xy=(v_phs[i].real, v_phs[i].imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='-|>', color=c_map[i], lw=2.5))
            ax.text(v_phs[i].real*1.1, v_phs[i].imag*1.1, v_l_labels[i], color=c_map[i], weight='bold')

        # Phase Currents (lab, lbc, lca)
        i_phs = [i_mag * np.exp(-1j*(i*r120 + phi)) for i in range(3)]
        # Line Currents (Ia, Ib, Ic)
        i_lines = [i_phs[0]-i_phs[2], i_phs[1]-i_phs[0], i_phs[2]-i_phs[1]]
        i_l_labels = ["$I_a$", "$I_b$", "$I_c$"]
        i_p_labels = ["$I_{ab}$", "$I_{bc}$", "$I_{ca}$"]

        for i in range(3):
            col = c_map[i]
            # Phase Current
            ax.annotate('', xy=(i_phs[i].real, i_phs[i].imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='->', color=col, lw=1.5))
            ax.text(i_phs[i].real*1.1, i_phs[i].imag*1.1, i_p_labels[i], color=col)

            # Negative Phase Current (Dotted)
            neg_i = -i_phs[(i-1)%3]
            ax.annotate('', xy=(neg_i.real, neg_i.imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='->', color=col, lw=1, ls=':', alpha=0.4))
            
            # Line Resultant Current
            ax.annotate('', xy=(i_lines[i].real, i_lines[i].imag), xytext=(0,0),
                        arrowprops=dict(arrowstyle='-|>', color=col, lw=2.5))
            ax.text(i_lines[i].real*1.1, i_lines[i].imag*1.1, i_l_labels[i], color=col, weight='bold')

            # Parallelogram
            ax.plot([i_phs[i].real, i_lines[i].real], [i_phs[i].imag, i_lines[i].imag], color='grey', ls='--', lw=0.8)
            ax.plot([neg_i.real, i_lines[i].real], [neg_i.imag, i_lines[i].imag], color='grey', ls='--', lw=0.8)

        # Draw Φ and 30 degree Arc for Delta
        arc_phi = Arc((0,0), 60, 60, theta1=-phi_deg, theta2=0, edgecolor='blue', ls=':')
        ax.add_patch(arc_phi)
        ax.text(35, -15, "Φ", color='blue')
        
        arc_30 = Arc((0,0), 100, 100, theta1=-phi_deg-30, theta2=-phi_deg, edgecolor='red', ls=':')
        ax.add_patch(arc_30)
        ax.text(50, -50, "30°", color='red')

# --- DISPLAY ---
col1, col2 = st.columns(2)
with col1:
    fig_star, ax_star = plt.subplots(figsize=(6,6))
    draw_phasor_diagram(ax_star, is_star=True)
    st.pyplot(fig_star)

with col2:
    fig_delta, ax_delta = plt.subplots(figsize=(6,6))
    draw_phasor_diagram(ax_delta, is_star=False)
    st.pyplot(fig_delta)

st.info("The diagram dynamically updates based on the Power Factor Angle (Φ) and magnitudes provided in the sidebar.")
