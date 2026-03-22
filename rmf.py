  import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("Rotating Magnetic Field (RMF) Simulator")
st.markdown("Observe how three stationary coils fed by 3-phase currents create a rotating field.")

# Set up the controls side-by-side
col1, col2 = st.columns([1, 4])
with col1:
    st.write("") # Spacing
    st.write("")
    play_button = st.button("▶ Play 1 Full Rotation", use_container_width=True)
with col2:
    manual_angle = st.slider("Manual Control (Electrical Angle ωt)", 0, 360, 0, 5)

# Create an empty container that we will overwrite rapidly during the animation
plot_placeholder = st.empty()

# We wrap the math and plotting in a function so we can call it inside a loop
def generate_rmf_plot(omega_t_deg):
    omega_t = np.deg2rad(omega_t_deg)
    Im = 1.0 

    # 1. Time Domain Currents
    ia = Im * np.cos(omega_t)
    ib = Im * np.cos(omega_t - np.deg2rad(120))
    ic = Im * np.cos(omega_t - np.deg2rad(240))

    # 2. Space Domain Orientations
    dir_a = np.exp(1j * 0)                  
    dir_b = np.exp(1j * np.deg2rad(120))    
    dir_c = np.exp(1j * np.deg2rad(240))    

    # 3. Individual Magnetic Field Vectors
    Ba = ia * dir_a
    Bb = ib * dir_b
    Bc = ic * dir_c

    # 4. Resultant Vector
    B_net = Ba + Bb + Bc

    # --- Plotting ---
    fig = plt.figure(figsize=(14, 6))

    ax1 = plt.subplot(121)
    t_arr = np.linspace(0, 2*np.pi, 360)
    ax1.plot(np.rad2deg(t_arr), Im * np.cos(t_arr), color='red', label=r'Phase A ($i_a$)')
    ax1.plot(np.rad2deg(t_arr), Im * np.cos(t_arr - np.deg2rad(120)), color='blue', label=r'Phase B ($i_b$)')
    ax1.plot(np.rad2deg(t_arr), Im * np.cos(t_arr - np.deg2rad(240)), color='green', label=r'Phase C ($i_c$)')
    ax1.axvline(x=omega_t_deg, color='black', linestyle='--', linewidth=2, label='Current Snapshot')

    ax1.set_title("3-Phase Currents (Time Domain)", fontsize=14)
    ax1.set_xlabel("Electrical Angle ωt (degrees)")
    ax1.set_ylabel("Current Magnitude")
    ax1.set_xlim(0, 360)
    ax1.grid(True, alpha=0.5)
    ax1.legend(loc='upper right')

    ax2 = plt.subplot(122, projection='polar')
    ax2.plot([0, np.angle(Ba)], [0, np.abs(Ba)], color='red', linewidth=3, alpha=0.6, label=r'$\vec{B}_a$')
    ax2.plot([0, np.angle(Bb)], [0, np.abs(Bb)], color='blue', linewidth=3, alpha=0.6, label=r'$\vec{B}_b$')
    ax2.plot([0, np.angle(Bc)], [0, np.abs(Bc)], color='green', linewidth=3, alpha=0.6, label=r'$\vec{B}_c$')
    ax2.plot([0, np.angle(B_net)], [0, np.abs(B_net)], color='black', linewidth=4, label=r'Net Field ($\vec{B}_{net}$)')
    ax2.plot(np.angle(B_net), np.abs(B_net), marker='o', markersize=8, color='black')

    ax2.set_title(f"Resultant Spatial Vector\nMagnitude: {np.abs(B_net):.2f} (Constant at 1.5x Peak)", fontsize=14, pad=20)
    ax2.set_ylim(0, 1.8)
    ax2.set_yticks([0.5, 1.0, 1.5])
    ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    return fig

# --- Execution Logic ---
if play_button:
    # If play is clicked, loop from 0 to 360 degrees
    for angle in range(0, 365, 5):
        fig = generate_rmf_plot(angle)
        plot_placeholder.pyplot(fig) # Push the new frame to the screen
        plt.close(fig) # Clear memory so the app doesn't crash
        time.sleep(0.02) # Pause briefly to control the animation speed
else:
    # If play is NOT clicked, just show a static image based on the slider
    fig = generate_rmf_plot(manual_angle)
    plot_placeholder.pyplot(fig)
    plt.close(fig)

st.markdown("""
### The Takeaway
Notice how the red, blue, and green spatial vectors pulse in and out along their fixed axes, but their sum (the black vector) maintains a perfectly constant length of **1.5** and sweeps smoothly in a circle.
""")
