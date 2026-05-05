import streamlit as st

# ================= 1. PAGE CONFIG MUST BE FIRST =================
st.set_page_config(
    page_title=" RL Circuit ",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= 2. IMPORTS =================
import numpy as np
import plotly.graph_objects as go

# ================= 3. RESPONSIVE CSS =================
# ================= 2. LIGHT MODE CSS =================
st.markdown("""
<style>
    /* Main background and font */
    .stApp {
        background-color: #f8f9fa;
    }
    html, body, [class*="css"] { 
        font-family: 'Inter', 'Segoe UI', sans-serif; 
        color: #212529;
    }
    .block-container { padding: 1rem 2rem; }
    
    /* KPI cards styling - Light Mode */
    .kpi-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
    }
    .kpi-title { 
        font-size: 0.85rem; 
        color: #6c757d; 
        font-weight: 600; 
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value { 
        font-size: 1.8rem; 
        font-weight: 800; 
        color: #0d6efd; /* Electric Blue */
    }

    /* Mobile adjustments */
    @media (max-width: 768px) {
        .kpi-value { font-size: 1.4rem; }
        h1 { font-size: 1.6rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ================= 4. CALCULATIONS =================
def calculate_rl(V_rms, R, L_mH, f):
    omega = 2 * np.pi * f
    L = L_mH / 1000  # mH to H
    XL = omega * L
    Z = np.sqrt(R**2 + XL**2)
    I_rms = V_rms / Z
    phi_rad = np.arctan(XL / R)
    phi_deg = np.degrees(phi_rad)
    pf = np.cos(phi_rad)
    P = V_rms * I_rms * pf
    Q = V_rms * I_rms * np.sin(phi_rad)

    return Z, I_rms, pf, phi_deg, XL, P, Q

# ================= 5. SIDEBAR =================
st.sidebar.header("🛠️ Circuit Parameters")

V_in = st.sidebar.slider("Voltage (Vrms)", 10, 230, 220)
R_in = st.sidebar.slider("Resistance (Ω)", 1, 500, 100)
L_in = st.sidebar.slider("Inductance (mH)", 1, 1000, 200)
f_in = st.sidebar.number_input("Frequency (Hz)", min_value=1, value=50)

# Calculate
Z, I, PF, Phase, XL, P, Q = calculate_rl(V_in, R_in, L_in, f_in)

# ================= 6. HEADER =================
st.markdown("<h1 style='text-align:center;'>⚡ RL Circuit Master Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Interactive Learning Dashboard for Electrical Engineering Students</p>", unsafe_allow_html=True)

# ================= 7. KPI DASHBOARD =================
col1, col2, col3, col4 = st.columns(4)

def kpi_card(title, value, unit=""):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value} {unit}</div>
        </div>
    """, unsafe_allow_html=True)

with col1:
    kpi_card("Impedance (Z)", f"{Z:.2f}", "Ω")

with col2:
    kpi_card("Current (Irms)", f"{I:.2f}", "A")

with col3:
    kpi_card("Power Factor", f"{PF:.3f}")

with col4:
    kpi_card("Phase Angle", f"{Phase:.1f}", "°")

# ================= 8. TABS =================
tab1, tab2, tab3 = st.tabs(["📊 Waveform Analysis", "📐 Phasor Diagram", "⚡ Power Analysis"])

# ---------- TAB 1 ----------
with tab1:
    t = np.linspace(0, 2/f_in, 1000)

    v_t = np.sqrt(2) * V_in * np.sin(2 * np.pi * f_in * t)
    i_t = np.sqrt(2) * I * np.sin(2 * np.pi * f_in * t - np.radians(Phase))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=v_t,
        name="Voltage (V)",
        line=dict(color="#ffeb3b", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=t, y=i_t * 10,
        name="Current (I x10)",
        line=dict(color="#00e5ff", width=3)
    ))

    fig.update_layout(
        title="RL Circuit Time Domain Response",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        template="plotly_dark",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- TAB 2 ----------
with tab2:
    fig_ph = go.Figure()

    # Voltage phasor endpoint
    Vx, Vy = V_in, 0

    # Current phasor endpoint (lagging)
    Ix = V_in * np.cos(np.radians(-Phase))
    Iy = V_in * np.sin(np.radians(-Phase))

    # Voltage Phasor Line
    fig_ph.add_trace(go.Scatter(
        x=[0, Vx],
        y=[0, Vy],
        mode="lines+text",
        text=["", "V"],
        textposition="top center",
        name="Voltage Phasor",
        line=dict(width=4)
    ))

    # Current Phasor Line
    fig_ph.add_trace(go.Scatter(
        x=[0, Ix],
        y=[0, Iy],
        mode="lines+text",
        text=["", "I"],
        textposition="top center",
        name="Current Phasor",
        line=dict(width=4)
    ))

    # Add Arrow for Voltage
    fig_ph.add_annotation(
        x=Vx,
        y=Vy,
        ax=0,
        ay=0,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.8,
        arrowwidth=3
    )

    # Add Arrow for Current
    fig_ph.add_annotation(
        x=Ix,
        y=Iy,
        ax=0,
        ay=0,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.8,
        arrowwidth=3
    )

    # Optional Phase Angle Arc
    theta = np.linspace(0, np.radians(-Phase), 50)
    arc_x = 0.25 * V_in * np.cos(theta)
    arc_y = 0.25 * V_in * np.sin(theta)

    fig_ph.add_trace(go.Scatter(
        x=arc_x,
        y=arc_y,
        mode="lines",
        name="Phase Angle",
        line=dict(dash="dot")
    ))

    # Phase Label
    fig_ph.add_annotation(
        x=0.3 * V_in * np.cos(np.radians(-Phase / 2)),
        y=0.3 * V_in * np.sin(np.radians(-Phase / 2)),
        text=f"φ = {Phase:.1f}°",
        showarrow=False
    )

    fig_ph.update_layout(
        title="Phasor Diagram with Direction Arrows",
        template="plotly_dark",
        xaxis=dict(
            title="Real Axis",
            range=[-V_in * 0.2, V_in * 1.2],
            zeroline=True
        ),
        yaxis=dict(
            title="Imaginary Axis",
            range=[-V_in, V_in * 0.5],
            zeroline=True,
            scaleanchor="x",
            scaleratio=1
        ),
        showlegend=True
    )

    st.plotly_chart(fig_ph, use_container_width=True)

# ---------- TAB 3 ----------
with tab3:
    st.subheader("Power Components")

    colp1, colp2 = st.columns(2)

    with colp1:
        st.metric("Real Power (P)", f"{P:.2f} W")

    with colp2:
        st.metric("Reactive Power (Q)", f"{Q:.2f} VAR")

    power_triangle = go.Figure()

    power_triangle.add_trace(go.Scatter(
        x=[0, P, P, 0],
        y=[0, 0, Q, 0],
        fill="toself",
        name="Power Triangle"
    ))

    power_triangle.update_layout(
        title="Power Triangle",
        xaxis_title="Real Power (W)",
        yaxis_title="Reactive Power (VAR)",
        template="plotly_dark"
    )

    st.plotly_chart(power_triangle, use_container_width=True)

# ================= 9. KEY FORMULAS =================
st.markdown("## 📘 Key RL Circuit Formulas")
st.latex(r"X_L = 2\pi f L")
st.latex(r"Z = \sqrt{R^2 + X_L^2}")
st.latex(r"I = \frac{V}{Z}")
st.latex(r"\cos\phi = \frac{R}{Z}")

# ================= 10. FOOTER =================
st.markdown("""
<hr>
<div style='text-align:center; font-size:14px;'>
⚡ Designed for Learn EE Interactive • Mobile Responsive • InfoTeck Analytics
</div>
""", unsafe_allow_html=True)
