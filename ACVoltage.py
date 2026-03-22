import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="AC Generator Principle", layout="centered")

st.title("AC Generator Principle")
st.markdown("""
This interactive simulation demonstrates the principle of an AC generator. 
Adjust the slider to rotate the rectangular coil within the uniform magnetic field and observe how the velocity vectors of the arms ($a, b$ and $c, d$) affect the induced e.m.f.
""")

# --- Interactive Slider ---
theta_deg = st.slider("Rotate Coil Angle (θ) in Degrees", min_value=0, max_value=360, value=0, step=5)

# Calculate radians
theta = np.radians(theta_deg)

# --- Figure Setup ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [2, 1]})
plt.subplots_adjust(hspace=0.3)

# ==========================================
# Top Plot: The Generator Cross-Section
# ==========================================

# 1. Draw North and South Poles
ax1.add_patch(plt.Rectangle((-2.5, 2.5), 5, 1.5, color='lightgray', ec='black', lw=1.5))
ax1.text(0, 3.25, 'N', fontsize=24, ha='center', va='center', fontweight='bold', color='#333333')

ax1.add_patch(plt.Rectangle((-2.5, -4.0), 5, 1.5, color='lightgray', ec='black', lw=1.5))
ax1.text(0, -3.25, 'S', fontsize=24, ha='center', va='center', fontweight='bold', color='#333333')

# 2. Draw Magnetic Field Lines (N to S)
for x in np.linspace(-2.0, 2.0, 7):
    ax1.arrow(x, 2.5, 0, -4.8, head_width=0.15, head_length=0.2, 
              fc='gray', ec='gray', linestyle='--', alpha=0.6, length_includes_head=True)

# 3. Define Coil Parameters
r = 1.8 # Radius of the rotation path
x_ab, y_ab = r * np.cos(theta), r * np.sin(theta)
x_cd, y_cd = -r * np.cos(theta), -r * np.sin(theta)

# 4. Draw the Coil
# Connecting rod
ax1.plot([x_cd, x_ab], [y_cd, y_ab], color='black', lw=6, alpha=0.1) 
ax1.plot([x_cd, x_ab], [y_cd, y_ab], color='gray', lw=3) 

# Cross sections of the wire arms
ax1.plot(x_ab, y_ab, 'o', markersize=14, color='white', mec='black', mew=2)
ax1.plot(x_cd, y_cd, 'o', markersize=14, color='white', mec='black', mew=2)

# Wire Labels
ax1.text(x_ab + 0.3, y_ab, 'a, b', fontsize=14, va='center')
ax1.text(x_cd - 0.3, y_cd, 'c, d', fontsize=14, va='center', ha='right')

# 5. Draw Velocity Vectors (Tangent to rotation path)
v_scale = 1.2
# Arm a,b (right side moving counter-clockwise)
vx_ab = -v_scale * np.sin(theta)
vy_ab = v_scale * np.cos(theta)
ax1.arrow(x_ab, y_ab, vx_ab, vy_ab, head_width=0.15, head_length=0.2, 
          fc='blue', ec='blue', lw=2, length_includes_head=True)
ax1.text(x_ab + vx_ab*1.2, y_ab + vy_ab*1.2, 'v', color='blue', fontsize=14, fontweight='bold')

# Arm c,d (left side moving counter-clockwise)
vx_cd = v_scale * np.sin(theta)
vy_cd = -v_scale * np.cos(theta)
ax1.arrow(x_cd, y_cd, vx_cd, vy_cd, head_width=0.15, head_length=0.2, 
          fc='red', ec='red', lw=2, length_includes_head=True)
ax1.text(x_cd + vx_cd*1.2, y_cd + vy_cd*1.2, 'v', color='red', fontsize=14, fontweight='bold')

# 6. Emf Callout Box
# The e.m.f is proportional to the horizontal component of velocity cutting vertical flux lines
if theta_deg % 180 == 0:
    emf_state = "Zero e.m.f."
elif theta_deg % 180 == 90:
    emf_state = "Maximum e.m.f."
else:
    # Indicate direction
    if 0 < theta_deg < 180:
        emf_state = "e.m.f. Increasing/Decreasing"
    else:
        emf_state = "Direction of e.m.f. reversed"

bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="black", lw=1.5)
ax1.text(3.5, 0, f"Angle: {theta_deg}°\n{emf_state}", 
         ha="center", va="center", size=12, bbox=bbox_props)

ax1.set_xlim(-5, 6)
ax1.set_ylim(-4.5, 4.5)
ax1.axis('off')

# ==========================================
# Bottom Plot: The Induced E.M.F Wave
# ==========================================
angles = np.linspace(0, 360, 360)
# e.m.f = B * L * v * sin(theta), simplified to just sin(theta) for the shape
emf_values = np.sin(np.radians(angles))

ax2.plot(angles, emf_values, color='green', lw=2, label="Induced E.M.F.")
ax2.axhline(0, color='black', lw=1)
ax2.axvline(theta_deg, color='gray', linestyle='--', alpha=0.7)

# Plot current position on the wave
current_emf = np.sin(theta)
ax2.plot(theta_deg, current_emf, 'ko', markersize=8)

ax2.set_xlabel("Rotation Angle θ (Degrees)")
ax2.set_ylabel("Induced e.m.f.")
ax2.set_xlim(0, 360)
ax2.set_ylim(-1.5, 1.5)
ax2.set_xticks([0, 90, 180, 270, 360])
ax2.grid(True, alpha=0.3)

# --- Render Plot in Streamlit ---
st.pyplot(fig)
