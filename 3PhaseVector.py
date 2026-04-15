import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="3-Phase Phasor Lab", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #000000; }
    p, h1, h2, h3, span { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("⚡ Unified 3-Phase Phasor Analysis")
st.markdown("Visualizing the relationship between **Phase** and **Line** vectors as shown in your reference diagram.")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Controls")
v_mag = st.sidebar.slider("Voltage Magnitude (V_ph)", 50.0, 240.0, 150.0)
i_mag = st.sidebar.slider("Current Magnitude (I_ph)", 1.0, 100.0, 80.0)
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 30)

# --- MATH CONSTANTS ---
rad120 = np.deg2rad(120)
phi = np.deg2rad(phi_deg)
# Colors: Red (R), Yellow (Y), Blue (B) - matching standard labeling
colors = ['#E63946', '#FFB703', '#1D3557'] 

def draw_phasor_diagram(ax, v_vecs, i_ph_vecs, i_line_vecs, title, is_star=True):
    ax.set_facecolor('white')
    limit = max(v_mag, i_mag * 2) * 1.2
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    ax.axhline(0, color='black', lw=0.5, alpha=0.3)
    ax.axvline(0, color='black', lw=0.5, alpha=0.3)

    v_labels = ["V_RY", "V_YB", "V_BR"]
    i_ph_labels = ["I_R", "I_Y", "I_B"]
    i_line_labels = ["I_1", "I_2", "I_3"]

    for i in range(3):
        # 1. DRAW VOLTAGE VECTORS (Solid)
        ax.annotate('', xy=(v_vecs[i].real, v_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=colors[i], lw=2.5))
        ax.text(v_vecs[i].real*1.1, v_vecs[i].imag*1.1, v_labels[i], color=colors[i], fontweight='bold')

        # 2. PARALLELOGRAM FOR LINE CURRENT (Only for Delta)
        if not is_star:
            # I1 = IR - IB (Reference to your image (a) and (b))
            curr_ph = i_ph_vecs[i]
            prev_ph_neg = -i_ph_vecs[(i-1)%3]
            line_res = i_line_vecs[i]
            
            # Draw parallelogram dotted lines
            ax.plot([curr_ph.real, line_res.real], [curr_ph.imag, line_res.imag], 'k--', lw=0.8, alpha=0.2)
            ax.plot([prev_ph_neg.real, line_res.real], [prev_ph_neg.imag, line_res.imag], 'k--', lw=0.8, alpha=0.2)
            ax.plot([0, prev_ph_neg.real], [0, prev_ph_neg.imag], 'k:', lw=1, alpha=0.1)

        # 3. DRAW PHASE CURRENTS (Thin Solid)
        ax.annotate('', xy=(i_ph_vecs[i].real, i_ph_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=1, alpha=0.7))
        ax.text(i_ph_vecs[i].real*0.8, i_ph_vecs[i].imag*0.8, i_ph_labels[i], color=colors[i], fontsize=9)

        # 4. DRAW LINE CURRENTS (Thick Dashed)
        ax.annotate('', xy=(i_line_vecs[i].real, i_line_vecs[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=colors[i], lw=2, ls='--'))
        ax.text(i_line_vecs[i].real*1.15, i_line_vecs[i].imag*1.15, i_line_labels[i], color=colors[i], fontstyle='italic')

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Voltages (Reference V_RY at 0 degrees as per image b)
V_RY = v_mag * np.exp(1j * 0)
V_YB = v_mag * np.exp(-1j * rad120)
V_BR = v_mag * np.exp(1j * rad120)
v_vecs = [V_RY, V_YB, V_BR]

# Phase Currents (lagging voltage by phi)
I_R = i_mag * np.exp(-1j * phi)
I_Y = i_mag * np.exp(-1j * (rad120 + phi))
I_B = i_mag * np.exp(1j * (rad120 - phi))
i_ph_vecs = [I_R, I_Y, I_B]

# Line Currents for Delta (I1 = IR - IB, I2 = IY - IR, I3 = IB - IY)
I1, I2, I3 = I_R - I_B, I_Y - I_R, I_B - I_Y
i_line_delta = [I1, I2, I3]

# Line Currents for Star (Line = Phase)
i_line_star = i_ph_vecs

# --- UI LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Delta Configuration (Δ)")
    st.write("Matches your provided diagram: $I_{Line}$ derived from $I_{Phase}$ subtraction.")
    fig1, ax1 = plt.subplots(figsize=(6,6))
    draw_phasor_diagram(ax1, v_vecs, i_ph_vecs, i_line_delta, "Delta: Line Current Formation", is_star=False)
    st.pyplot(fig1)

with col2:
    st.subheader("Star Configuration (Y)")
    st.write("Currents overlap while Line Voltages (not shown for clarity) would shift.")
    fig2, ax2 = plt.subplots(figsize=(6,6))
    draw_phasor_diagram(ax2, v_vecs, i_ph_vecs, i_line_star, "Star: Line & Phase Current", is_star=True)
    st.pyplot(fig2)

st.divider()
st.markdown("""
### 🔍 Key takeaways from your Phasor Diagram:
- **Phase Current ($I_R, I_Y, I_B$):** Lags the respective phase voltage by angle $\phi$.
- **Line Current ($I_1, I_2, I_3$):** In Delta, the line current is the vector difference. As seen in your image (b), $I_1$ is the resultant of $I_R$ and $-I_B$.
- **30° Shift:** Note that the line current resultant is shifted by $30^\circ$ relative to the phase current.
""")
