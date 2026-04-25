import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Lorentz Force Direction", layout="wide")
st.title("⚡ Changing Current Direction & Lorentz Force")

# Inputs
I = st.sidebar.slider("Current (I)", 0.0, 10.0, 5.0)
angle = st.sidebar.slider("Current Direction (deg in XY plane)", 0, 360, 90)

# Vectors
# B is fixed on X axis
B_vec = np.array([5.0, 0, 0])
# L rotates in XY plane
rad = np.radians(angle)
L_vec = np.array([np.cos(rad), np.sin(rad), 0]) * 3.0 # Length 3
# F = I * (L x B)
F_vec = I * np.cross(L_vec, B_vec)

# Plotting
fig = go.Figure()

def add_vec(vec, name, color):
    fig.add_trace(go.Scatter3d(x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]], 
                               mode='lines', name=name, line=dict(color=color, width=8)))
    fig.add_trace(go.Cone(x=[vec[0]], y=[vec[1]], z=[vec[2]], 
                          u=[vec[0]], v=[vec[1]], w=[vec[2]], 
                          sizemode="absolute", sizeref=0.5, colorscale=[[0, color], [1, color]]))

add_vec(L_vec, "Current (L)", "blue")
add_vec(B_vec, "Magnetic Field (B)", "green")
add_vec(F_vec, "Force (F)", "red")

fig.update_layout(scene=dict(xaxis=dict(range=[-6,6]), yaxis=dict(range=[-6,6]), zaxis=dict(range=[-6,6])),
                  margin=dict(l=0, r=0, b=0, t=0))

st.plotly_chart(fig, use_container_width=True)

st.write(f"""
### 💡 Understanding the Shift:
- **Magnetic Field ($B$):** Fixed on the X-axis.
- **Current ($L$):** Rotating in the XY-plane.
- **Force ($F$):** Since $\mathbf{L} \times \mathbf{B}$ involves a vector in the XY-plane crossing the X-axis, the result will **always point along the Z-axis** (either positive or negative).
""")
