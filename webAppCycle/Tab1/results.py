import streamlit as st

def show_parameter_descriptions():
    with st.expander("📘 Parameter Descriptions"):
        st.markdown("""
        ### 🔹 User Input Parameters
        - **floor_area**: Total area of the room floor (m²).
        - **room_height**: Height of the room (m).
        - **window_orientation**: Direction windows are facing (e.g., South).
        - **num_lamps**: Number of lamps in the room.
        - **num_computers**: Number of computers.
        - **num_people**: Number of people occupying the room.

        ### 🔹 Computed Parameters
        - **wall_area**: Total wall area, minus window area, calculated based on floor area and room height.

        ### 🔹 Constant Parameters
        - **ventilation_rate**: Air change rate due to mechanical ventilation (1/hr).
        - **window_u_value**: Thermal transmittance of the windows (W/m²·K).
        - **window_area**: Glazed window surface area (m²).
        - **floor_u_value**: Thermal transmittance of the floor (W/m²·K).
        - **shading_coefficient**: Shading reduction factor (unitless).
        - **wall_u_value**: Thermal transmittance of the walls (W/m²·K).
        - **sensible_gain_per_person**: Heat gain from one person (W).
        - **sensible_gain_per_lamp**: Heat gain from one lamp (W).
        - **roof_u_value**: Thermal transmittance of the roof (W/m²·K).
        - **sensible_gain_per_computer**: Heat gain from one computer (W).
        - **window_shgc**: Solar heat gain coefficient of window glazing (unitless).
        - **infiltration_rate_night**: Night-time infiltration rate (1/hr).
        - **infiltration_rate_day**: Daytime infiltration rate (1/hr).
        - **latent_gain_per_person**: Latent heat gain from one person (W).
        - **indoor_set_temp**: Target indoor temperature (°C).
        - **ventilation_schedule**: Schedule for ventilation (fixed as 'Day').
        - **initial_indoor_rh**: Initial indoor relative humidity (%).
        - **ac_runtime_schedule**: Operating hours of AC system (e.g., 9–17).
        - **latent_heat_vaporization**: Heat required to vaporize water (kJ/kg).
        - **occupancy_schedule**: Occupancy schedule of the room.
        - **specific_heat_air**: Specific heat of air (kJ/kg·K).
        - **air_density**: Density of air (kg/m³).
        """)

    with st.expander("📄 ASHRAE 62.1 Dew Point Limit Explanation"):
        st.markdown(r"""
```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{enumitem}
\usepackage{hyperref}

\title{ASHRAE 62.1 Dew Point Limit and Its Importance}
\author{}
\date{}

\begin{document}

\maketitle

\section*{ASHRAE 62.1 Dew Point Limit}

According to Addendum ae to ASHRAE Standard 62.1-2016, mechanically cooled buildings must be equipped with dehumidification systems that limit the indoor air dew point to a maximum of 60\textdegree F (15.6\textdegree C) during both occupied and unoccupied hours, especially when the outdoor air dew point exceeds this value. This requirement aims to reduce the risk of microbial growth by controlling the amount of moisture available for condensation or absorption on building surfaces.

\section*{Importance of Dew Point Control}

Managing the indoor dew point is essential because:

\begin{itemize}[leftmargin=*, label={--}]
    \item \textbf{Moisture Control:} Limiting the dew point reduces the potential for condensation on cooler surfaces, which can lead to mold growth and structural damage.
    \item \textbf{Indoor Air Quality (IAQ):} Lower dew points help maintain better IAQ by minimizing conditions favorable to allergens and microbial proliferation.
    \item \textbf{Energy Efficiency:} Proper humidity control can enhance HVAC system efficiency by reducing the latent load, leading to energy savings.
\end{itemize}

\section*{Exceptions and Considerations}

There are exceptions to the dew point limit requirement:

\begin{itemize}[leftmargin=*, label={--}]
    \item \textbf{Non-Mechanically Cooled Spaces:} Buildings or spaces without mechanical cooling equipment are exempt, as their surfaces typically remain warmer, reducing condensation risks.
    \item \textbf{Special Use Areas:} Spaces designed to handle higher humidity levels, such as shower rooms or swimming pool enclosures, may be exempt if they utilize materials and systems resistant to moisture damage.
    \item \textbf{Short Unoccupied Periods:} During overnight unoccupied periods not exceeding 12 hours, the 60\textdegree F dew point limit does not apply, provided that indoor relative humidity does not exceed 65\% at any time during those hours.
\end{itemize}

\end{document}
```
        """)
