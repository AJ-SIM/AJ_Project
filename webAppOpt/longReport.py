from simulation import T_s, T_c, delta_T, D, H, W, fin_thickness, N_r, N_c

def generate_latex_report(fluid_data, results_summary, constants):
    film_temp = (constants['T_s'] + constants['T_c']) / 2

    def num(name, value):
        return f"{value:.2f}" if isinstance(value, float) else str(value)

    def tex_table(tabular_content):
        return """\n\begin{tabular}{" + "l" * len(tabular_content[0]) + "}\n\toprule\n" + \
               " \\\n".join([" & ".join(row) for row in tabular_content]) + \
               " \\\n\\bottomrule\n\\end{tabular}\n"

    # Insert data-dependent tables dynamically
    def spacing_table():
        rows = [[oil,
                 num('opt', results_summary['spacing_opt'][i]),
                 num('sug', results_summary['spacing_suggested'][i])]
                for i, oil in enumerate(results_summary['Oil'])]
        return tex_table([["Oil", "$S_{\\text{opt}}$ (mm)", "$S_{\\text{suggested}}$ (mm)"]] + rows)

    def heat_table():
        rows = [[oil,
                 num('no', results_summary['Q_no_fin'][i]),
                 num('opt', results_summary['Q_opt'][i]),
                 num('sug', results_summary['Q_suggested'][i])]
                for i, oil in enumerate(results_summary['Oil'])]
        return tex_table([["Oil", "$Q_{\\text{no-fin}}$ (W)", "$Q_{\\text{opt}}$ (W)", "$Q_{\\text{suggested}}$ (W)"]] + rows)

    def h_table():
        rows = [[oil,
                 num('h0', results_summary['h_no_fin'][i]),
                 num('h1', results_summary['h_opt'][i]),
                 num('h2', results_summary['h_suggested'][i])]
                for i, oil in enumerate(results_summary['Oil'])]
        return tex_table([["Oil", "$h_{\\text{no-fin}}$ (W/m$^2$K)", "$h_{\\text{opt}}$", "$h_{\\text{suggested}}$"]] + rows)

    def eta_table():
        rows = [[oil,
                 num('eta1', results_summary['eta_opt'][i]),
                 num('eta2', results_summary['eta_suggested'][i])]
                for i, oil in enumerate(results_summary['Oil'])]
        return tex_table([["Oil", "$\\eta_{\\text{opt}}$ (%)", "$\\eta_{\\text{suggested}}$ (%)"]] + rows)

    def fluid_property_table():
        rows = [[
            oil,
            f"{props['nu']:.1e}",
            f"{props['beta']:.1e}",
            f"{props['rho']}",
            f"{props['c_p']}",
            f"{props['alpha']:.2e}",
            f"{props['Pr']:.2f}",
            f"{props['k']}"
        ] for oil, props in fluid_data.items()]
        return tex_table([
            ["Oil", "$\\nu$ (m$^2$/s)", "$\\beta$ (1/K)", "$\\rho$ (kg/m$^3$)", "$c_p$ (J/kg$\\cdot$K)",
             "$\\alpha$ (m$^2$/s)", "$Pr$", "$k$ (W/m$\\cdot$K)"]
        ] + rows)

    # Begin LaTeX document (copied content)
    latex_code = r"""
\documentclass[12pt]{article}
\usepackage{amsmath,graphicx,booktabs}
\usepackage[margin=1in]{geometry}

\begin{document}

\title{Natural Convection Heat Exchanger Analysis: Fins Necessity and Oil Selection}
\author{}
\date{\today}
\maketitle

\section{Introduction}
... (full static intro text here) ...

\section{Methodology}

\subsection{Geometry and Setup}
... include full static text ...
\begin{table}[h!]
\centering
\caption{Key geometric parameters and thermal conditions of the heat exchanger.}
\label{tab:geom}
\begin{tabular}{ll}
\toprule
Tube outer diameter, $D$ & """ + str(D) + " m \\
" + \
"Fin height, $H$ & " + str(H) + " m \\
" + \
"Fin width (per side), $W$ & " + str(W) + " m \\
" + \
"Fin thickness, $t$ & " + str(fin_thickness) + " m \\
" + \
"Fin material thermal conductivity, $k_{\text{fin}}$ & 237 W/m$\cdot$K (Aluminum) \\
" + \
"Tube bank arrangement & " + f"{N_r} rows $\times$ {N_c} columns ({N_r * N_c} tubes) \\
" + \
"Tube span length & 0.70 m per tube \\
" + \
"Surface temperature, $T_s$ & " + str(T_s) + " °C \\
" + \
"Ambient (oil bath) temperature, $T_\infty$ & " + str(T_c) + " °C \\
" + \
"Temperature difference, $\Delta T = T_s - T_\infty$ & " + str(delta_T) + " K \\
" + \
"Target heat dissipation, $Q_{\text{target}}$ & 350 W \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Fluid Properties and Prandtl Number}
\begin{table}[h!]
\centering
\caption{Thermophysical properties of Shell Risella oils at $T_f \approx """ + f"{film_temp}" + r"~^\circ\text{C}$.}
\label{tab:properties}
""" + fluid_property_table() + r"""
\end{table}

... continue the full LaTeX document with static content ...

% Results Sections
\section{Results}

\subsection{Optimal vs. Suggested Fin Spacing}
\begin{table}[h!]
\centering
\caption{Optimal and suggested fin spacing for each oil (in mm).}
\label{tab:spacing}
""" + spacing_table() + r"""
\end{table}

\subsection{Heat Transfer Performance Without Fins (Bare Tubes)}
\begin{table}[h!]
\centering
\caption{Bare tube (no fins) convective performance for each oil.}
\label{tab:noFin}
""" + heat_table() + r"""
\end{table}

\subsection{Heat Transfer with Fins – Optimal and Suggested Configurations}
\begin{table}[h!]
\centering
\caption{Comparison of heat transfer performance with and without fins for each oil.}
\label{tab:performance}
""" + h_table() + r"""
\end{table}

\subsection{Fin Efficiency}
\begin{table}[h!]
\centering
\caption{Fin efficiency for each oil with optimal and suggested spacing.}
\label{tab:eta}
""" + eta_table() + r"""
\end{table}

... (continue with static Discussion and Conclusion text) ...

\end{document}
"""

    return latex_code
