import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Phasor Lab Pro", layout="wide")

# --- CUSTOM CSS (Forces white background style) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #000000; }
    p, h1, h2, h3, span { color: #000000 !important; }
    .stMetric { border: 1px solid #eeeeee; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & LOGO ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    try:
        # Assumes logo.png is in the same directory
        st.image("logo.png", width=100)
    except:
        st.markdown("### ⚡ **EE-LAB**")

with col_title:
    st.title("3-Phase Vector Analysis: Star & Delta")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Controls")
v_mag = st.sidebar.slider("Voltage Magnitude (V_ph)", 50.0, 240.0, 120.0)
i_mag = st.sidebar.slider("Current Magnitude (I_ph)", 1.0, 20.0, 10.0)
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 30)

# --- MATHEMATICAL CONSTANTS ---
rad120 = np.deg2rad(120)
phi = np.deg2rad(phi_deg)

# --- PLOTTING LOGIC ---
def draw_phasors(ax, p_vecs, l_vecs, p_labels, l_labels, title, is_voltage=True):
    ax.set_facecolor('white')
    # Set limits based on Line Voltage/Current (~1.732 * Phase)
    limit = max(np.abs(l_vecs)) * 1.5
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit)
    
    # Standard IEEE Phase Colors
    colors = ['#E63946', '#FFB703', '#1D3557'] # Red, Yellow/Gold, Blue
    
    # Draw Origin Axes
    ax.axhline(0, color='black', lw=0.8, alpha=0.2)
    ax.axvline(0, color='black', lw=0.8, alpha=0.2)

    # 1. Draw ALL THREE Parallelogram Constructions
    for i in range(3):
        p_vec = p_vecs[i]
        # In Star: Vab = Van - Vbn. In Delta: Ia = Iab - Ica
        # We need the "negative" vector of the other phase to show subtraction
        if is_voltage:
            neg_vec = -p_vecs[(i + 1) % 3] # -Vbn, -Vcn, -Van
        else:
            neg_vec = -p_vecs[(i - 1) % 3] # -Ica, -Iab, -Ibc
        
        resultant = l_vecs[i]
        
        # Dotted lines connecting the tips
        ax.plot([p_vec.real, resultant.real], [p_vec.imag, resultant.imag], 
                ls='--', color='gray', lw=1, alpha=0.5)
        ax.plot([neg_vec.real, resultant.real], [neg_vec.imag, resultant.imag], 
                ls='--', color='gray', lw=1, alpha=0.5)
        # Optional: draw the negative vector reference line
        ax.plot([0, neg_vec.real], [0, neg_vec.imag], 
                ls=':', color='gray', lw=1, alpha=0.3)

    # 2. Draw Phase Vectors (Thinner)
    for v, col, lab in zip(p_vecs, colors, p_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->', color=col, lw=2, alpha=0.8))
        ax.text(v.real*1.1, v.imag*1.1, lab, color=col, fontweight='bold')

    # 3. Draw Line Vectors (Thicker)
    for v, col, lab in zip(l_vecs, colors, l_labels):
        ax.annotate('', xy=(v.real, v.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>', color=col, lw=4, mutation_scale=20))
        ax.text(v.real*1.15, v.imag*1.15, lab, color=col, fontweight='extra bold', fontsize=12)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
# Star Voltages: Van (Ref), Vbn (-120), Vcn (+120)
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
Vab, Vbc, Vca = Van-Vbn, Vbn-Vcn, Vcn-Van

# Delta Currents: Iab (Ref - phi), Ibc, Ica
Iab = i_mag * np.exp(-1j * phi)
Ibc = i_mag * np.exp(-1j * (rad120 + phi))
Ica = i_mag * np.exp(1j * (rad120 - phi))
Ia, Ib, Ic = Iab-Ica, Ibc-Iab, Ica-Ibc

# --- DISPLAY UI ---
tab1, tab2 = st.tabs(["📊 Phasor Visualizer", "📖 Theory & Calculations"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Star Configuration")
        st.markdown("Line Voltage leads Phase Voltage by **30°**")
        fig_star, ax_star = plt.subplots(figsize=(7,7))
        draw_phasors(ax_star, [Van, Vbn, Vcn], [Vab, Vbc, Vca], 
                     ["Van", "Vbn", "Vcn"], ["Vab", "Vbc", "Vca"], 
                     "Voltage: Line vs Phase (Y)", is_voltage=True)
        st.pyplot(fig_star)
        plt.close(fig_star)

    with col2:
        st.subheader("🔺 Delta Configuration")
        st.markdown("Line Current lags Phase Current by **30°**")
        fig_delta, ax_delta = plt.subplots(figsize=(7,7))
        draw_phasors(ax_delta, [Iab, Ibc, Ica], [Ia, Ib, Ic], 
                     ["Iab", "Ibc", "Ica"], ["Ia", "Ib", "Ic"], 
                     "Current: Line vs Phase (Δ)", is_voltage=False)
        st.pyplot(fig_delta)
        plt.close(fig_delta)

with tab2:
    st.header("Mathematical Proofs")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Star Voltage (Line)")
        st.latex(r"V_{ab} = V_{an} - V_{bn} = \sqrt{3}V_{ph} \angle 30^\circ")
        st.metric("Line Voltage Resultant", f"{np.abs(Vab):.2f} V")
    with c2:
        st.write("### Delta Current (Line)")
        st.latex(r"I_{a} = I_{ab} - I_{ca} = \sqrt{3}I_{ph} \angle -30^\circ")
        st.metric("Line Current Resultant", f"{np.abs(Ia):.2f} A")

st.success("Interactive Simulator Ready. Adjust parameters in the sidebar to see vector transformations.")
