import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from report import generate_latex_report
from export_figures import generate_oil_plot_pdf, generate_comparison_bar_pdf
from simulation import (
    oil_data,
    get_fluid_props,
    optimize_fin_spacing,
    suggested_spacing,
    compute_surface_area,
    compute_nusselt_elenbaas,
    compute_h,
    compute_fin_efficiency,
    compute_rayleigh,
    churchill_chu,
    kinematic_viscosity_interp,
    g,
    T_s,
    T_c,
    delta_T,
    T_film,
    k_aluminum,
    D,
    N_r,
    N_c,
    H,
    W,
    L_array,
    fin_thickness,
    spacing_min,
    spacing_max,
    Q_target
)

from description import render_description
from plot import render_oil_plots

st.set_page_config(layout="wide")

st.title("🛠️ Fin Spacing Optimization for Two Oils")

left_col, right_col = st.columns([1, 1], gap="large")

# Prepare results and fluid data
results_summary = {
    'Oil': [],
    'Q_no_fin': [],
    'Q_opt': [],
    'Q_suggested': [],
    'h_no_fin': [],
    'h_opt': [],
    'h_suggested': [],
    'eta_opt': [],
    'eta_suggested': [],
    'spacing_opt': [],
    'spacing_suggested': []
}
fluid_data = {}

for oil_name, props in oil_data.items():
    fluid = get_fluid_props(props)
    fluid_data[oil_name] = fluid

    optimal_spacing = optimize_fin_spacing(fluid, delta_T)
    suggested = suggested_spacing(fluid)
    Ra_base = compute_rayleigh(g, fluid['beta'], delta_T, D, fluid['nu'], fluid['alpha'])
    Nu_base = churchill_chu(Ra_base, fluid['Pr'])
    h_base = compute_h(Nu_base, fluid['k'], D)
    
    A_base = np.pi * D * N_r * N_c * L_array
    Q_no_fin = h_base * A_base * delta_T
    
    Ra_fins_opt = compute_rayleigh(g, fluid['beta'], delta_T, optimal_spacing, fluid['nu'], fluid['alpha'])
    A_base_opt, A_total_opt = compute_surface_area(optimal_spacing)
    A_fins_opt = A_total_opt - A_base_opt
    Nu_fins_opt = compute_nusselt_elenbaas(Ra_fins_opt, optimal_spacing / H)

    h_fins_opt = compute_h(Nu_fins_opt, fluid['k'], optimal_spacing)
    eta_opt = np.tanh(np.sqrt(2 * h_fins_opt / (237 * 0.001)) * 0.5) / (np.sqrt(2 * h_fins_opt / (237 * 0.001)) * 0.5)
    Q_opt = Q_no_fin + h_fins_opt * eta_opt * A_fins_opt * delta_T
    h_opt = Q_opt / (A_total_opt * delta_T)

    A_base_sug, A_total_sug = compute_surface_area(suggested)
    A_fins_sug = A_total_sug - A_base_sug
    Ra_sug = compute_rayleigh(g, fluid['beta'], delta_T, suggested, fluid['nu'], fluid['alpha'])
    Nu_sug = compute_nusselt_elenbaas(Ra_sug, suggested / H)
    h_fins_sug = compute_h(Nu_sug, fluid['k'], suggested)
    # h_fins_sug = fluid['k'] * compute_nusselt_elenbaas(
    #     9.81 * fluid['beta'] * delta_T * suggested**3 / (fluid['nu'] * fluid['alpha']),
    #     suggested / 0.5
    # ) / suggested
    eta_sug = compute_fin_efficiency(h_fins_sug, k_aluminum, fin_thickness, H)

    # eta_sug = np.tanh(np.sqrt(2 * h_fins_sug / (237 * 0.001)) * 0.5) / (np.sqrt(2 * h_fins_sug / (237 * 0.001)) * 0.5)
    Q_sug = Q_no_fin + h_fins_sug * eta_sug * A_fins_sug * delta_T
    h_sug = Q_sug / (A_total_sug * delta_T)

    results_summary['Oil'].append(oil_name)
    results_summary['Q_no_fin'].append(Q_no_fin)
    results_summary['Q_opt'].append(Q_opt)
    results_summary['Q_suggested'].append(Q_sug)
    results_summary['h_no_fin'].append(h_base)
    results_summary['h_opt'].append(h_opt)
    results_summary['h_suggested'].append(h_sug)
    results_summary['eta_opt'].append(eta_opt * 100)
    results_summary['eta_suggested'].append(eta_sug * 100)
    results_summary['spacing_opt'].append(optimal_spacing * 1000)
    results_summary['spacing_suggested'].append(suggested * 1000)

# Constants for display
constants = {
    "T_s": 60,
    "T_c": 45,
    "delta_T": 15,
    "D": 0.01,
    "H": 0.5,
    "W": 0.036,
    "fin_thickness": 0.001,
    "N_r": 24,
    "N_c": 2
}

# === LEFT COLUMN ===
with left_col:
    render_oil_plots()
    st.subheader("🔍 Final Comparison Between Oils")

    labels = results_summary['Oil']
    x = np.arange(len(labels))
    width = 0.22

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Performance Comparison Between Oils")

    axs[0, 0].bar(x - width, results_summary['Q_no_fin'], width, label='No Fin')
    axs[0, 0].bar(x, results_summary['Q_opt'], width, label='Optimal')
    axs[0, 0].bar(x + width, results_summary['Q_suggested'], width, label='Suggested')
    axs[0, 0].set_title('Heat Transfer Q (W)')
    axs[0, 0].set_xticks(x)
    axs[0, 0].set_xticklabels(labels)
    axs[0, 0].legend()
    axs[0, 0].grid(True, linestyle='--', alpha=0.5)

    axs[0, 1].bar(x - width, results_summary['h_no_fin'], width, label='No Fin')
    axs[0, 1].bar(x, results_summary['h_opt'], width, label='Optimal')
    axs[0, 1].bar(x + width, results_summary['h_suggested'], width, label='Suggested')
    axs[0, 1].set_title('Heat Transfer Coefficient h (W/m²·K)')
    axs[0, 1].set_xticks(x)
    axs[0, 1].set_xticklabels(labels)
    axs[0, 1].legend()
    axs[0, 1].grid(True, linestyle='--', alpha=0.5)

    axs[1, 0].bar(x, results_summary['eta_opt'], width, label='Optimal')
    axs[1, 0].bar(x + width, results_summary['eta_suggested'], width, label='Suggested')
    axs[1, 0].set_title('Fin Efficiency η (%)')
    axs[1, 0].set_xticks(x)
    axs[1, 0].set_xticklabels(labels)
    axs[1, 0].legend()
    axs[1, 0].grid(True, linestyle='--', alpha=0.5)

    axs[1, 1].bar(x, results_summary['spacing_opt'], width, label='Optimal')
    axs[1, 1].bar(x + width, results_summary['spacing_suggested'], width, label='Suggested')
    axs[1, 1].set_title('Fin Spacing (mm)')
    axs[1, 1].set_xticks(x)
    axs[1, 1].set_xticklabels(labels)
    axs[1, 1].legend()
    axs[1, 1].grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)

# === RIGHT COLUMN ===
with right_col:
    st.markdown("## 📤 Download Section")

    # Generate LaTeX code
    latex_code = generate_latex_report(fluid_data, results_summary, constants)
    st.download_button(
        label="📥 Download LaTeX Summery (.tex)",
        data=latex_code,
        file_name="15_04_25_AJ_HeatTransfer_finSpacingOptimizationTwoOil_NC_summery.tex",
        mime="text/plain"
    )

    # Oil-specific plots
    for oil_name in results_summary["Oil"]:
        oil_pdf = generate_oil_plot_pdf(oil_name)
        st.download_button(
            label=f"📑 Download {oil_name} Plots PDF",
            data=oil_pdf,
            file_name=f"15_04_25_AJ_HeatTransfer_finSpacingOptimizationTwoOil_NC_{oil_name.replace(' ', '_').lower()}_plots.pdf",
            mime="application/pdf"
        )

    # Bar chart PDF
    comparison_pdf = generate_comparison_bar_pdf(fig)
    st.download_button(
        label="📊 Download Comparison Bar Chart PDF",
        data=comparison_pdf,
        file_name="15_04_25_AJ_HeatTransfer_finSpacingOptimizationTwoOil_NC_bar_comparison.pdf",
        mime="application/pdf"
    )
    # # Load your existing PDF file
    # with open("15_04_25_AJ_HeatTransfer_finSpacingOptimizationTwoOil_NC_finalReport.pdf", "rb") as file:
    #     pdf_data = file.read()

    # # Add a download button for the PDF
    # st.download_button(
    #     label="📄 Download Final Report (PDF)",
    #     data=pdf_data,
    #     file_name="15_04_25_AJ_HeatTransfer_finSpacingOptimizationTwoOil_NC.pdf",
    #     mime="application/pdf"
    # )
    
    # Show description last
    st.markdown("---")
    render_description(fluid_data, results_summary, constants)
