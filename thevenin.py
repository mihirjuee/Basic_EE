import streamlit as st
import pandas as pd
import numpy as np
import schemdraw
import schemdraw.elements as elm
import matplotlib.pyplot as plt
import time

# --- Page Config ---
st.set_page_config(page_title="Thevenin Virtual Lab", layout="wide")

st.title("⚡ Thevenin's Theorem Virtual Lab")
st.markdown("Interactively verify Thevenin’s Theorem with visualization and animation.")

# --- Sidebar Controls ---
st.sidebar.header("🔧 Controls")

mode = st.sidebar.radio("Select Circuit View", ["Original Circuit", "Thevenin Equivalent"])

V_s = st.sidebar.slider("Source Voltage (Vs) [V]", 1, 100, 12)
R1 = st.sidebar.slider("R1 [Ω]", 10, 1000, 100)
R2 = st.sidebar.slider("R2 [Ω]", 10, 1000, 200)
R3 = st.sidebar.slider("R3 [Ω]", 10, 1000, 150)
RL = st.sidebar.slider("Load RL [Ω]", 10, 1000, 50)

animate = st.sidebar.checkbox("⚡ Animate Current Flow")

# --- Calculations ---
V_th = V_s * (R2 / (R1 + R2))
R_parallel = (R1 * R2) / (R1 + R2)
R_th = R_parallel + R3
I_L = V_th / (R_th + RL)

# --- Circuit Drawing Functions ---
def draw_original():
    d = schemdraw.Drawing()

    d += elm.SourceV().label(f'{V_s}V')
    d += elm.Resistor().right().label(f'R1\n{R1}Ω')
    d += elm.Dot()

    d.push()
    d += elm.Resistor().down().label(f'R2\n{R2}Ω')
    d += elm.Ground()
    d.pop()

    d += elm.Resistor().right().label(f'R3\n{R3}Ω')
    d += elm.Dot()

    d.push()
    d += elm.Resistor().down().label(f'RL\n{RL}Ω')
    d += elm.Ground()
    d.pop()

    return d

def draw_thevenin():
    d = schemdraw.Drawing()

    d += elm.SourceV().label(f'Vth\n{V_th:.2f}V')
    d += elm.Resistor().right().label(f'Rth\n{R_th:.2f}Ω')
    d += elm.Dot()

    d.push()
    d += elm.Resistor().down().label(f'RL\n{RL}Ω')
    d += elm.Ground()
    d.pop()

    return d

# --- Layout ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("🔌 Circuit View")

    if mode == "Original Circuit":
        d = draw_original()
    else:
        d = draw_thevenin()

import io

fig = d.draw()

import io

with col1:
    st.subheader("🔌 Circuit View")

    if mode == "Original Circuit":
        d = draw_original()
    else:
        d = draw_thevenin()

    # ✅ Save directly to PNG buffer (NO matplotlib dependency)
    buf = io.BytesIO()
    d.save(buf)   # <-- KEY FIX
    buf.seek(0)

    st.image(buf, use_container_width=True)

st.image(buf)

with col2:
    st.subheader("📊 Results")

    st.metric("Vth", f"{V_th:.2f} V")
    st.metric("Rth", f"{R_th:.2f} Ω")
    st.metric("Load Current", f"{I_L*1000:.2f} mA")

    st.progress(min(I_L * 10, 1.0))

# --- Animation Section ---
st.divider()
st.subheader("⚡ Current Flow Animation")

placeholder = st.empty()

if animate:
    x = np.linspace(0, 2*np.pi, 200)

    for i in range(50):
        fig, ax = plt.subplots()

        y = np.sin(x + i * 0.3)
        ax.plot(x, y)

        ax.set_title("AC Current Flow Representation")
        ax.set_xlabel("Time")
        ax.set_ylabel("Current")

        placeholder.pyplot(fig)
        plt.close(fig)   # ✅ Prevent memory crash

        time.sleep(0.05)

else:
    st.info("Enable animation from sidebar to visualize current flow.")

# --- Table ---
st.divider()
st.subheader("📋 Verification Table")

data = {
    "Parameter": ["Vth", "Rth", "RL", "Load Current (mA)"],
    "Value": [f"{V_th:.2f} V", f"{R_th:.2f} Ω", f"{RL} Ω", f"{I_L*1000:.2f} mA"]
}

st.table(pd.DataFrame(data))

# --- Theory ---
st.divider()
st.markdown("### 💡 Theory")

st.write("""
Any linear circuit can be replaced by an equivalent voltage source (Vth) 
in series with a resistance (Rth). This app demonstrates that both circuits 
produce the same load current.
""")
