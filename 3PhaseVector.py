import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="EE Phasor Lab", layout="centered")

# --- TOGGLE VIEW ---
mode = st.toggle("🖥️ Desktop Mode", value=False)
if mode:
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

# --- ANGLE DRAW FUNCTION ---
def draw_angle(ax, v1, v2, radius, label, color):
    a1 = np.angle(v1)
    a2 = np.angle(v2)

    theta = np.linspace(a1, a2, 50)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    ax.plot(x, y, linestyle=':', color=color, lw=1.5)

    mid = (a1 + a2) / 2
    ax.text(radius*np.cos(mid), radius*np.sin(mid),
            label, color=color, fontsize=10, weight='bold')

# --- DRAW FUNCTION ---
def draw_system(ax, Vph, Vline, Iline, title, is_star=True):
    limit = max(v_mag, i_mag) * 2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    ax.axhline(0, lw=0.5, color='gray')
    ax.axvline(0, lw=0.5, color='gray')

    v_labels = ["Vab", "Vbc", "Vca"]
    i_labels = ["Ia", "Ib", "Ic"]

    for i in range(3):

        if is_star:
            comp1 = Vph[i]
            comp2 = -Vph[(i+1)%3]
            res = Vline[i]
        else:
            comp1 = Iline[i]
            comp2 = -Iline[(i-1)%3]
            res = Iline[i]

        # --- PARALLELOGRAM ---
        ax.plot([0, comp1.real], [0, comp1.imag], ':', color=COL[i], alpha=0.3)
        ax.plot([0, comp2.real], [0, comp2.imag], ':', color=COL[i], alpha=0.3)

        ax.plot([comp1.real, res.real], [comp1.imag, res.imag],
                '--', color=COL[i], alpha=0.6)
        ax.plot([comp2.real, res.real], [comp2.imag, res.imag],
                '--', color=COL[i], alpha=0.6)

        # --- NEGATIVE VECTOR ---
        ax.annotate('', xy=(comp2.real, comp2.imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->',
                                    linestyle='--',
                                    color=COL[i], lw=1.5))

        # --- VOLTAGE VECTOR ---
        ax.annotate('', xy=(Vline[i].real, Vline[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='-|>',
                                    color=COL[i], lw=3))

        ax.text(Vline[i].real*1.1, Vline[i].imag*1.1,
                v_labels[i], color=COL[i], weight='bold')

        # --- CURRENT VECTOR ---
        ax.annotate('', xy=(Iline[i].real, Iline[i].imag), xytext=(0,0),
                    arrowprops=dict(arrowstyle='->',
                                    linestyle='--',
                                    color=COL[i], lw=2))

        ax.text(Iline[i].real*1.1, Iline[i].imag*1.1,
                i_labels[i], color=COL[i], style='italic')

    # --- ANGLES ---
    draw_angle(ax, Vph[0], Vline[0], v_mag*0.4, "30°", "blue")
    draw_angle(ax, Vph[0], Iline[0], v_mag*0.6, "Φ", "red")

    ax.set_title(title, fontsize=13, weight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

# --- CALCULATIONS ---
Van = v_mag * np.exp(1j * 0)
Vbn = v_mag * np.exp(-1j * rad120)
Vcn = v_mag * np.exp(1j * rad120)
Vph = [Van, Vbn, Vcn]

# STAR
Vline_star = [Van - Vbn, Vbn - Vcn, Vcn - Van]
Iline_star = [
    i_mag * np.exp(-1j*(0 + phi)),
    i_mag * np.exp(-1j*(rad120 + phi)),
    i_mag * np.exp(1j*(rad120 - phi))
]

# DELTA
Iph_delta = [
    i_mag * np.exp(-1j*phi),
    i_mag * np.exp(-1j*(rad120 + phi)),
    i_mag * np.exp(1j*(rad120 - phi))
]

Iline_delta = [
    Iph_delta[0] - Iph_delta[2],
    Iph_delta[1] - Iph_delta[0],
    Iph_delta[2] - Iph_delta[1]
]

# --- LAYOUT ---
if mode:
    col1, col2 = st.columns(2)
else:
    col1 = st.container()
    col2 = st.container()

# --- STAR ---
with col1:
    st.subheader("⭐ Star (Y) Connection")
    fig1, ax1 = plt.subplots(figsize=(5,5))
    draw_system(ax1, Vph, Vline_star, Iline_star,
                "Line Voltage leads by 30°")
    st.pyplot(fig1)

# --- DELTA ---
with col2:
    st.subheader("🔺 Delta (Δ) Connection")
    fig2, ax2 = plt.subplots(figsize=(5,5))
    draw_system(ax2, Vph, Iline_delta, Iph_delta,
                "Line Current lags by 30°", is_star=False)
    st.pyplot(fig2)

# --- FOOTER ---
st.divider()
st.info("""
**Legend:**
- Thick Solid → Line Voltage  
- Dashed → Line Current  
- Dotted → Construction (Parallelogram)  
- Arc → Phase relationships (30°, Φ)
""")
