# ================= MOBILE RESPONSIVE UPGRADE =================
# Add this section near the top of your Streamlit app
# (after st.set_page_config)

st.set_page_config(
    page_title="⚡ RL Circuit Master Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= RESPONSIVE CSS =================
st.markdown("""
<style>
/* Base App Styling */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Main container */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    margin-bottom: 10px;
}
.kpi-title {
    font-size: 0.9rem;
    color: #cfd8dc;
}
.kpi-value {
    font-size: 1.4rem;
    font-weight: bold;
    color: #00e5ff;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    min-width: 280px !important;
    max-width: 320px !important;
}

/* Charts */
canvas, .js-plotly-plot {
    max-width: 100% !important;
}

/* Tablet */
@media (max-width: 992px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .kpi-value {
        font-size: 1.2rem;
    }

    .kpi-title {
        font-size: 0.8rem;
    }
}

/* Mobile */
@media (max-width: 768px) {

    .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    h1 {
        font-size: 1.6rem !important;
        text-align: center;
    }

    h2, h3 {
        font-size: 1.2rem !important;
    }

    .kpi-card {
        padding: 10px;
        border-radius: 10px;
    }

    .kpi-value {
        font-size: 1rem;
    }

    .kpi-title {
        font-size: 0.75rem;
    }

    section[data-testid="stSidebar"] {
        width: 100% !important;
    }

    /* Stack columns vertically */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Plot resizing */
    .js-plotly-plot, .plot-container {
        width: 100% !important;
        overflow-x: auto;
    }
}

/* Small mobile */
@media (max-width: 480px) {
    h1 {
        font-size: 1.3rem !important;
    }

    .stSlider label {
        font-size: 0.8rem !important;
    }

    .stNumberInput label {
        font-size: 0.8rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ================= RESPONSIVE HEADER =================
st.markdown("""
<div style='text-align:center; padding:10px;'>
    <h1>⚡ RL Circuit Master Pro</h1>
    <p style='font-size:16px;'>Interactive Mobile-Friendly RL Circuit Learning Dashboard</p>
</div>
""", unsafe_allow_html=True)


# ================= MOBILE KPI FUNCTION =================
def kpi_card(title, value, unit=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value} {unit}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ================= EXAMPLE RESPONSIVE KPI LAYOUT =================
st.subheader("📊 RL Circuit Key Parameters")

col1, col2 = st.columns(2)
with col1:
    kpi_card("Impedance", "24.5", "Ω")
    kpi_card("Current", "2.4", "A")

with col2:
    kpi_card("Power Factor", "0.82")
    kpi_card("Phase Angle", "34°")


# ================= MOBILE TABS =================
tab1, tab2, tab3 = st.tabs(["⚡ AC Analysis", "🔄 DC Transient", "📈 Frequency Sweep"])

with tab1:
    st.write("AC RL circuit analysis content here")

with tab2:
    st.write("Transient response graphs here")

with tab3:
    st.write("Frequency sweep visualization here")


# ================= MOBILE FOOTER =================
st.markdown("""
<hr>
<div style='text-align:center; font-size:14px; padding:8px;'>
    Designed for Desktop • Tablet • Mobile 📱
</div>
""", unsafe_allow_html=True)
