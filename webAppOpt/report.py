# report.py

def generate_latex_report(fluid_data, results_summary, constants):
    film_temp = (constants['T_s'] + constants['T_c']) / 2

    latex = r"""\documentclass[12pt]{article}
\usepackage{amsmath,graphicx,booktabs}
\usepackage[margin=1in]{geometry}
\title{Fin Spacing Optimization Report}
\author{}
\date{}

\begin{document}
\maketitle

\section{Problem Overview}
This analysis aims to optimize the fin spacing for a heat exchanger (condenser) to enhance natural convection heat transfer
when immersed in two types of oil: Shell Risella X 430 and Shell Risella C 415. 
The objective is to identify both the optimal spacing (using numerical optimization) and a suggested spacing
(based on empirical formulas), and to compare their impact on thermal performance.

\section{Geometry and Physical Setup}
The physical model consists of a tube bank with 24 rows and 2 columns...

\begin{itemize}
  \item Tube Diameter (D): """ + f"{constants['D']} m" + r"""
  \item Fin Height (H): """ + f"{constants['H']} m" + r"""
  \item Fin Width (W): """ + f"{constants['W']} m" + r"""
  \item Fin Thickness: """ + f"{constants['fin_thickness']} m" + r"""
  \item Number of Rows: """ + f"{constants['N_r']}" + r"""
  \item Number of Columns: """ + f"{constants['N_c']}" + r"""
  \item Fin Material: Aluminum (k = 237 W/m$\cdot$K)
\end{itemize}

\section{Fluid Properties at """ + f"{film_temp:.1f}" + r""" °C}
\begin{tabular}{lccccccc}
\toprule
Oil & $\nu$ [m$^2$/s] & $\beta$ [1/K] & $\rho$ [kg/m$^3$] & $c_p$ [J/kg$\cdot$K] & $\alpha$ [m$^2$/s] & Pr & $k$ [W/m$\cdot$K] \\
\midrule
"""

    for oil, props in fluid_data.items():
        latex += f"{oil} & {props['nu']:.2e} & {props['beta']} & {props['rho']} & {props['c_p']} & {props['alpha']:.2e} & {props['Pr']:.2f} & {props['k']} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}

\section{Methods and Equations}
\subsection{Rayleigh Number}
\[
Ra = \frac{g \cdot \beta \cdot \Delta T \cdot d^3}{\nu \cdot \alpha}
\]
\subsection{Nusselt Number - Elenbaas}
\[
Nu = \frac{1}{24} Ra \cdot \frac{S}{L} \left(1 - e^{-\frac{35}{Ra \cdot (S/L)}} \right)^{0.75}
\]
\subsection{Heat Transfer Rate}
\[
Q = h_{\text{base}} A_{\text{base}} \Delta T + h_{\text{fins}} \eta A_{\text{fins}} \Delta T
\]

\section{Results}
"""

    def table(title, header, rows):
        tex = f"\\subsection*{{{title}}}\n\\begin{{tabular}}{{{'c' * len(header)}}}\n\\toprule\n"
        tex += " & ".join(header) + " \\\\\n\\midrule\n"
        for row in rows:
            tex += " & ".join(row) + " \\\\\n"
        tex += "\\bottomrule\n\\end{tabular}\n"
        return tex

    tex_tables = [
        ("Fin Spacing (mm)", ["Oil", "Optimal", "Suggested"], [
            [results_summary['Oil'][i],
             f"{results_summary['spacing_opt'][i]:.2f}",
             f"{results_summary['spacing_suggested'][i]:.2f}"]
            for i in range(len(results_summary['Oil']))
        ]),
        ("Heat Transfer Q (W)", ["Oil", "No Fin", "Optimal", "Suggested"], [
            [results_summary['Oil'][i],
             f"{results_summary['Q_no_fin'][i]:.2f}",
             f"{results_summary['Q_opt'][i]:.2f}",
             f"{results_summary['Q_suggested'][i]:.2f}"]
            for i in range(len(results_summary['Oil']))
        ]),
        ("Heat Transfer Coefficient h (W/m$^2$$\cdot$K)", ["Oil", "No Fin", "Optimal", "Suggested"], [
            [results_summary['Oil'][i],
             f"{results_summary['h_no_fin'][i]:.2f}",
             f"{results_summary['h_opt'][i]:.2f}",
             f"{results_summary['h_suggested'][i]:.2f}"]
            for i in range(len(results_summary['Oil']))
        ]),
        ("Fin Efficiency $\eta$ [\\%]", ["Oil", "Optimal", "Suggested"], [
            [results_summary['Oil'][i],
             f"{results_summary['eta_opt'][i]:.2f}",
             f"{results_summary['eta_suggested'][i]:.2f}"]
            for i in range(len(results_summary['Oil']))
        ]),
    ]

    for title, header, rows in tex_tables:
        latex += table(title, header, rows)

    latex += r"\end{document}"
    return latex
import subprocess
import tempfile
import os

def export_report_pdf(latex_code: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "report.tex")
        pdf_path = os.path.join(tmpdir, "report.pdf")

        with open(tex_path, "w") as f:
            f.write(latex_code)

        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_path],
                cwd=tmpdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError("LaTeX compilation failed") from e

        with open(pdf_path, "rb") as f:
            return f.read()
