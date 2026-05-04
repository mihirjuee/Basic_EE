import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ================= 1. MOBILE RESPONSIVE CONFIG =================
st.set_page_config(
    page_title="⚡ RL Circuit Master Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. RESPONSIVE CSS =================
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    .block-container { padding: 1rem 2rem; }
    
    /* KPI cards styling */
    .kpi-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        margin-bottom: 15px;
    }
    .kpi-title { font-size: 0.9rem; color: #cfd8dc; }
    .kpi-value { font-size: 1.6rem; font-weight: bold; color: #00e5ff; }

    /* Mobile adjustments */
    @media (max-width: 768px) {
        .kpi-value { font-size: 1.2rem; }
        h1 { font-size: 1.6rem !important; text-align: center; }
        div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. LOGIC & CALCULATIONS =================
def calculate_rl(V_rms, R, L_mH, f):
    omega = 2 * np.pi * f
    L = L_mH / 1000  # Convert mH to H
    XL = omega * L
    Z = np.sqrt(R**2 + XL**2)
    I_rms = V_rms / Z
    phi_rad = np.arctan(XL / R)
    phi_deg = np.degrees(phi_rad)
    pf = np.cos(phi_rad)
    return Z, I_rms, pf, phi_deg, XL

# ================= 4. SIDEBAR CONTROLS =================
st.sidebar.header("🛠️ Circuit Parameters")
V_in = st.sidebar.slider("Voltage (Vrms)", 10, 230, 220)
R_in = st.sidebar.slider("Resistance (Ω)", 1, 500, 100)
L_in = st.sidebar.slider("Inductance (mH)", 1, 1000, 200)
f_in = st.sidebar.number_input("Frequency (Hz)", value=50)

# Run Calculations
Z, I, PF, Phase, XL = calculate_rl(V_in, R_in, L_in, f_in)

# ================= 5. HEADER & KPI DASHBOARD =================
st.markdown("<h1 style='text-align: center;'>⚡ RL Circuit Master Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interactive Learning Dashboard for InfoTeck Students</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

def kpi_card(title, value, unit=""):
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">{title}</div>
    <div class="kpi-value">{value} {unit}</div></div>""", unsafe_allow_html=True)

with col1: kpi_card("Impedance (Z)", f"{Z:.2f}", "Ω")
with col2: kpi_card("Current (Irms)", f"{I:.2f}", "A")
with col3: kpi_card("Power Factor", f"{PF:.3f}")
with col4: kpi_card("Phase Angle", f"{Phase:.1f}", "°")

# ================= 6. TABS & VISUALIZATION =================
tab1, tab2 = st.tabs(["📊 Waveform Analysis", "📐 Phasor Diagram"])

with tab1:
    t = np.linspace(0, 0.04, 500) # 2 cycles at 50Hz
    v_t = np.sqrt(2) * V_in * np.sin(2 * np.pi * f_in * t)
    i_t = np.sqrt(2) * I * np.sin(2 * np.pi * f_in * t - np.radians(Phase))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=v_t, name="Voltage (v)", line=dict(color='#ffeb3b')))
    fig.add_trace(go.Scatter(x=t, y=i_t*10, name="Current (i x10)", line=dict(color='#00e5ff'))) # Scaled for visibility
    
    fig.update_layout(
        title="Time Domain Waveforms",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        template="plotly_dark",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Basic Phasor Plot
    fig_phasor = go.Figure()
    # Voltage Phasor (Reference)
    fig_phasor.add_trace(go.Scatter(x=[0, V_in], y=[0, 0], mode='lines+markers', name='V Phasor', line=dict(width=4)))
    # Current Phasor (Lagging)
    fig_phasor.add_trace(go.Scatter(x=[0, V_in*np.cos(np.radians(-Phase))], 
                                    y=[0, V_in*np.sin(np.radians(-Phase))], 
                                    mode='lines+markers', name='I Phasor (scaled)', line=dict(width=4)))
    
    fig_phasor.update_layout(title="Phasor Diagram", template="plotly_dark", showlegend=True,
                             xaxis=dict(range=[-V_in, V_in*1.2]), yaxis=dict(range=[-V_in, V_in]))
    st.plotly_chart(fig_phasor, use_container_width=True)

# ================= 7. FOOTER =================
st.markdown("""<hr><div style='text-align:center; font-size:14px;'>
Designed for Learn EE Interactive • Validated by InfoTeck Analytics 📱</div>""", unsafe_allow_html=True)
