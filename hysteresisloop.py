# ============================================================
# ⚡ B-H LOOP ANIMATION APP (Hysteresis Curve Visualizer)
# Streamlit + Plotly
# Learn how magnetic materials respond to changing magnetizing force
# ============================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="B-H Loop Visualizer", layout="wide")

st.title("🧲 B-H Loop Animation: Magnetic Hysteresis")
st.markdown("### Visualize magnetization, saturation, retentivity, and coercivity")

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
st.sidebar.header("⚙️ Material Controls")

H_max = st.sidebar.slider("Maximum Magnetizing Force H", 1, 20, 10)
mu = st.sidebar.slider("Relative Permeability Factor", 1.0, 10.0, 5.0)
coercivity = st.sidebar.slider("Coercivity Shift", 0.1, 5.0, 1.5)
points = st.sidebar.slider("Animation Resolution", 100, 1000, 400)

material = st.sidebar.selectbox(
    "Magnetic Material",
    ["Soft Iron", "Silicon Steel", "Hard Magnetic Material"]
)

# Material presets
if material == "Soft Iron":
    mu = 8.0
    coercivity = 0.8
elif material == "Silicon Steel":
    mu = 6.0
    coercivity = 1.2
else:
    mu = 3.5
    coercivity = 3.0

# ============================================================
# HYSTERESIS MODEL (Simplified)
# ============================================================

# Increasing H
H_up = np.linspace(-H_max, H_max, points)
B_up = np.tanh(mu * (H_up + coercivity))

# Decreasing H
H_down = np.linspace(H_max, -H_max, points)
B_down = np.tanh(mu * (H_down - coercivity))

# Full loop
H_loop = np.concatenate([H_up, H_down])
B_loop = np.concatenate([B_up, B_down])

# ============================================================
# ANIMATION FRAMES
# ============================================================
frames = []

for i in range(10, len(H_loop), 5):
    frames.append(
        go.Frame(
            data=[
                go.Scatter(
                    x=H_loop[:i],
                    y=B_loop[:i],
                    mode="lines",
                    line=dict(width=4),
                    name="B-H Loop"
                )
            ],
            name=str(i)
        )
    )

# ============================================================
# BASE FIGURE
# ============================================================
fig = go.Figure(
    data=[
        go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(width=4),
            name="B-H Loop"
        )
    ],
    layout=go.Layout(
        title=f"{material} Hysteresis Loop",
        xaxis=dict(title="Magnetizing Force (H)"),
        yaxis=dict(title="Flux Density (B)"),
        width=900,
        height=650,
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="▶ Start Animation",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {"duration": 30, "redraw": True},
                                "fromcurrent": True
                            }
                        ],
                    )
                ],
            )
        ]
    ),
    frames=frames
)

# Add key magnetic points
fig.add_hline(y=0, line_dash="dash")
fig.add_vline(x=0, line_dash="dash")

# ============================================================
# DISPLAY
# ============================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# METRICS
# ============================================================
with col2:
    st.subheader("📘 Key Magnetic Properties")

    retentivity = np.tanh(mu * coercivity)
    st.metric("Retentivity (Residual B)", f"{retentivity:.2f}")

    st.metric("Coercive Force", f"{coercivity:.2f}")

    loop_area = np.trapz(np.abs(B_up), H_up) + np.trapz(np.abs(B_down), H_down)
    st.metric("Approx. Hysteresis Loss", f"{loop_area:.2f}")

    # Material interpretation
    if material == "Soft Iron":
        st.success("⚡ Low coercivity → Ideal for transformers")
    elif material == "Silicon Steel":
        st.info("🌀 Balanced performance → Common in machine cores")
    else:
        st.warning("🧲 High coercivity → Permanent magnet behavior")

# ============================================================
# THEORY SECTION
# ============================================================
st.markdown("---")
st.subheader("📖 Understanding the B-H Loop")

st.info("""
### What the loop shows:
- **Saturation:** Material reaches max flux density
- **Retentivity:** Residual magnetism when H = 0
- **Coercivity:** Reverse H needed to demagnetize
- **Loop Area:** Energy lost as heat per cycle (hysteresis loss)

### Key Insight:
Soft magnetic materials have narrow loops (low loss)  
Hard magnetic materials have wide loops (high retention)
""")

# ============================================================
# FORMULA
# ============================================================
st.latex(r"P_h \propto \text{Area of B-H Loop}")

# ============================================================
# REEL CTA
# ============================================================
st.success("🎬 Reel Idea: 'Why does iron remember magnetism? Watch the B-H loop reveal the secret.'")
