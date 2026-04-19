import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Two Wattmeter Method", page_icon="⚡", layout="wide")

# --- CALCULATIONS ---
V_supply = st.sidebar.slider("Line Voltage (V)", 100, 440, 400)
V_rated = st.sidebar.slider("Rated Voltage (V)", 200, 440, 400)
I_rated = st.sidebar.slider("Rated Current (A)", 1, 50, 10)
P_rated = st.sidebar.slider("Rated Power (kW)", 1.0, 50.0, 5.0)

Z = (V_rated / np.sqrt(3)) / I_rated
I_actual = (V_supply / np.sqrt(3)) / Z
pf = np.clip((P_rated * 1000) / (np.sqrt(3) * V_rated * I_rated), 0, 1)
phi = np.arccos(pf)
W1 = (V_supply * I_actual) * np.cos(np.radians(30) - phi)
W2 = (V_supply * I_actual) * np.cos(np.radians(30) + phi)

# --- IMPROVED TEXTBOOK CIRCUIT ---
def draw_textbook_circuit(ax):
    d = schemdraw.Drawing(canvas=ax)
    
    # Lines
    d += (L1 := elm.Line().length(4).label("R", 'left'))
    d += (L2 := elm.Line().up(2).at(L1.start))
    d += (L3 := elm.Line().down(2).at(L1.start))
    
    # Wattmeter 1 (R-Y)
    d += elm.CurrentComp(loops=3).at(L1.end).label("CC1", 'bottom')
    d += (P1 := elm.Line().right(2))
    d += elm.Resistor().down(2).label("Zr")
    d += elm.Line().left(2)
    d += elm.Line().up(2).at(P1.end).label("PC1", 'right').dot()
    d += elm.Voltmeter().up(2)
    
    # Wattmeter 2 (B-Y)
    d.move(-4, -4)
    d += (LB := elm.Line().right(4).label("B", 'left'))
    d += elm.CurrentComp(loops=3).at(LB.end).label("CC2", 'bottom')
    d += (P2 := elm.Line().right(2))
    d += elm.Resistor().down(2).label("Zb")
    d += elm.Line().left(2)
    d += elm.Line().up(2).at(P2.end).label("PC2", 'right').dot()
    d += elm.Voltmeter().up(2)

    d.draw()

st.title("⚡ Two-Wattmeter Method")
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')
draw_textbook_circuit(ax)
st.pyplot(fig)
plt.close(fig)
