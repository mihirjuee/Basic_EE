import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="3-Phase Phasor Lab", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: black; }
    div[data-testid="stMetricValue"] { color: #d62728; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        st.image("logo.png", width=80)
    except:
        st.write("⚡ **LOGO**")

with col_title:
    st.title("Comprehensive 3-Phase Phase & Line Vectors")

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
    limit = max(np.abs(l_vecs)) * 1.5
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    
    # Draw Axes
    ax.axhline(0, color='black', lw=1, alpha=0.3)
    ax.axvline(0, color='black', lw=1, alpha=0.3)
    
    # Red, Yellow, Blue standard EE colors
    colors = ['#d62728', '#bcbd22', '#1f77b4'] 
    
    # 1. Draw Phase Vectors (Reference)
    for v, col, lab in zip(p_vecs, colors, p_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.5, alpha=0.7))
        ax.text(v.real*1.15, v.imag*1.15, lab, color=col, fontweight='bold')

    # 2. Draw ALL THREE Parallelograms (Vector Subtraction)
    # The pairs used are determined by the definition of Line vector
    # STAR: V_l1_l2 = V_ph1 - V_ph2
    # DELTA: I_l1 = I_ph_branch1 - I_ph_branch2 (at the node)
    
    if is_voltage:
        # Pairs for Star: Vab = Van - Vbn | Vbc = Vbn - Vcn | Vca = Vcn - Van
        # The secondary vector is the negative of the phase after it
        s_vec_pairs = [p_vecs[0], p_vecs[1], p_vecs[2]] # Van, Vbn, Vcn
        n_vec_pairs = [-p_vecs[1], -p_vecs[2], -p_vecs[0]] # -Vbn, -Vcn, -Van
    else:
        # Pairs for Delta: Ia = Iab - Ica | Ib = Ibc - Iab | Ic = Ica - Ibc
        # The secondary vector is the negative of the phase branch BEFORE it
        s_vec_pairs = [p_vecs[0], p_vecs[1], p_vecs[2]] # Iab, Ibc, Ica
        n_vec_pairs = [-p_vecs[2], -p_vecs[0], -p_vecs[1]] # -Ica, -Iab, -Ibc

    for s_vec, n_vec, l_vec in zip(s_vec_pairs, n_vec_pairs, l_vecs):
        # Draw the dotted construction lines
        ax.plot([s_vec.real, l_vec.real], [s_vec.imag, l_vec.imag], 'k--', lw=0.8, alpha=0.3)
        ax.plot([n_vec.real, l_vec.real], [n_vec.imag, l_vec.imag], 'k--', lw=0.8, alpha=0.3)
        # Draw the reference negative vector (invisible body, just the tip reference)
        ax.plot([0, n_vec.real], [0, n_vec.imag], 'k:', lw=1, alpha=0.3) 

    # 3. Draw Line Vectors (Resultant)
    for v, col, lab in zip(l_vecs, colors, l_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=3.5, mutation_scale=20))
        ax.text(v.real*1.1, v.imag*1.1, lab, color=col, fontweight='extra bold', fontsize=12)

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# --- CALCULATIONS ---
# Star Voltage (V_line = V_ph1 - V_ph2)
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
Vab, Vbc, Vca = Van-Vbn, Vbn-Vcn, Vcn-Van

# Delta Current (I_line = I_branch1 - I_branch2 meeting at node)
Iab = i_mag * np.exp(-1j * phi)
Ibc = i_mag * np.exp(-1j * (rad120 + phi))
Ica = i_mag * np.exp(1j * (rad120 - phi))
Ia, Ib, Ic = Iab-Ica, Ibc-Iab, Ica-Ibc

# --- UI LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Star: Phase vs Line Voltage")
    st.write(rf"$|V_{{L}}| = \sqrt{3}|V_{{ph}}| \angle 30^\circ$")
    st.info(f"Magnitude: {v_mag:.1f}V (Phase) → {np.abs(Vab):.1f}V (Line)")
    
    fig1, ax1 = plt.subplots(figsize=(6,6), facecolor='white')
    draw_detailed_phasor(ax1, [Van, Vbn, Vcn], [Vab, Vbc, Vca], 
                        ["Van", "Vbn", "Vcn"], ["Vab", "Vbc", "Vca"], 
                        "Voltage Relations (Star)", "V", is_voltage=True)
    st.pyplot(fig1)

with col2:
    st.subheader("🔺 Delta: Phase vs Line Current")
    st.write(rf"$|I_{{L}}| = \sqrt{3}|I_{{ph}}| \angle -30^\circ$")
    st.info(f"Magnitude: {i_mag:.1f}A (Branch) → {np.abs(Ia):.1f}A (Line)")
    
    fig2, ax2 = plt.subplots(figsize=(6,6), facecolor='white')
    draw_detailed_phasor(ax2, [Iab, Ibc, Ica], [Ia, Ib, Ic], 
                        ["Iab", "Ibc", "Ica"], ["Ia", "Ib", "Ic"], 
                        "Current Relations (Delta)", "A", is_voltage=False)
    st.pyplot(fig2)

st.divider()
with st.expander("📖 Interpretation Guide"):
    st.markdown("""
The dotted grey lines form the parallelograms defined by vector subtraction. For each of the three line vectors (Red, Yellow, Blue), you can observe how the line vector is derived by connecting the origin to the opposite corner of the parallelogram.
    
1.  **Star (Voltage):** The parallelogram for $V_{ab}$ (Red) is defined by $\vec{V}_{an}$ and $-\vec{V}_{bn}$.
2.  **Delta (Current):** The parallelogram for $I_{a}$ (Red) is defined by $\vec{I}_{ab}$ and $-\vec{I}_{ca}$.
    """)
