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

# --- Title and Description ---
st.title("🧮 Boundary Layer Thickness Calculator")

# --- Full-Page Two-Column Layout ---
left_col, right_col = st.columns([1, 1], gap="Large")

# === LEFT COLUMN: Inputs + Plots ===
with left_col:
    st.markdown("""
    - Adjust the **flow velocity** below.
    - See how the boundary layers change in real-time.
    """)

    # --- User Input ---
    U = st.slider("Flow Velocity (m/s)", min_value=1.0, max_value=100.0, value=1.0, step=1.0)

    # --- Oil Properties at 40°C ---
    k = 0.15              # W/m·K
    rho = 835             # kg/m³
    cp = 2100             # J/kg·K
    nu = 0.0003           # m²/s (kinematic viscosity)
    beta = 0.0009         # 1/K (thermal expansion coefficient)
    alpha = k / (rho * cp)    # m²/s
    Pr = nu / alpha            # Prandtl number

    # --- Calculation ---
    x = np.linspace(0.0001, 0.040, 500)
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
    # Add a horizontal line at a critical Reynolds number (example: 2300 or 5e5)
    fig1.add_shape(
    type="line",
    x0=0, x1=40,  # in mm
    y0=1, y1=1,
    line=dict(color="black", width=1, dash="solid"),
    name='Transition Threshold'
    )
   # Add a dummy trace for legend
    fig1.add_trace(go.Scatter(
    x=[None],
    y=[None],
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
        xaxis_range=[0, 40],
        yaxis_range=[0, 20],
        template="plotly_white",
        autosize=False,
        width=850,
        height=500
    )
    st.plotly_chart(fig1, use_container_width=False)

    # --- Plot 2: Reynolds Number (Interactive) ---
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
        xaxis_range=[0, 40],
        yaxis_range=[0, 5000],
        template="plotly_white",
        autosize=False,
        width=850,
        height=500
    )
    st.plotly_chart(fig2, use_container_width=False)

# === RIGHT COLUMN: Live Report Output ===
with right_col:
    report_data = ReportData("Oil", Pr, delta_end, delta_t_end, Re_end)
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
