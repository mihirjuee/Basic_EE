import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Page Config
st.set_page_config(page_title="Superposition Theorem", layout="wide")

def draw_circuit(v1, v2, r1, r2, r3, mode="Full"):
    """Draws a schematic representation of the circuit using Matplotlib."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 6)
    
    # Coordinates for components
    # Left Branch (V1 & R1)
    ax.plot([0, 0], [0, 2], 'k-')  # Wire
    if mode == "V2_Only":
        ax.plot([0, 0], [2, 3], 'b--', label="Short Circuit (V1)")
    else:
        ax.add_patch(plt.Circle((0, 2.5), 0.5, color='orange', fill=False, lw=2))
        ax.text(-1.5, 2.3, f"{v1}V", fontsize=12, fontweight='bold')
    
    ax.plot([0, 0], [3, 5], 'k-')  # Wire
    ax.plot([0, 2], [5, 5], 'k-')  # Wire to R1
    # R1 Rectangle
    ax.add_patch(plt.Rectangle((2, 4.75), 2, 0.5, color='gray', alpha=0.3))
    ax.text(2.5, 5.3, f"R1: {r1}Ω", fontsize=10)
    ax.plot([4, 5], [5, 5], 'k-')

    # Middle Branch (R3 - Load)
    ax.plot([5, 5], [5, 4], 'k-')
    ax.add_patch(plt.Rectangle((4.75, 2), 0.5, 2, color='red', alpha=0.3))
    ax.text(5.6, 2.8, f"R3: {r3}Ω\n(LOAD)", fontsize=10, color='red')
    ax.plot([5, 5], [2, 0], 'k-')

    # Right Branch (V2 & R2)
    ax.plot([5, 6], [5, 5], 'k-')
    ax.add_patch(plt.Rectangle((6, 4.75), 2, 0.5, color='gray', alpha=0.3))
    ax.text(6.5, 5.3, f"R2: {r2}Ω", fontsize=10)
    ax.plot([8, 10], [5, 5], 'k-')
    ax.plot([10, 10], [5, 3], 'k-')
    
    if mode == "V1_Only":
        ax.plot([10, 10], [2, 3], 'b--', label="Short Circuit (V2)")
    else:
        ax.add_patch(plt.Circle((10, 2.5), 0.5, color='orange', fill=False, lw=2))
        ax.text(10.7, 2.3, f"{v2}V", fontsize=12, fontweight='bold')
    
    ax.plot([10, 10], [2, 0], 'k-')
    ax.plot([10, 0], [0, 0], 'k-') # Bottom rail

    ax.set_title(f"Circuit Diagram: {mode} Mode", fontsize=14)
    ax.axis('off')
    return fig

# --- UI Setup ---
st.title("🔌 Interactive Superposition Solver")
st.sidebar.header("Configure Components")

V1 = st.sidebar.slider("Voltage V1 (Volts)", 0, 100, 24)
V2 = st.sidebar.slider("Voltage V2 (Volts)", 0, 100, 12)
R1 = st.sidebar.number_input("R1 (Ω)", value=10.0)
R2 = st.sidebar.number_input("R2 (Ω)", value=20.0)
R3 = st.sidebar.number_input("R3 (Load Ω)", value=5.0)

# --- Calculations ---
# Step 1: V1 Only
req1 = R1 + (R2 * R3 / (R2 + R3))
i_total1 = V1 / req1
i_load_v1 = i_total1 * (R2 / (R2 + R3))

# Step 2: V2 Only
req2 = R2 + (R1 * R3 / (R1 + R3))
i_total2 = V2 / req2
i_load_v2 = i_total2 * (R1 / (R1 + R3))

total_i = i_load_v1 + i_load_v2

# --- App Tabs ---
tab1, tab2, tab3 = st.tabs(["Step 1: V1 Active", "Step 2: V2 Active", "Final Summary"])

with tab1:
    st.subheader("Case 1: V1 is ON, V2 is Shorted")
    st.pyplot(draw_circuit(V1, V2, R1, R2, R3, mode="V1_Only"))
    st.metric("Contribution to Load", f"{i_load_v1:.4f} A")
    st.latex(r"I_{R3(V1)} = \frac{V_1}{R_1 + (R_2 || R_3)} \times \frac{R_2}{R_2 + R_3}")

with tab2:
    st.subheader("Case 2: V2 is ON, V1 is Shorted")
    st.pyplot(draw_circuit(V1, V2, R1, R2, R3, mode="V2_Only"))
    st.metric("Contribution to Load", f"{i_load_v2:.4f} A")
    st.latex(r"I_{R3(V2)} = \frac{V_2}{R_2 + (R_1 || R_3)} \times \frac{R_1}{R_1 + R_3}")

with tab3:
    st.header("Results Summary")
    st.pyplot(draw_circuit(V1, V2, R1, R2, R3, mode="Full"))
    
    c1, c2, c3 = st.columns(3)
    c1.write(f"**From V1:** {i_load_v1:.4f} A")
    c2.write(f"**From V2:** {i_load_v2:.4f} A")
    c3.success(f"**Total I:** {total_i:.4f} A")
    
    st.progress(min(abs(total_i/10), 1.0)) # Visual current flow indicator
