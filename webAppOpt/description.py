import streamlit as st

def render_description(fluid_data: dict, results_summary: dict, constants: dict):
    film_temp = (constants['T_s'] + constants['T_c']) / 2

    # === SECTION 1: PROBLEM DEFINITION ===
    st.markdown("## 1. Problem Overview")
    st.write("""
        This analysis aims to optimize the fin spacing for a heat exchanger (condenser) to enhance natural convection heat transfer
        when immersed in two types of oil: Shell Risella X 430 and Shell Risella C 415. 
        The objective is to identify both the optimal spacing (using numerical optimization) and a suggested spacing
        (based on empirical formulas), and to compare their impact on thermal performance.
    """)

    # === SECTION 2: GEOMETRY AND PHYSICAL SETUP ===
    st.markdown("## 2. Geometry and Physical Setup")
    st.write("""
The physical model consists of a tube bank with 24 rows and 2 columns, arranged such that the vertical planes are stacked perpendicular to the tube bank.
Aluminum fins are attached to enhance heat transfer. Heat is dissipated from the surface to the surrounding oil through natural convection, which occurs in a crossflow configuration.""")
    st.markdown("**Geometric Specifications:**")
    st.markdown(f"""
        - **Tube Diameter (D):** {constants['D']} m  
        - **Fin Height (H):** {constants['H']} m  
        - **Fin Width (W):** {constants['W']} m  
        - **Fin Thickness (t):** {constants['fin_thickness']} m  
        - **Number of Rows (N_r):** {constants['N_r']}  
        - **Number of Columns (N_c):** {constants['N_c']}  
        - **Fin Material:** Aluminum (thermal conductivity k = 237 W/m·K)
    """)

    st.markdown("**Thermal Conditions:**")
    st.markdown(f"""
        - **Surface Temperature (T_s):** {constants['T_s']} °C  
        - **Ambient Temperature (T_c):** {constants['T_c']} °C  
        - **Temperature Difference (ΔT):** {constants['delta_T']} °C
    """)

    # === SECTION 3: FLUID PROPERTIES ===
       # === SECTION 3: FLUID PROPERTIES ===
    st.markdown(f"## 3. Fluid Properties @ {film_temp:.1f} °C")
    st.markdown("The fluid properties used in the simulation are interpolated at the film temperature.")

    fluid_table = '''
    <table style="width:100%; border-collapse: collapse; text-align: center;">
        <thead>
            <tr style="background-color: #f2f2f2; border-bottom: 1px solid #ccc;">
                <th>Oil</th><th>ν [m²/s]</th><th>β [1/K]</th><th>ρ [kg/m³]</th>
                <th>c_p [J/kg·K]</th><th>α [m²/s]</th><th>Pr</th><th>k [W/m·K]</th>
            </tr>
        </thead>
        <tbody>
    '''
    for oil, props in fluid_data.items():
        fluid_table += f'''
            <tr style="border-bottom: 1px solid #ccc;">
                <td>{oil}</td>
                <td>{props['nu']:.2e}</td>
                <td>{props['beta']}</td>
                <td>{props['rho']}</td>
                <td>{props['c_p']}</td>
                <td>{props['alpha']:.2e}</td>
                <td>{props['Pr']:.2f}</td>
                <td>{props['k']}</td>
            </tr>
        '''
    fluid_table += "</tbody></table>"
    st.components.v1.html(fluid_table, height=100, scrolling=False)


    # === SECTION 4: MATHEMATICAL METHODS ===
    st.markdown("## 4. Methods and Equations")
    st.markdown("### 4.1 Interpolation Method")
    st.write("Log-linear interpolation is applied to estimate the kinematic viscosity at the film temperature.")

    st.markdown("### 4.2 Governing Equations")
    st.markdown("**Rayleigh Number:**")
    st.latex(r"Ra = \frac{g \cdot \beta \cdot \Delta T \cdot d^3}{\nu \cdot \alpha}")

    st.markdown("**Nusselt Number – Finned Surface (Elenbaas):**")
    st.latex(r"Nu = \frac{1}{24} Ra \cdot \frac{S}{L} \left(1 - e^{-\frac{35}{Ra \cdot (S/L)}} \right)^{0.75}")

    st.markdown("**Nusselt Number – Bare Tube (Churchill-Chu):**")
    st.latex(r"Nu = \left[ 0.60 + \frac{0.387 \cdot Ra^{1/6}}{ \left( 1 + \left( \frac{0.559}{Pr} \right)^{9/16} \right)^{8/27} } \right]^2")

    st.markdown("**Heat Transfer Coefficient:**")
    st.latex(r"h = \frac{Nu \cdot k}{d}")

    st.markdown("**Fin Efficiency (Straight Fin of Uniform Cross Section):**")
    st.latex(r"\eta = \frac{\tanh(mL)}{mL}, \quad m = \sqrt{\frac{2h}{k_{\text{fin}} \cdot t}}")

    st.markdown("**Overall Heat Transfer Rate:**")
    st.latex(r"Q = h_{\text{base}} A_{\text{base}} \Delta T + h_{\text{fins}} \eta A_{\text{fins}} \Delta T")

    # === SECTION 5: RESULTS TABLES ===
    def render_table(title, headers, rows):
        html = f"<h4 style='margin-top: 2rem;'>{title}</h4>"
        html += "<table style='width:100%; border-collapse: collapse; text-align: center;'>"
        html += "<thead><tr style='border-bottom: 1px solid #ccc; background-color: #f9f9f9;'>"
        for h in headers:
            html += f"<th style='padding: 6px; border: 1px solid #ccc;'>{h}</th>"
        html += "</tr></thead><tbody>"
        for row in rows:
            html += "<tr>" + "".join([f"<td style='padding: 6px; border: 1px solid #ccc;'>{val}</td>" for val in row]) + "</tr>"
        html += "</tbody></table>"
        return html

    html = "<h3 style='margin-top: 3rem;'>5. Results Summary</h3>"

    rows_spacing = [
        [results_summary['Oil'][i],
         f"{results_summary['spacing_opt'][i]:.2f}",
         f"{results_summary['spacing_suggested'][i]:.2f}"]
        for i in range(len(results_summary['Oil']))
    ]
    html += render_table("5.1 Optimal and Suggested Fin Spacing (mm)", ["Oil", "Optimal", "Suggested"], rows_spacing)

    rows_q = [
        [results_summary['Oil'][i],
         f"{results_summary['Q_no_fin'][i]:.2f}",
         f"{results_summary['Q_opt'][i]:.2f}",
         f"{results_summary['Q_suggested'][i]:.2f}"]
        for i in range(len(results_summary['Oil']))
    ]
    html += render_table("5.2 Heat Transfer Rate (W)", ["Oil", "No Fin", "Optimal", "Suggested"], rows_q)

    rows_h = [
        [results_summary['Oil'][i],
         f"{results_summary['h_no_fin'][i]:.2f}",
         f"{results_summary['h_opt'][i]:.2f}",
         f"{results_summary['h_suggested'][i]:.2f}"]
        for i in range(len(results_summary['Oil']))
    ]
    html += render_table("5.3 Overall Heat Transfer Coefficient h [W/m²·K]", ["Oil", "No Fin", "Optimal", "Suggested"], rows_h)

    rows_eta = [
        [results_summary['Oil'][i],
         f"{results_summary['eta_opt'][i]:.2f}",
         f"{results_summary['eta_suggested'][i]:.2f}"]
        for i in range(len(results_summary['Oil']))
    ]
    html += render_table("5.4 Fin Efficiency η [%]", ["Oil", "Optimal", "Suggested"], rows_eta)

    st.components.v1.html(html, height=1600, scrolling=True)
