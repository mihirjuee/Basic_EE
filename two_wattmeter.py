import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Two Wattmeter Method", page_icon="logo.png", layout="wide")

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

import schemdraw
import schemdraw.elements as elm

def draw_textbook_circuit(ax):
    d = schemdraw.Drawing(canvas=ax)
    
    # R-Phase

    d += elm.Dot().label("R", 'left')
    d.push()
    d += elm.Oval(width=1.2, height=1.2).label("W1")
    d += (CC1 := elm.Inductor().label("CC1", loc="top"))
    #d += elm.Line().right(0.5)
    d.push()
    d += elm.Line().down(1)
    d += elm.Resistor().label("PC1", 'right').left(1.5)
    d += elm.Line().down(2)
    d += elm.Dot()
    d.pop()
    d += elm.Line().right(3.5)
    d += elm.Line().down(0.45)
    
    d.pop()
    
    #Y-PHASE
    d.move(0, -3)
    d.push()
    d += (Y_line := elm.Dot().label("Y", 'left'))
    d += elm.Line().right(2)
    d += elm.Resistor().label("ZY")
    d.push()
    #d += elm.Line().theta(60)
    #d += elm.Rect(width=2, height=1).label("ZR") 
    d += elm.Resistor().label("ZR").theta(60)
    d.pop()
    d += elm.Resistor().label("ZB").theta(-60)
    d.pop()
    
    #B-PHASE
    d.move(0, -3)
    d += (Y_line := elm.Dot().label("B", 'left'))
    d += (CC2 := elm.Inductor(loops=3).label("CC2", 'top'))
    d.push()
    d += elm.Line().up(1)
    d += elm.Resistor().label("PC2", 'right').left(1.5)
    d += elm.Line().up(2)
    d.pop()
    d += elm.Line().right(3.5)
    d += elm.Line().up(0.5)

    
    d.draw()

st.title("⚡ Two-Wattmeter Method Circuit")
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')
draw_textbook_circuit(ax)
st.pyplot(fig)
plt.close(fig)
