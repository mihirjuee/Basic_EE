import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Phasor Lab", layout="centered")

# --- VIEW TOGGLE ---
desktop = st.toggle("🖥️ Desktop Mode", value=False)
if desktop:
    st.set_page_config(layout="wide")

# --- HEADER ---
st.title("⚡ Three-Phase Phasor Visualization Lab")

# --- SIDEBAR ---
st.sidebar.header("🕹️ Controls")
v_mag = st.sidebar.slider("Voltage Magnitude", 50.0, 240.0, 150.0)
i_mag = st.sidebar.slider("Current Magnitude", 1.0, 100.0, 60.0)
phi_deg = st.sidebar.slider("Power Factor Angle (Φ°)", -90, 90, 30)

phi = np.deg2rad(phi_deg)
rad120 = np.deg2rad(120)

COL = ['#E63946', '#FFB703', '#1D3557']

# --- ANGLE DRAW ---
def draw_angle(ax, v1, v2, r, label, color):
    a1, a2 = np.angle(v1), np.angle(v2)
    theta = np.linspace(a1, a2, 60)

    ax.plot(r*np.cos(theta), r*np.sin(theta),
            linestyle=':', color=color, lw=1.5)

    mid = (a1 + a2)/2
    ax.text(r*np.cos(mid), r*np.sin(mid),
            label, color=color, fontsize=10, weight='bold')

# --- DELTA DRAW FUNCTION (TEXTBOOK PERFECT) ---
def draw_delta(ax, Vph, Iph, Iline):

    limit = max(v_mag, i_mag) * 2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    ax.axhline(0, lw=0.5, color='gray')
    ax.axvline(0, lw=0.5, color='gray')

    v_labels = ["Vab", "Vbc", "Vca"]
    iph_labels = ["Iab", "Ibc", "Ica"]
    il_labels = ["Ia", "Ib", "Ic"]

    for i in range(3):

        # --- COMPONENTS ---
        comp1 = Iph[i]                # Iab
        comp2 = -Iph[(i-1)%3]         # -Ica
        res = Iline[i]                # Ia

        # --- BASE VECTORS (PHASE CURRENTS) ---
        ax.annotate('', xy=(comp1.real, comp1.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->',
                                    color=COL[i], lw=2))
        ax.text(comp1.real*1.1, comp1.imag*1.1,
                iph_labels[i], color=COL[i])

        # --- NEGATIVE VECTOR ---
        ax.annotate('', xy=(comp2.real, comp2.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->',
                                    linestyle='--',
                                    color=COL[i], lw=1.5))
        ax.text(comp2.real*1.1, comp2.imag*1.1,
                f"-{iph_labels[(i-1)%3]}",
                color=COL[i], style='italic')

        # --- PARALLELOGRAM (FULL) ---
        p_end = comp1 + comp2

        ax.plot([comp1.real, p_end.real],
                [comp1.imag, p_end.imag],
                linestyle='--', color=COL[i], alpha=0.7)

        ax.plot([comp2.real, p_end.real],
                [comp2.imag, p_end.imag],
                linestyle='--', color=COL[i], alpha=0.7)

        # --- RESULTANT LINE CURRENT ---
        ax.annotate('', xy=(res.real, res.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>',
                                    color=COL[i], lw=3))
        ax.text(res.real*1.1, res.imag*1.1,
                il_labels[i], color=COL[i], weight='bold')

        # --- VOLTAGE (REFERENCE) ---
        ax.annotate('', xy=(Vph[i].real, Vph[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-',
                                    color='black', lw=1.5, alpha=0.5))
        ax.text(Vph[i].real*1.1, Vph[i].imag*1.1,
                v_labels[i], color='black', alpha=0.6)

    # --- ANGLES ---
    draw_angle(ax, Vph[0], Iline[0], v_mag*0.6, "Φ", "red")
    draw_angle(ax, Iph[0], Iline[0], v_mag*0.4, "30°", "blue")

    ax.set_title("Delta: Ia = Iab - Ica (30° lag)", fontsize=13, weight='bold')
    ax.set_aspect('equal')
    ax.axis('off')


# --- STAR DRAW (CLEAN) ---
def draw_star(ax, Vph, Vline, Iline):

    limit = max(v_mag, i_mag) * 2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    ax.axhline(0, lw=0.5, color='gray')
    ax.axvline(0, lw=0.5, color='gray')

    labels = ["Vab", "Vbc", "Vca"]

    for i in range(3):

        comp1 = Vph[i]
        comp2 = -Vph[(i+1)%3]
        res = Vline[i]

        # parallelogram
        p_end = comp1 + comp2

        ax.plot([comp1.real, p_end.real],
                [comp1.imag, p_end.imag],
                '--', color=COL[i])

        ax.plot([comp2.real, p_end.real],
                [comp2.imag, p_end.imag],
                '--', color=COL[i])

        # line voltage
        ax.annotate('', xy=(res.real, res.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>',
                                    color=COL[i], lw=3))

        ax.text(res.real*1.1, res.imag*1.1,
                labels[i], color=COL[i])

        # current
        ax.annotate('', xy=(Iline[i].real, Iline[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->',
                                    linestyle='--',
                                    color=COL[i], lw=2))

    draw_angle(ax, Vph[0], Vline[0], v_mag*0.4, "30°", "blue")
    draw_angle(ax, Vph[0], Iline[0], v_mag*0.6, "Φ", "red")

    ax.set_title("Star: Vline = √3 Vph (30° lead)", fontsize=13, weight='bold')
    ax.set_aspect('equal')
    ax.axis('off')


# --- CALCULATIONS ---
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
Vph = [Van, Vbn, Vcn]

# STAR
Vline_star = [Van-Vbn, Vbn-Vcn, Vcn-Van]
Iline_star = [
    i_mag*np.exp(-1j*(0+phi)),
    i_mag*np.exp(-1j*(rad120+phi)),
    i_mag*np.exp(1j*(rad120-phi))
]

# DELTA
Iph_delta = [
    i_mag*np.exp(-1j*phi),
    i_mag*np.exp(-1j*(rad120+phi)),
    i_mag*np.exp(1j*(rad120-phi))
]

Iline_delta = [
    Iph_delta[0] - Iph_delta[2],
    Iph_delta[1] - Iph_delta[0],
    Iph_delta[2] - Iph_delta[1]
]

# --- LAYOUT ---
if desktop:
    col1, col2 = st.columns(2)
else:
    col1 = st.container()
    col2 = st.container()

# --- STAR ---
with col1:
    st.subheader("⭐ Star Connection")
    fig1, ax1 = plt.subplots(figsize=(5,5))
    draw_star(ax1, Vph, Vline_star, Iline_star)
    st.pyplot(fig1)

# --- DELTA ---
with col2:
    st.subheader("🔺 Delta Connection")
    fig2, ax2 = plt.subplots(figsize=(5,5))
    draw_delta(ax2, Vph, Iph_delta, Iline_delta)
    st.pyplot(fig2)

# --- FOOTER ---
st.divider()
st.info("""
**Legend**
- Thick solid → Line quantities  
- Thin solid → Phase quantities  
- Dashed → Negative vectors  
- Dotted → Parallelogram construction  
- Angles → 30° relation & power factor Φ
""")
