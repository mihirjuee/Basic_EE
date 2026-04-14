import streamlit as st
import pandas as pd
import schemdraw
import schemdraw.elements as elm
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Norton's Theorem Virtual Lab",page_icon="logo.png", layout="wide")

st.title("⚡ Verification of Norton's Theorem")
st.markdown("""
This interactive lab demonstrates how a complex network can be reduced to a single current source ($I_{sc}$) 
in parallel with a resistance ($R_n$). 
""")

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")
V1 = st.sidebar.slider("Voltage Source (V1) [V]", 5.0, 50.0, 10.0, step=1.0)
R1 = st.sidebar.slider("Resistor R1 [Ω]", 10.0, 100.0, 50.0, step=5.0)
R2 = st.sidebar.slider("Resistor R2 [Ω]", 10.0, 100.0, 50.0, step=5.0)
R3 = st.sidebar.slider("Resistor R3 [Ω]", 10.0, 100.0, 50.0, step=5.0)
RL = st.sidebar.slider("Load Resistor RL [Ω]", 10.0, 200.0, 100.0, step=10.0)

# --- Circuit Calculations ---
# 1. Norton Resistance: Rth/Rn = R2 + (R1||R3)
Rn = R2 + ((R1 * R3) / (R1 + R3))
# 2. Thevenin Voltage (Open Circuit) for step-wise calculation: Vth = V1 * (R3 / (R1 + R3))
Vth = V1 * (R3 / (R1 + R3))
# 3. Norton Current: Isc = Vth / Rn
Isc = Vth / Rn
# 4. Actual Load Current from original circuit
IL_actual = Vth / (Rn + RL)
# 5. Calculated Current using Norton's Formula
IL_norton = Isc * (Rn / (Rn + RL))

# --- Drawing Functions ---

def draw_main_circuit(v, r1, r2, r3, rl):
    """Original T-Network."""
    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().up().label(f'{v}V')
    d += elm.Resistor().right().label(f'R1\n{r1}Ω')
    d.push()
    d += elm.Resistor().down().label(f'R3\n{r3}Ω')
    d += elm.Line().left()
    d.pop()
    d += elm.Resistor().right().label(f'R2\n{r2}Ω')
    d += elm.Resistor().down().label(f'RL\n{rl}Ω', color='blue')
    d += elm.Line().left().tox(d.elements[0].start)
    return d.draw().fig

def draw_short_circuit(v, r1, r2, r3):
    """Case 2a: Finding Isc."""
    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().up().label(f'{v}V')
    d += elm.Resistor().right().label(f'R1\n{r1}Ω')
    d.push()
    d += elm.Resistor().down().label(f'R3\n{r3}Ω')
    d += elm.Line().left()
    d.pop()
    d += elm.Resistor().right().label(f'R2\n{r2}Ω')
    d += elm.Line().down().color('red').label('$I_{sc}$', loc='bottom')
    d += elm.CurrentLabel(top=False).at(d.elements[-1]).label('')
    d += elm.Line().left().tox(d.elements[0].start)
    return d.draw().fig

def draw_rn_circuit(r1, r2, r3):
    d = schemdraw.Drawing(show=False)
    # 1. Source is shorted (represented as a wire)
    d += elm.Line().up().label('Short', loc='center')
    d += elm.Resistor().right().label(f'R1\n{r1}Ω')
    
    d.push()
    # 2. Draw R3 and save it to find the bottom rail height
    d += (R3_el := elm.Resistor().down().label(f'R3\n{r3}Ω'))
    d += elm.Line().left().tox(d.elements[0].start)
    d.pop()
    
    # 3. Draw R2 going to the right
    d += (R2_el := elm.Resistor().right().label(f'R2\n{r2}Ω'))
    
    # 4. Place Terminal A (Open)
    d += (DotA := elm.Dot(open=True).label('A', loc='right'))
    
    # 5. Place Terminal B (Open) - NO LINE DRAWN HERE
    # We place it at the same x-coordinate as A, but the same y-coordinate as the bottom rail
    d += (DotB := elm.Dot(open=True).at((DotA.end[0], R3_el.end[1])).label('B', loc='right'))
    
    # 6. Close the bottom rail back to R3
    d += elm.Line().left().at(DotB.center).tox(R3_el.end)
    return d.draw().fig
    
def draw_norton_equivalent(isc, rn, rl):
    """Case 3: Equivalent Circuit."""
    d = schemdraw.Drawing(show=False)
    d += elm.SourceI().up().label(f'$I_{{sc}}$\n{isc:.3f}A')
    d += elm.Line().right()
    d.push()
    d += elm.Resistor().down().label(f'$R_n$\n{rn:.2f}Ω')
    d += elm.Line().left()
    d.pop()
    d += elm.Line().right()
    d += elm.Resistor().down().label(f'$R_L$\n{rl}Ω', color='blue')
    d += elm.Line().left().tox(d.elements[0].start)
    return d.draw().fig

# --- UI Interface with Tabs ---
tab1, tab2, tab3 = st.tabs(["1. Actual Circuit", "2. Norton Parameters", "3. Verification"])

with tab1:
    st.header("Step 1: Original Network")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.pyplot(draw_main_circuit(V1, R1, R2, R3, RL))
    with c2:
        st.metric("Load Current ($I_L$)", f"{IL_actual:.4f} A")
        st.info("This is the current flowing through the load resistor in the original circuit.")

with tab2:
    st.header("Step 2: Deriving $I_{sc}$ and $R_n$")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("2(a): Short Circuit Current")
        st.pyplot(draw_short_circuit(V1, R1, R2, R3))
        st.success(f"**$I_{{sc}}$ = {Isc:.4f} A**")
    with col2:
        st.subheader("2(b): Equivalent Resistance")
        st.pyplot(draw_rn_circuit(R1, R2, R3))
        st.success(f"**$R_n$ = {Rn:.2f} Ω**")

with tab3:
    st.header("Step 3: Norton Verification")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.pyplot(draw_norton_equivalent(Isc, Rn, RL))
    with c2:
        st.latex(r"I_L = I_{sc} \times \frac{R_n}{R_n + R_L}")
        st.metric("Calculated $I_L$", f"{IL_norton:.4f} A")
        
        if round(IL_actual, 4) == round(IL_norton, 4):
            st.balloons()
            st.success("✅ **Verified!** The equivalent circuit yields the same load current.")

# --- Results Table ---
st.divider()
st.subheader("📋 Observation Data")
res_data = {
    "V_source": [V1], "R_load": [RL], "Norton_Isc": [round(Isc, 4)], 
    "Norton_Rn": [round(Rn, 2)], "Actual_IL": [round(IL_actual, 4)], 
    "Verified_IL": [round(IL_norton, 4)]
}
st.table(pd.DataFrame(res_data))
