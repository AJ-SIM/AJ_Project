# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# from dataclasses import dataclass
# from report import show_html_report

# # --- Page Config ---
# st.set_page_config(page_title="Boundary Layer Calculator", layout="wide")

# # --- Data Structure for Report Inputs ---
# @dataclass
# class ReportData:
#     fluid_name: str
#     Pr: float
#     delta_end: float
#     delta_t_end: float
#     Re_end: float

# # --- Title and Description ---
# st.title("🧮 Boundary Layer Thickness Calculator")

# # --- Full-Page Two-Column Layout ---
# left_col, right_col = st.columns([1, 1], gap="Large")

# # === LEFT COLUMN: Inputs + Plots ===
# with left_col:
#     st.markdown("""
#     - Select the **fluid** and **flow velocity** below.
#     - See how the boundary layers change in real-time.
#     """)

#     # --- Fluid Selection ---
#     fluid_choice = st.selectbox("Select Fluid", options=["Oil", "Air"])

#     if fluid_choice == "Oil":
#         k = 0.15            # W/m·K
#         rho = 835           # kg/m³
#         cp = 2100           # J/kg·K
#         nu = 0.0003         # m²/s
#     else:  # Air
#         k = 0.0267          # W/m·K
#         rho = 1.145         # kg/m³
#         cp = 1005           # J/kg·K
#         nu = 1.62e-5        # m²/s

#     # --- User Input ---
#     U = st.slider("Flow Velocity (m/s)", min_value=1.0, max_value=100.0, value=1.0, step=1.0)

#     # --- Derived Properties ---
#     alpha = k / (rho * cp)
#     Pr = nu / alpha

#     # --- Calculation ---
#     x = np.linspace(0.0001, 0.036, 500)
#     Re_x = U * x / nu
#     delta = 5.0 * np.sqrt(nu * x / U)
#     delta_t = delta / Pr**(1/3)

#     # --- Values for Report ---
#     delta_end = delta[-1]
#     delta_t_end = delta_t[-1]
#     Re_end = Re_x[-1]

#     # --- Plot 1: Boundary Layer Thicknesses (Interactive) ---
#     fig1 = go.Figure()
#     fig1.add_trace(go.Scatter(
#         x=x*1000, y=delta*1000,
#         mode='lines',
#         name='Hydrodynamic BL thickness δ(x)',
#         line=dict(width=4)
#     ))
#     fig1.add_shape(
#         type="line",
#         x0=0, x1=36,
#         y0=1, y1=1,
#         line=dict(color="black", width=1, dash="solid"),
#         name='Reference Line'
#     )
#     fig1.add_trace(go.Scatter(
#         x=[None], y=[None],
#         mode='lines',
#         name='Reference Line (1 mm)',
#         line=dict(color='black', width=1, dash='solid')
#     ))
#     fig1.add_trace(go.Scatter(
#         x=x*1000, y=delta_t*1000,
#         mode='lines',
#         name='Thermal BL thickness δₜ(x)',
#         line=dict(dash='dash', width=4)
#     ))
#     fig1.update_layout(
#         title=f"Boundary Layer Thickness vs x (U = {U} m/s)",
#         xaxis_title="Distance from Leading Edge x (mm)",
#         yaxis_title="Boundary Layer Thickness (mm)",
#         xaxis_range=[0, 36],
#         yaxis_range=[0, 20],
#         template="plotly_white",
#         autosize=False,
#         width=850,
#         height=500
#     )
#     st.plotly_chart(fig1, use_container_width=False)

#     # --- Plot 2: Reynolds Number ---
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(
#         x=x*1000, y=Re_x,
#         mode='lines',
#         name='Reynolds Number',
#         line=dict(width=4)
#     ))
#     fig2.update_layout(
#         title="Reynolds Number vs x",
#         xaxis_title="Distance from Leading Edge x (mm)",
#         yaxis_title="Reynolds Number Reₓ",
#         xaxis_range=[0, 36],
#         yaxis_range=[0, 5000],
#         template="plotly_white",
#         autosize=False,
#         width=850,
#         height=500
#     )
#     st.plotly_chart(fig2, use_container_width=False)

# # === RIGHT COLUMN: Live Report Output ===
# with right_col:
#     report_data = ReportData(fluid_choice, Pr, delta_end, delta_t_end, Re_end)
#     show_html_report(
#         fluid_name=report_data.fluid_name,
#         Pr=report_data.Pr,
#         delta_end=report_data.delta_end,
#         delta_t_end=report_data.delta_t_end,
#         Re_end=report_data.Re_end,
#         fig1=fig1,
#         fig2=fig2
#     )

# # --- Footer ---
# st.markdown("---")
# st.caption("Created with ❤️ using Streamlit")



import streamlit as st
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from report import show_html_report

# --- Page Config ---
st.set_page_config(page_title="Boundary Layer Calculator", layout="wide")

# --- Data Structure for Report Inputs ---
@dataclass
class ReportData:
    fluid_name: str
    Pr: float
    delta_end: float
    delta_t_end: float
    Re_end: float

# --- Viscosity Function for Oil ---
def kinematic_viscosity_oil(T):
    """
    Estimate kinematic viscosity [m²/s] of oil based on temperature using log-log interpolation.
    """
    T1, nu1 = 40, 43.0e-6   # in m²/s
    T2, nu2 = 100, 7.6e-6   # in m²/s
    log_nu1 = np.log10(nu1)
    log_nu2 = np.log10(nu2)
    log_nu_T = log_nu1 + ((T - T1) / (T2 - T1)) * (log_nu2 - log_nu1)
    return 10**log_nu_T

# --- Title and Description ---
st.title("🧮 Boundary Layer Thickness Calculator")

# --- Full-Page Two-Column Layout ---
left_col, right_col = st.columns([1, 1], gap="Large")

# === LEFT COLUMN: Inputs + Plots ===
with left_col:
    st.markdown("""
    - Select the **fluid** and **flow velocity** below.
    - See how the boundary layers change in real-time.
    """)

    # --- Fluid Selection ---
    fluid_choice = st.selectbox("Select Fluid", options=["Oil", "Air"])

    # --- Film Temperature for Oil ---
    if fluid_choice == "Oil":
        T_film = st.slider("Mean Film Temperature (°C)", min_value=20, max_value=100, value=50, step=1)
        k = 0.15            # W/m·K
        rho = 835           # kg/m³
        cp = 2100           # J/kg·K
        nu = kinematic_viscosity_oil(T_film)  # dynamic based on temperature
    else:  # Air
        k = 0.0267          # W/m·K
        rho = 1.145         # kg/m³
        cp = 1005           # J/kg·K
        nu = 1.62e-5        # m²/s

    # --- User Input ---
    U = st.slider("Flow Velocity (m/s)", min_value=1.0, max_value=100.0, value=1.0, step=1.0)

    # --- Derived Properties ---
    alpha = k / (rho * cp)
    Pr = nu / alpha

    # --- Calculation ---
    x = np.linspace(0.0001, 0.036, 500)
    Re_x = U * x / nu
    delta = 5.0 * np.sqrt(nu * x / U)
    delta_t = delta / Pr**(1/3)

    # --- Values for Report ---
    delta_end = delta[-1]
    delta_t_end = delta_t[-1]
    Re_end = Re_x[-1]

    # --- Plot 1: Boundary Layer Thicknesses (Interactive) ---
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=x*1000, y=delta*1000,
        mode='lines',
        name='Hydrodynamic BL thickness δ(x)',
        line=dict(width=4)
    ))
    fig1.add_shape(
        type="line",
        x0=0, x1=36,
        y0=1, y1=1,
        line=dict(color="black", width=1, dash="solid"),
        name='Reference Line'
    )
    fig1.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        name='Reference Line (1 mm)',
        line=dict(color='black', width=1, dash='solid')
    ))
    fig1.add_trace(go.Scatter(
        x=x*1000, y=delta_t*1000,
        mode='lines',
        name='Thermal BL thickness δₜ(x)',
        line=dict(dash='dash', width=4)
    ))
    fig1.update_layout(
        title=f"Boundary Layer Thickness vs x (U = {U} m/s)",
        xaxis_title="Distance from Leading Edge x (mm)",
        yaxis_title="Boundary Layer Thickness (mm)",
        xaxis_range=[0, 36],
        yaxis_range=[0, 20],
        template="plotly_white",
        autosize=False,
        width=850,
        height=500
    )
    st.plotly_chart(fig1, use_container_width=False)

    # --- Plot 2: Reynolds Number ---
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=x*1000, y=Re_x,
        mode='lines',
        name='Reynolds Number',
        line=dict(width=4)
    ))
    fig2.update_layout(
        title="Reynolds Number vs x",
        xaxis_title="Distance from Leading Edge x (mm)",
        yaxis_title="Reynolds Number Reₓ",
        xaxis_range=[0, 36],
        yaxis_range=[0, 5000],
        template="plotly_white",
        autosize=False,
        width=850,
        height=500
    )
    st.plotly_chart(fig2, use_container_width=False)

# === RIGHT COLUMN: Live Report Output ===
with right_col:
    report_data = ReportData(fluid_choice, Pr, delta_end, delta_t_end, Re_end)
    show_html_report(
        fluid_name=report_data.fluid_name,
        Pr=report_data.Pr,
        delta_end=report_data.delta_end,
        delta_t_end=report_data.delta_t_end,
        Re_end=report_data.Re_end,
        fig1=fig1,
        fig2=fig2
    )

# --- Footer ---
st.markdown("---")
st.caption("Created with ❤️ using Streamlit")
