import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AC Phasor & Tracer", layout="wide")

# --- MOBILE TOGGLE ---
is_mobile = st.toggle("📱 Mobile Layout", value=False)

# --- HEADER (WITH LOGO) ---
if is_mobile:
    st.image("logo.png", width=80)
    st.title("AC Fundamentals: Moving Tracer & Vector")
else:
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("logo.png", width=60)
    with col2:
        st.title("AC Fundamentals: Moving Tracer & Vector")

# --- SESSION STATE ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'theta_step' not in st.session_state:
    st.session_state.theta_step = 0.0

# --- SIDEBAR ---
st.sidebar.header("Signal Parameters")
V_m = st.sidebar.slider("Amplitude (V_m)", 1.0, 10.0, 5.0)
phase_deg = st.sidebar.slider("Initial Phase (φ)", -180, 180, 0)

st.sidebar.markdown("---")
st.sidebar.header("Motion Controls")
speed = st.sidebar.slider("Playback Speed", 1, 20, 5)

manual_theta = st.sidebar.slider(
    "Manual Angle Scrub",
    0.0, 360.0,
    float(st.session_state.theta_step % 360),
    step=1.0
)
st.session_state.theta_step = manual_theta

# --- PLAY/PAUSE ---
col1, col2 = st.sidebar.columns(2)
if col1.button("▶️ Play"):
    st.session_state.running = True
if col2.button("⏸️ Pause"):
    st.session_state.running = False

# --- MATH ---
phase_rad = np.deg2rad(phase_deg)
current_theta_deg = st.session_state.theta_step % 360
current_theta_rad = np.deg2rad(current_theta_deg)

degrees_axis = np.linspace(0, 360, 500)
v_waveform = V_m * np.sin(np.deg2rad(degrees_axis) + phase_rad)

v_instant = V_m * np.sin(current_theta_rad + phase_rad)
total_vector_angle = current_theta_rad + phase_rad

# --- PLOT AREA ---
plot_placeholder = st.empty()

with plot_placeholder.container():

    # 📱 MOBILE → STACKED
    if is_mobile:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    else:
        fig, (ax1, ax2) = plt.subplots(
            1, 2,
            figsize=(12, 5),
            gridspec_kw={'width_ratios': [1, 1.5]}
        )

    # --- POLAR VECTOR ---
    ax1.remove()
    if is_mobile:
        ax1 = fig.add_subplot(211, projection='polar')
    else:
        ax1 = fig.add_subplot(121, projection='polar')

    ax1.annotate(
        '',
        xy=(total_vector_angle, V_m),
        xytext=(0, 0),
        arrowprops=dict(
            facecolor='dodgerblue',
            edgecolor='dodgerblue',
            width=2 if is_mobile else 3,
            headwidth=8 if is_mobile else 10
        )
    )

    ax1.set_ylim(0, 10)
    ax1.set_title(f"Vector: {current_theta_deg:.1f}°", pad=15)

    # --- WAVEFORM ---
    if is_mobile:
        ax2 = fig.add_subplot(212)
    else:
        ax2 = fig.add_subplot(122)

    ax2.axhline(0, linewidth=1.2)

    ax2.plot(
        degrees_axis,
        v_waveform,
        linewidth=2,
        alpha=0.4,
        label='Signal Path'
    )

    ax2.plot(
        current_theta_deg,
        v_instant,
        marker='o',
        markersize=10 if is_mobile else 12,
        label='Tracer'
    )

    ax2.axvline(
        x=current_theta_deg,
        linestyle='--',
        alpha=0.3
    )

    ax2.set_xlim(0, 360)
    ax2.set_ylim(-10.5, 10.5)
    ax2.set_xticks([0, 90, 180, 270, 360])
    ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])

    ax2.set_xlabel("Cycle Angle (Degrees)")
    ax2.set_ylabel("Voltage (V)")
    ax2.set_title("Waveform Tracer")

    ax2.grid(True, linestyle=':', alpha=0.5)
    ax2.legend(loc='upper right')

    st.pyplot(fig)
    plt.close(fig)

# --- ANIMATION LOOP ---
if st.session_state.running:
    st.session_state.theta_step += speed
    time.sleep(0.01)
    st.rerun()
