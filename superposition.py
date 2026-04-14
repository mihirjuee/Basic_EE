import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Superposition Solver", page_icon="log.png")

st.title("⚡ Superposition Theorem Solver")
st.markdown("""
This app calculates the current through a central load resistor ($R_3$) in a two-source circuit 
by applying the **Superposition Theorem** step-by-step.
""")

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")

with st.sidebar:
    st.subheader("Voltage Sources (V)")
    v1 = st.number_input("Source V1 (Volts)", value=12.0)
    v2 = st.number_input("Source V2 (Volts)", value=6.0)

    st.subheader("Resistors (Ω)")
    r1 = st.number_input("Resistor R1", value=10.0, min_value=0.1)
    r2 = st.number_input("Resistor R2", value=20.0, min_value=0.1)
    r3 = st.number_input("Load Resistor R3", value=5.0, min_value=0.1)

# --- Calculation Logic ---

# Step 1: V1 acting alone (V2 shorted)
# R2 and R3 are in parallel
r_p1 = (r2 * r3) / (r2 + r3)
i_total1 = v1 / (r1 + r_p1)
# Current through R3 using current divider
i_r3_v1 = i_total1 * (r2 / (r2 + r3))

# Step 2: V2 acting alone (V1 shorted)
# R1 and R3 are in parallel
r_p2 = (r1 * r3) / (r1 + r3)
i_total2 = v2 / (r2 + r_p2)
# Current through R3 using current divider
i_r3_v2 = i_total2 * (r1 / (r1 + r3))

# Final Result
total_current = i_r3_v1 + i_r3_v2

# --- UI Display ---

col1, col2 = st.columns(2)

with col1:
    st.info(f"**Contribution from V1**\n\n{i_r3_v1:.4f} A")
    st.write(f"*Calculation:* V1 is active, V2 is replaced by a short circuit. R2 and R3 are in parallel.")

with col2:
    st.info(f"**Contribution from V2**\n\n{i_r3_v2:.4f} A")
    st.write(f"*Calculation:* V2 is active, V1 is replaced by a short circuit. R1 and R3 are in parallel.")

st.divider()

# Final Large Display
st.metric(label="Total Current through R3 (Load)", value=f"{total_current:.4f} A")

# Visualizing the contribution
chart_data = pd.DataFrame({
    "Source": ["V1 Only", "V2 Only", "Total"],
    "Current (A)": [i_r3_v1, i_r3_v2, total_current]
})

st.subheader("Contribution Visualization")
st.bar_chart(chart_data, x="Source", y="Current (A)", color="#FF4B4B")

# Detailed Mathematical Breakdown
with st.expander("Show Detailed Mathematical Steps"):
    st.latex(r"I_{R3(V1)} = \frac{V_1}{R_1 + \frac{R_2 \cdot R_3}{R_2 + R_3}} \cdot \frac{R_2}{R_2 + R_3}")
    st.latex(r"I_{R3(V2)} = \frac{V_2}{R_2 + \frac{R_1 \cdot R_3}{R_1 + R_3}} \cdot \frac{R_1}{R_1 + R_3}")
    st.latex(r"I_{total} = I_{R3(V1)} + I_{R3(V2)}")
