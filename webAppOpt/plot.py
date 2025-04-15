# plot.py

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from simulation import (
    compute_rayleigh,
    compute_nusselt_elenbaas,
    compute_h,
    compute_surface_area,
    compute_fin_efficiency,
    churchill_chu,
    get_fluid_props,
    optimize_fin_spacing,
    suggested_spacing,
    oil_data,
    delta_T,
    D, H, k_aluminum, fin_thickness
)

def render_oil_plots():
    st.subheader("📈 Select Oil & Plot Type")

    oil_choice = st.selectbox("Select Oil Type", list(oil_data.keys()), key="oil_plot_select")
    plot_options = [
        "Rayleigh Number vs Fin Spacing",
        "Heat Transfer Coefficient vs Fin Spacing",
        "Surface Area vs Fin Spacing",
        "Heat Transfer Rate vs Fin Spacing",
        "Nusselt Numbers vs Fin Spacing"
    ]
    selected_plots = st.multiselect("Select plots to display", plot_options)

    props = oil_data[oil_choice]
    fluid = get_fluid_props(props)
    optimal_spacing = optimize_fin_spacing(fluid, delta_T)
    spacing_suggested = suggested_spacing(fluid)

    spacings = np.linspace(0.001, 0.05, 300)
    area_list, eta_list, h_list, Ra_list, Q_list, Nu_list, Nu_base_list, Nu_fins_list = [], [], [], [], [], [], [], []

    Ra_base_D = compute_rayleigh(9.81, fluid['beta'], delta_T, D, fluid['nu'], fluid['alpha'])
    Nu_base_D = churchill_chu(Ra_base_D, fluid['Pr'])
    h_base = compute_h(Nu_base_D, fluid['k'], D)

    for d in spacings:
        Ra_d = compute_rayleigh(9.81, fluid['beta'], delta_T, d, fluid['nu'], fluid['alpha'])
        Nu_d = compute_nusselt_elenbaas(Ra_d, d / H)
        h_d = compute_h(Nu_d, fluid['k'], d)
        A_base, A_total = compute_surface_area(d)
        A_fins = A_total - A_base
        eta = compute_fin_efficiency(h_d, k_aluminum, fin_thickness, H)
        Q = h_d * eta * A_fins * delta_T + h_base * A_base * delta_T
        h_overall = Q / (A_total * delta_T)

        area_list.append(A_total)
        eta_list.append(eta)
        h_list.append(h_overall)
        Ra_list.append(Ra_d)
        Q_list.append(Q)

        Nu_fins = compute_nusselt_elenbaas(Ra_d, d / H)
        Nu_base_list.append(Nu_base_D)
        Nu_fins_list.append(Nu_fins)

    if "Surface Area vs Fin Spacing" in selected_plots:
        fig, ax = plt.subplots()
        ax.plot(spacings, area_list, color='teal')
        ax.axvline(optimal_spacing, color='red', linestyle='--', label='Optimal')
        ax.axvline(spacing_suggested, color='orange', linestyle='--', label='Suggested')
        ax.set_title(f"Surface Area vs Fin Spacing - {oil_choice}")
        ax.set_xlabel("Fin Spacing (m)")
        ax.set_ylabel("Surface Area (m²)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    if "Rayleigh Number vs Fin Spacing" in selected_plots:
        fig, ax = plt.subplots()
        ax.plot(spacings, Ra_list, color='purple')
        ax.axvline(optimal_spacing, color='blue', linestyle='--', label='Optimal')
        ax.axvline(spacing_suggested, color='orange', linestyle='--', label='Suggested')
        ax.set_yscale("log")
        ax.set_title(f"Rayleigh Number vs Fin Spacing - {oil_choice}")
        ax.set_xlabel("Fin Spacing (m)")
        ax.set_ylabel("Rayleigh Number (log scale)")
        ax.legend()
        ax.grid(True, which='both', linestyle='--', alpha=0.7)
        st.pyplot(fig)

    if "Heat Transfer Rate vs Fin Spacing" in selected_plots:
        fig, ax = plt.subplots()
        ax.plot(spacings, Q_list, color='green')
        ax.axvline(optimal_spacing, color='red', linestyle='--', label='Optimal')
        ax.axvline(spacing_suggested, color='orange', linestyle='--', label='Suggested')
        ax.axhline(350, color='black', linestyle=':', label='Target Q = 350 W')
        ax.set_title(f"Heat Transfer Rate Q vs Fin Spacing - {oil_choice}")
        ax.set_xlabel("Fin Spacing (m)")
        ax.set_ylabel("Q (W)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    if "Heat Transfer Coefficient vs Fin Spacing" in selected_plots:
        fig, ax = plt.subplots()
        ax.plot(spacings, h_list, color='darkred')
        ax.axvline(optimal_spacing, color='red', linestyle='--', label='Optimal')
        ax.axvline(spacing_suggested, color='orange', linestyle='--', label='Suggested')
        ax.set_title(f"Heat Transfer Coefficient vs Fin Spacing - {oil_choice}")
        ax.set_xlabel("Fin Spacing (m)")
        ax.set_ylabel("h (W/m²·K)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    if "Nusselt Numbers vs Fin Spacing" in selected_plots:
        fig, ax = plt.subplots()
        ax.plot(spacings, Nu_base_list, label='Nu_base (D)', color='blue')
        ax.plot(spacings, Nu_fins_list, label='Nu_fins (spacing)', color='green')
        ax.axvline(optimal_spacing, color='red', linestyle='--', label='Optimal')
        ax.axvline(spacing_suggested, color='orange', linestyle='--', label='Suggested')
        ax.axhline(1, color='black', linestyle=':', label='Nu = 1')
        ax.set_title(f"Nu_base and Nu_fins vs Fin Spacing - {oil_choice}")
        ax.set_xlabel("Fin Spacing (m)")
        ax.set_ylabel("Nusselt Number")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
