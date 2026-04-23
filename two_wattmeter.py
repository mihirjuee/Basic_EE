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
    
    # R-Phase: CC in series, PC connected to Y
    d += (R := elm.Dot().label("R", 'left'))
    d += (CC1 := elm.Inductor(loops=3).label("CC1", 'top'))
    d += (P1 := elm.Dot())
    d += (PC1 := elm.Resistor().label("PC1", 'right').down().at(P1.start))
    d += (Y_node := elm.Dot().label("Y", 'right'))
    d += (LoadR := elm.Resistor().label("Zr").right().at(P1.end))
    
    # Y-Phase: Direct line
    d.move(0, -3)
    d += elm.Dot().label("Y", 'left')
    d += elm.Line().length(4)
    d += (LoadY := elm.Resistor().label("Zy").up(3).at(Y_node))
    
    # B-Phase: CC in series, PC connected to Y
    d.move(0, -3)
    d += (B := elm.Dot().label("B", 'left'))
    d += (CC2 := elm.Inductor(loops=3).label("CC2", 'top'))
    d += (P2 := elm.Dot())
    d += (PC2 := elm.Resistor().label("PC2", 'right').up().at(P2.start))
    d += (LoadB := elm.Resistor().label("Zb").right().at(P2.end))
    
    d.draw()

st.title("⚡ Two-Wattmeter Method Circuit")
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')
draw_textbook_circuit(ax)
st.pyplot(fig)
plt.close(fig)
