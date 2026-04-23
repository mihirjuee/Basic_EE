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

# Electrical Math
Z = (V_rated / np.sqrt(3)) / I_rated
I_actual = (V_supply / np.sqrt(3)) / Z
pf = np.clip((P_rated * 1000) / (np.sqrt(3) * V_rated * I_rated), 0, 1)
phi = np.arccos(pf)
W1 = (V_supply * I_actual) * np.cos(np.radians(30) - phi)
W2 = (V_supply * I_actual) * np.cos(np.radians(30) + phi)

# --- TEXTBOOK CIRCUIT DIAGRAM ---
def draw_textbook_circuit(ax):
    d = schemdraw.Drawing(canvas=ax)
    
    # R-Phase (Wattmeter 1)
    d += elm.Dot().label("R", 'left')
    d += (L1 := elm.Inductor(loops=3).label("CC1", 'bottom'))
    d += (P1 := elm.Line().right(2))
    d += elm.Line().at(P1.end).up(2).label("PC1", 'right')
    d += elm.Resistor().label("Zr").down(2)
    d += elm.Line().left(2)
   
    
    # Y-Phase (Common)
    d.move(0, -4)
    d += elm.Dot().label("Y", 'left')
    d += elm.Line().right(2)
    d += elm.Resistor().label("Zy").down(2)
    
    # B-Phase (Wattmeter 2)
    d.move(0, 2)
    d += elm.Dot().label("B", 'left')
    d += (L2 := elm.Inductor(loops=3).label("CC2", 'bottom'))
    d += (P2 := elm.Line().right(2))
    d += elm.Resistor().label("Zb").down(2)
    d += elm.Line().left(2)
    d += elm.Line().at(P2.end).up(2).label("PC2", 'right')
    
    d.draw()

st.title("⚡ Two-Wattmeter Method Circuit")
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')
draw_textbook_circuit(ax)
st.pyplot(fig)
plt.close(fig)
