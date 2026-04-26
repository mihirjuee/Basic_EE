import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.title("🔌 Advanced Circuit Simulator")

# ================= SESSION =================
if "components" not in st.session_state:
    st.session_state.components = []

if "connections" not in st.session_state:
    st.session_state.connections = []

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🧩 Add Component")

    comp_type = st.selectbox("Type", ["Battery", "Resistor"])
    value = st.number_input("Value", 1.0, 1000.0, 10.0)

    if st.button("Add"):
        st.session_state.components.append({
            "type": comp_type,
            "value": value,
            "id": len(st.session_state.components)
        })

    st.header("🔗 Connections")

    if len(st.session_state.components) >= 2:
        c1 = st.selectbox("From", range(len(st.session_state.components)))
        c2 = st.selectbox("To", range(len(st.session_state.components)))

        if st.button("Connect"):
            if c1 != c2:
                st.session_state.connections.append((c1, c2))

# ================= GRAPH =================
fig = go.Figure()
positions = {}

for i, comp in enumerate(st.session_state.components):
    x = i * 2
    y = 0
    positions[i] = (x, y)

    # Different visual for components
    if comp["type"] == "Battery":
        symbol = "⚡"
    else:
        symbol = "⎍"

    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text',
        text=[f"{symbol}\n{comp['value']}"],
        textposition="top center",
        marker=dict(size=20)
    ))

# Draw wires
for (i, j) in st.session_state.connections:
    x0, y0 = positions[i]
    x1, y1 = positions[j]

    fig.add_trace(go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode='lines',
        line=dict(width=4, color="black")
    ))

fig.update_layout(height=400, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ================= SOLVER =================
st.subheader("🧠 Circuit Solution")

components = st.session_state.components
connections = st.session_state.connections

nodes = list(set([i for pair in connections for i in pair]))
n = len(nodes)

if n < 2:
    st.warning("Incomplete circuit")
else:
    node_index = {node: idx for idx, node in enumerate(nodes)}

    G = np.zeros((n, n))
    I_vec = np.zeros(n)

    # Build matrix
    for (i, j) in connections:
        comp_i = components[i]
        comp_j = components[j]

        if comp_i["type"] == "Resistor":
            R = comp_i["value"]
        elif comp_j["type"] == "Resistor":
            R = comp_j["value"]
        else:
            continue

        g = 1 / R
        ni, nj = node_index[i], node_index[j]

        G[ni][ni] += g
        G[nj][nj] += g
        G[ni][nj] -= g
        G[nj][ni] -= g

    # Handle multiple voltage sources (simple model)
    for comp in components:
        if comp["type"] == "Battery":
            idx = node_index.get(comp["id"], None)
            if idx is not None:
                I_vec[idx] += comp["value"]

    # Solve
    try:
        G_red = G[1:, 1:]
        I_red = I_vec[1:]

        V_nodes = np.linalg.solve(G_red, I_red)
        V_nodes = np.insert(V_nodes, 0, 0)

        st.success("Solved ✅")

        # ================= CURRENT ANIMATION =================
        st.subheader("⚡ Current Flow Animation")

        placeholder = st.empty()

        for frame in range(20):
            fig_anim = go.Figure()

            # Draw static circuit
            for (i, j) in connections:
                x0, y0 = positions[i]
                x1, y1 = positions[j]

                fig_anim.add_trace(go.Scatter(
                    x=[x0, x1],
                    y=[y0, y1],
                    mode='lines',
                    line=dict(width=4)
                ))

                # Animate flow dots
                t = frame / 20
                x_flow = x0 + t * (x1 - x0)
                y_flow = y0 + t * (y1 - y0)

                fig_anim.add_trace(go.Scatter(
                    x=[x_flow],
                    y=[y_flow],
                    mode='markers',
                    marker=dict(size=10),
                    showlegend=False
                ))

            fig_anim.update_layout(height=400)
            placeholder.plotly_chart(fig_anim, use_container_width=True)
            time.sleep(0.05)

    except:
        st.error("Solver failed")
