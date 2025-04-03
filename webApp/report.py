import streamlit as st
import datetime
from io import StringIO

# === LATEX REPORT GENERATION ===
def generate_latex_report(fluid_name, Pr, delta_end, delta_t_end, Re_end):
    return rf"""
    \documentclass[12pt]{{article}}
    \usepackage[a4paper,margin=1in]{{geometry}}
    \usepackage{{graphicx}}
    \usepackage{{amsmath}}
    \usepackage{{hyperref}}
    \usepackage{{longtable}}
    \title{{Laminar Forced Convection Boundary Layer Report}}
    \date{{\today}}
    \begin{{document}}
    \maketitle

    \section*{{Problem Description}}
    We investigate laminar boundary layer development along a vertical flat plate subjected to external forced convection. The plate is maintained at a uniform surface temperature of 60~\textdegree{{}}C, while the free-stream fluid ({fluid_name}) enters at 40~\textdegree{{}}C with a controllable velocity. This is relevant in oil cooling, electronics, and heat exchanger design.

    \section*{{Research Questions}}
    \begin{{itemize}}
        \item How do $\delta(x)$, $\delta_t(x)$, and $Re_x$ vary with $x$?
        \item How does the fluid type affect boundary layer growth?
        \item How do fluid properties affect Prandtl number and boundary layer profiles?
        \item Is the flow laminar over the plate length?
        \item What are the values at $x = 36$~mm?
    \end{{itemize}}

    \section*{{Methods and Formulas}}
    \textbf{{Fluid:}} {fluid_name}\\
    \textbf{{Prandtl Number:}} {Pr:.1f}\\
    \textbf{{Thermal Diffusivity:}} $\alpha = \frac{{k}}{{\rho c_p}}$\\
    \textbf{{Boundary Layer Thicknesses:}}
    \begin{{align*}}
        Re_x &= \frac{{Ux}}{{\nu}} \\
        \delta(x) &= 5.0 \sqrt{{\frac{{\nu x}}{{U}}}} \\
        \delta_t(x) &= \frac{{\delta(x)}}{{Pr^{{1/3}}}}
    \end{{align*}}

    \section*{{Results at x = 36 mm}}
    \begin{{longtable}}{{|l|c|}}
        \hline
        Quantity & Value \\
        \hline
        Reynolds Number $Re_x$ & {Re_end:.1f} \\
        Velocity BL $\delta(x)$ & {delta_end*1000:.2f}~mm \\
        Thermal BL $\delta_t(x)$ & {delta_t_end*1000:.2f}~mm \\
        Prandtl Number $Pr$ & {Pr:.1f} \\
        \hline
    \end{{longtable}}

    \section*{{Discussion}}
    For {fluid_name}, the boundary layers grow with $x$. High Prandtl numbers (like in oil) cause $\delta_t \ll \delta$. This difference influences thermal design: oil systems experience sharp thermal gradients.

    \section*{{Conclusion}}
    \begin{{itemize}}
        \item Velocity and thermal boundary layers grow downstream.
        \item Prandtl number controls relative thickness.
        \item Laminar flow persists through the plate.
        \item Design must consider fluid-specific heat and momentum diffusion.
    \end{{itemize}}
    \end{{document}}
    """

# === LIVE HTML REPORT (INLINE, WITH MATHJAX & FIXED LATEX) ===
def show_html_report(fluid_name, Pr, delta_end, delta_t_end, Re_end, fig1=None, fig2=None):
    st.markdown("## 📘 Live Technical Report")
    st.markdown(
        f"**Fluid:** {fluid_name} &nbsp;&nbsp;&nbsp; "
        f"**Pr:** {Pr:.1f} &nbsp;&nbsp;&nbsp; "
        f"**Reₓ:** {Re_end:.1f} &nbsp;&nbsp;&nbsp; "
        f"**δ:** {delta_end*1000:.2f} mm &nbsp;&nbsp;&nbsp; "
        f"**δₜ:** {delta_t_end*1000:.2f} mm"
    )

    st.markdown("### 🔍 Problem Description")
    st.markdown(
        f"We investigate laminar boundary layer development along a flat plate with a "
        f"surface temperature of 60 °C. The fluid ({fluid_name}) enters at 40 °C with a set velocity. "
        f"The goal is to understand boundary layer thicknesses."
    )

    st.markdown("### 📊 Methods and Results")
    st.latex(r"Re_x = \frac{Ux}{\nu} \approx " + f"{Re_end:.1f}")
    st.latex(r"\delta(x) \approx " + f"{delta_end*1000:.2f}" + r"\,\text{mm}")
    st.latex(r"\delta_t(x) = \frac{\delta(x)}{Pr^{1/3}} \approx " + f"{delta_t_end*1000:.2f}" + r"\,\text{mm}")

    st.markdown("### 🧠 Conclusion")
    st.markdown(
        "The flow remains laminar. For high-Pr fluids like oil, "
        r"$\delta_t \ll \delta$. For air, $\delta_t$ can be thicker. "
        "Understanding this helps engineers design more efficient cooling surfaces."
    )

    # Optional: LaTeX download
    tex_string = generate_latex_report(fluid_name, Pr, delta_end, delta_t_end, Re_end)
    st.download_button(
        label="📄 Download LaTeX (.tex) Report",
        data=tex_string,
        file_name="boundary_layer_report.tex",
        mime="text/plain"
    )
