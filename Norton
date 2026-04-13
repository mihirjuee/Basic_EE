import streamlit as st
import pandas as pd
import schemdraw
import schemdraw.elements as elm

# --- Page Config ---
st.set_page_config(page_title="Norton's Theorem Virtual Lab", layout="wide")
st.title("⚡ Verification of Norton's Theorem")
st.write("Adjust the circuit parameters in the sidebar to verify the theorem.")

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")
V1 = st.sidebar.slider("Voltage Source (V1) in Volts", 5.0, 50.0, 10.0, step=1.0)
R1 = st.sidebar.slider("Resistor R1 (Ohms)", 10.0, 100.0, 50.0, step=5.0)
R2 = st.sidebar.slider("Resistor R2 (Ohms)", 10.0, 100.0, 50.0, step=5.0)
R3 = st.sidebar.slider("Resistor R3 (Ohms)", 10.0, 100.0, 50.0, step=5.0)
RL = st.sidebar.slider("Load Resistor RL (Ohms)", 10.0, 200.0, 100.0, step=10.0)

# --- Circuit Math ---
Rn = R2 + ((R1 * R3) / (R1 + R3))
Vth = V1 * (R3 / (R1 + R3))
Isc = Vth / Rn
IL_actual = Vth / (Rn + RL)
IL_norton = Isc * (Rn / (Rn + RL))

# --- Drawing Functions ---
def draw_main_circuit(v, r1, r2, r3, rl):
    """Draws the standard T-network circuit."""
    d = schemdraw.Drawing(show=False)
    d.config(fontsize=12)
    d += elm.SourceV().up().label(f'{v}V')
    d += elm.Resistor().right().label(f'R1\n{r1}Ω')
    d.push()
    d += elm.Resistor().down().label(f'R3\n{r3}Ω')
    d += elm.Line().left()
    d.pop()
    d += elm.Resistor().right().label(f'R2\n{r2}Ω')
    # Highlight the load resistor in blue
    d += elm.Resistor().down().label(f'RL\n{rl}Ω', color='blue')
    d += elm.Line().left().tox(d.elements[0].start)
    return d.draw().fig

def draw_norton_circuit(isc, rn, rl):
    """Draws the Norton equivalent circuit."""
    d = schemdraw.Drawing(show=False)
    d.config(fontsize=12)
    d += elm.SourceI().up().label(f'I_sc\n{isc:.2f}A')
    d += elm.Line().right()
    d.push()
    d += elm.Resistor().down().label(f'Rn\n{rn:.2f}Ω')
    d += elm.Line().left()
    d.pop()
    d += elm.Line().right()
    # Highlight the load resistor in blue
    d += elm.Resistor().down().label(f'RL\n{rl}Ω', color='blue')
    d += elm.Line().left().tox(d.elements[0].start)
    return d.draw().fig

# --- Main App Interface (Tabs) ---
tab1, tab2, tab3 = st.tabs(["Case 1: Actual Load", "Case 2: Norton Parameters", "Case 3: Verification"])

with tab1:
    st.header("Case 1: Measure Actual Load Current")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Here is the full circuit. The load resistor ($R_L$) is highlighted in blue.")
        st.pyplot(draw_main_circuit(V1, R1, R2, R3, RL))
    with col2:
        st.info(f"**Actual Load Current ($I_L$):**\n\n### {IL_actual:.4f} A")

with tab2:
    st.header("Case 2: Find Norton Equivalent")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Case 2(a): Short Circuit")
        st.write("If we short the load, this is the current that flows.")
        st.success(f"**Norton Current ($I_{{sc}}$):**\n\n### {Isc:.4f} A")
        
    with col2:
        st.subheader("Case 2(b): Norton Resistance")
        st.write("Resistance measured from the load terminals with the voltage source shorted.")
        st.success(f"**Norton Resistance ($R_n$):**\n\n### {Rn:.2f} Ω")

with tab3:
    st.header("Case 3: Verification")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Here is the simplified Norton Equivalent circuit:")
        st.pyplot(draw_norton_circuit(Isc, Rn, RL))
    with col2:
        st.write("Applying the current divider rule:")
        st.latex(r"I_L = I_{sc} \times \frac{R_n}{R_n + R_L}")
        st.info(f"**Calculated Load Current:**\n\n### {IL_norton:.4f} A")
        
        if round(IL_actual, 4) == round(IL_norton, 4):
            st.success("✅ **Verified!** Actual current matches calculated current.")

# --- Observation Table ---
st.divider()
st.subheader("Observation Table")
data = {
    "V1 (V)": [V1], "R1 (Ω)": [R1], "R2 (Ω)": [R2], "R3 (Ω)": [R3], "RL (Ω)": [RL],
    "Actual I_L (A)": [round(IL_actual, 4)], "Norton I_sc (A)": [round(Isc, 4)],
    "Norton R_n (Ω)": [round(Rn, 2)], "Calculated I_L (A)": [round(IL_norton, 4)]
}
st.dataframe(pd.DataFrame(data), hide_index=True)
