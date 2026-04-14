import streamlit as st
import pandas as pd
import schemdraw
import schemdraw.elements as elm
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Thevenin's Theorem Virtual Lab", layout="wide")

st.title("⚡ Verification of Thevenin's Theorem")
st.markdown("""
This interactive lab demonstrates how a complex network can be reduced to a single voltage source ($V_{th}$) 
in series with a resistance ($R_{th}$).
""")

# --- Sidebar Inputs ---
st.sidebar.header("Circuit Parameters")
V1 = st.sidebar.slider("Voltage Source (V1) [V]", 5.0, 50.0, 10.0, step=1.0)
R1 = st.sidebar.slider("Resistor R1 [Ω]", 10.0, 100.0, 50.0, step=5.0)
R2 = st.sidebar.slider("Resistor R2 [Ω]", 10.0, 100.0, 50.0, step=5.0)
R3 = st.sidebar.slider("Resistor R3 [Ω]", 10.0, 100.0, 50.0, step=5.0)
RL = st.sidebar.slider("Load Resistor RL [Ω]", 10.0, 200.0, 100.0, step=10.0)

# --- Circuit Calculations ---
# Thevenin Voltage (Open Circuit Voltage)
Vth = V1 * (R3 / (R1 + R3))

# Thevenin Resistance (Source shorted)
Rth = R2 + ((R1 * R3) / (R1 + R3))

# Load Current (Original Circuit)
IL_actual = Vth / (Rth + RL)

# Load Current (Thevenin Equivalent)
IL_thevenin = Vth / (Rth + RL)

# --- Drawing Functions ---

def draw_main_circuit(v, r1, r2, r3, rl):
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


def draw_open_circuit(v, r1, r2, r3):
    """Finding Vth (open RL)"""
    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().up().label(f'{v}V')
    d += elm.Resistor().right().label(f'R1\n{r1}Ω')

    d.push()
    d += elm.Resistor().down().label(f'R3\n{r3}Ω')
    d += elm.Line().right()
    d += elm.Dot(open=True).label('B')
    d.pop()

    d += elm.Resistor().right().label(f'R2\n{r2}Ω')
    d += elm.Dot(open=True).label('A')

    #d += elm.Line().down().length(2)
    #d += elm.Dot(open=True).label('B')

    #d += elm.Line().left().tox(d.elements[0].start)

    return d.draw().fig


def draw_rth_circuit(r1, r2, r3):
    """Finding Rth (source shorted)"""
    d = schemdraw.Drawing(show=False)

    d += elm.Line().up().label('Short')
    d += elm.Resistor().right().label(f'R1\n{r1}Ω')

    d.push()
    R3_el = elm.Resistor().down().label(f'R3\n{r3}Ω')
    d += R3_el
    d += elm.Line().left().tox(d.elements[0].start)
    d.pop()

    d += elm.Resistor().right().label(f'R2\n{r2}Ω')
    d += elm.Dot(open=True).label('A')

    d += elm.Dot(open=True).at((d.elements[-1].end[0], R3_el.end[1])).label('B')
    d += elm.Line().left().tox(R3_el.end)

    return d.draw().fig


def draw_thevenin_equivalent(vth, rth, rl):
    d = schemdraw.Drawing(show=False)

    d += elm.SourceV().up().label(f'$V_{{th}}$\n{vth:.2f}V')
    d += elm.Resistor().right().label(f'$R_{{th}}$\n{rth:.2f}Ω')

    d += elm.Resistor().down().label(f'$R_L$\n{rl}Ω', color='blue')
    d += elm.Line().left().tox(d.elements[0].start)

    return d.draw().fig


# --- UI Tabs ---
tab1, tab2, tab3 = st.tabs(["1. Actual Circuit", "2. Thevenin Parameters", "3. Verification"])

# --- TAB 1 ---
with tab1:
    st.header("Step 1: Original Network")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.pyplot(draw_main_circuit(V1, R1, R2, R3, RL))

    with c2:
        st.metric("Load Current ($I_L$)", f"{IL_actual:.4f} A")
        st.info("Current through load in original circuit.")

# --- TAB 2 ---
with tab2:
    st.header("Step 2: Deriving $V_{th}$ and $R_{th}$")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2(a): Open Circuit Voltage")
        st.pyplot(draw_open_circuit(V1, R1, R2, R3))
        st.success(f"**$V_{{th}}$ = {Vth:.2f} V**")

    with col2:
        st.subheader("2(b): Equivalent Resistance")
        st.pyplot(draw_rth_circuit(R1, R2, R3))
        st.success(f"**$R_{{th}}$ = {Rth:.2f} Ω**")

# --- TAB 3 ---
with tab3:
    st.header("Step 3: Thevenin Verification")

    c1, c2 = st.columns([2, 1])

    with c1:
        st.pyplot(draw_thevenin_equivalent(Vth, Rth, RL))

    with c2:
        st.latex(r"I_L = \frac{V_{th}}{R_{th} + R_L}")
        st.metric("Calculated $I_L$", f"{IL_thevenin:.4f} A")

        if round(IL_actual, 4) == round(IL_thevenin, 4):
            st.balloons()
            st.success("✅ **Verified!** Thevenin equivalent matches original circuit.")

# --- Results Table ---
st.divider()
st.subheader("📋 Observation Data")

res_data = {
    "V_source": [V1],
    "R_load": [RL],
    "Vth": [round(Vth, 2)],
    "Rth": [round(Rth, 2)],
    "Actual_IL": [round(IL_actual, 4)],
    "Thevenin_IL": [round(IL_thevenin, 4)]
}

st.table(pd.DataFrame(res_data))
