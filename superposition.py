import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Page Setup
st.set_page_config(page_title="Superposition Theorem",page_icon="logo.png", layout="wide")

def draw_schematic(v1, v2, r1, r2, r3, active_source="Both"):
    """Draws the circuit with polarity and source status."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 6)
    
    # 1. LEFT BRANCH (V1 & R1)
    # Voltage Source V1
    if active_source == "V2":
        ax.plot([0, 0], [1.5, 3.5], 'b--', lw=2, label="Short Circuit") # Shorted
    else:
        circle1 = plt.Circle((0, 2.5), 0.5, color='black', fill=False, lw=2)
        ax.add_patch(circle1)
        ax.text(-0.15, 2.6, "+", fontsize=15, fontweight='bold')
        ax.text(-0.15, 2.1, "-", fontsize=15, fontweight='bold')
        ax.text(-1.5, 2.3, f"{v1}V", fontsize=12, color="green")
    
    ax.plot([0, 0], [0, 2], 'k-') 
    ax.plot([0, 0], [3, 5], 'k-')
    ax.plot([0, 1.5], [5, 5], 'k-')
    
    # Resistor R1
    ax.add_patch(plt.Rectangle((1.5, 4.75), 2, 0.5, facecolor='lightgray', edgecolor='black'))
    ax.text(2, 5.4, f"R1: {r1}Ω", fontsize=10, fontweight='bold')
    ax.plot([3.5, 5], [5, 5], 'k-')

    # 2. MIDDLE BRANCH (R3 Load)
    ax.plot([5, 5], [5, 4], 'k-')
    ax.add_patch(plt.Rectangle((4.75, 2), 0.5, 2, facecolor='salmon', edgecolor='black'))
    ax.text(5.6, 2.8, f"R3 (Load): {r3}Ω", fontsize=10, fontweight='bold', color="red")
    ax.plot([5, 5], [2, 0], 'k-')
    
    # 3. RIGHT BRANCH (V2 & R2)
    ax.plot([5, 6.5], [5, 5], 'k-')
    # Resistor R2
    ax.add_patch(plt.Rectangle((6.5, 4.75), 2, 0.5, facecolor='lightgray', edgecolor='black'))
    ax.text(7, 5.4, f"R2: {r2}Ω", fontsize=10, fontweight='bold')
    ax.plot([8.5, 10], [5, 5], 'k-')
    
    # Voltage Source V2
    ax.plot([10, 10], [5, 3], 'k-')
    if active_source == "V1":
        ax.plot([10, 10], [1.5, 3.5], 'b--', lw=2) # Shorted
    else:
        circle2 = plt.Circle((10, 2.5), 0.5, color='black', fill=False, lw=2)
        ax.add_patch(circle2)
        ax.text(9.85, 2.6, "+", fontsize=15, fontweight='bold')
        ax.text(9.85, 2.1, "-", fontsize=15, fontweight='bold')
        ax.text(10.7, 2.3, f"{v2}V", fontsize=12, color="green")
    
    ax.plot([10, 10], [0, 2], 'k-')
    
    # BOTTOM RAIL
    ax.plot([0, 10], [0, 0], 'k-')
    
    ax.set_title(f"Circuit Diagram: Mode = {active_source}", fontsize=14)
    ax.axis('off')
    return fig

# --- STREAMLIT UI ---
st.title("⚡ Professional Superposition Solver")
st.markdown("Calculate the total current through the load resistor **R3** using the Superposition Theorem.")

# Inputs
with st.sidebar:
    st.header("Component Values")
    V1 = st.number_input("V1 Polarity (+) Up (V)", value=24.0)
    V2 = st.number_input("V2 Polarity (+) Up (V)", value=12.0)
    st.divider()
    R1 = st.number_input("R1 (Ω)", value=10.0, min_value=0.1)
    R2 = st.number_input("R2 (Ω)", value=20.0, min_value=0.1)
    R3 = st.number_input("R3 Load (Ω)", value=5.0, min_value=0.1)

# --- CALCULATIONS ---
# Step 1: V1 Only
req1 = R1 + (R2 * R3) / (R2 + R3)
i_total1 = V1 / req1
i_r3_v1 = i_total1 * (R2 / (R2 + R3)) # Current Divider

# Step 2: V2 Only
req2 = R2 + (R1 * R3) / (R1 + R3)
i_total2 = V2 / req2
i_r3_v2 = i_total2 * (R1 / (R1 + R3)) # Current Divider

# Total
total_i = i_r3_v1 + i_r3_v2

# --- TABS FOR STEPS ---
tab_orig, tab_v1, tab_v2, tab_final = st.tabs([
    "1. Original Circuit", 
    "2. V1 Contribution", 
    "3. V2 Contribution", 
    "4. Final Sum"
])

with tab_orig:
    st.subheader("Initial Circuit Configuration")
    st.pyplot(draw_schematic(V1, V2, R1, R2, R3, "Both"))
    st.info("The goal is to find the current flowing down through R3.")

with tab_v1:
    st.subheader("Analyzing V1 (V2 replaced by a short circuit)")
    st.pyplot(draw_schematic(V1, V2, R1, R2, R3, "V1"))
    st.latex(r"R_{parallel} = \frac{R_2 \cdot R_3}{R_2 + R_3}")
    st.write(f"Resistance in parallel: **{ (R2*R3)/(R2+R3) :.2f} Ω**")
    st.metric("Current Contribution (I')", f"{i_r3_v1:.4f} A")

with tab_v2:
    st.subheader("Analyzing V2 (V1 replaced by a short circuit)")
    st.pyplot(draw_schematic(V1, V2, R1, R2, R3, "V2"))
    st.latex(r"R_{parallel} = \frac{R_1 \cdot R_3}{R_1 + R_3}")
    st.write(f"Resistance in parallel: **{ (R1*R3)/(R1+R3) :.2f} Ω**")
    st.metric("Current Contribution (I'')", f"{i_r3_v2:.4f} A")

with tab_final:
    st.header("Superposition Result")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### Algebraic Summation")
        st.latex(r"I_{total} = I' + I''")
        st.write(f"$$I_{{total}} = {i_r3_v1:.4f} + {i_r3_v2:.4f}$$")
        st.success(f"**Total Current = {total_i:.4f} Amps**")
    
    with col_b:
        st.write("### Contribution Ratio")
        df = pd.DataFrame({
            "Source": ["V1", "V2"],
            "Amps": [i_r3_v1, i_r3_v2]
        })
        st.bar_chart(df, x="Source", y="Amps")
