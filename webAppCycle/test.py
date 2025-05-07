#!/usr/bin/env python3
"""
psychro_chart.py

Generate a psychrometric chart using psychrochart.
Highlight an optimal comfort point,
overlay the summer comfort zone as a shaded region,
draw the critical dew-point line, and style axes for clarity.

All RH inputs are in percent and converted to fraction for calculations.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import psychrolib
from psychrochart import PsychroChart

def main():
    # Initialize PsychroLib with SI units and define ambient pressure
    psychrolib.SetUnitSystem(psychrolib.SI)
    pressure = 101325.0  # Pa

    # Create the psychrometric chart
    chart = PsychroChart.create()
    chart.config.chart_params.with_zones = False
    chart.config.chart_params.with_constant_h = True
    ax = chart.plot()

    # Define the summer comfort zone in temperature and RH (percent)
    T_min, T_max = 23.0, 26.0
    RH_min_pct, RH_max_pct = 30, 60

    # Convert RH percent to fraction for psychrolib functions
    rh_min = RH_min_pct / 100.0
    rh_max = RH_max_pct / 100.0

    # Define comfort zone corners based on humidity ratio
    corners = [
        (T_min, 1000 * psychrolib.GetHumRatioFromRelHum(T_min, rh_min, pressure)),
        (T_min, 1000 * psychrolib.GetHumRatioFromRelHum(T_min, rh_max, pressure)),
        (T_max, 1000 * psychrolib.GetHumRatioFromRelHum(T_max, rh_max, pressure)),
        (T_max, 1000 * psychrolib.GetHumRatioFromRelHum(T_max, rh_min, pressure)),
    ]

    # Draw comfort zone with transparent fill
    comfort_patch = Polygon(
        corners,
        closed=True,
        facecolor='skyblue',
        edgecolor='blue',
        alpha=0.3,
        linewidth=1.0,
        zorder=0
    )
    ax.add_patch(comfort_patch)

    # Add label inside comfort zone
    label_x = (T_min + T_max) / 2
    label_y = psychrolib.GetHumRatioFromRelHum(label_x, (rh_min + rh_max) / 2, pressure)
  
    # Plot the optimal comfort point (green triangle, smaller size)
    RH_opt_pct = 50
    chart.plot_points_dbt_rh({
        'Optimal Comfort': {
            'xy': (24.5, RH_opt_pct),
            'style': {'marker': '^', 'color': 'green', 'markersize': 12},
            'label': f'Optimal ({RH_opt_pct} %)'
        }
    })

    # Annotate the optimal comfort point
    w_opt = psychrolib.GetHumRatioFromRelHum(24.5, RH_opt_pct / 100.0, pressure)

    # Add caption in the top-left corner for the optimal point
    ax.text(
        0.01, 0.98,
        "Green triangle shows optimal\ncomfort point: 24.5°C, 50% RH",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        horizontalalignment='left',
        color='white',
        bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.3')
    )

    # Add another caption below, describing the shaded polygon
    ax.text(
        0.01, 0.93,
        "Shaded polygon is comfort zone:\n23–26°C, 30–60% RH",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='top',
        horizontalalignment='left',
        color='white',
        bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.3')
    )

    # Draw a horizontal line at the dew point (16.8°C)
    dewpt = 16.8
    w_crit = 1000*psychrolib.GetHumRatioFromRelHum(dewpt, 1.0, pressure)
    ax.hlines(
        w_crit,
        chart.config.limits.range_temp_c[0],
        chart.config.limits.range_temp_c[1],
        linestyles='--', linewidth=1.5, color='blue'
    )
    ax.text(
        chart.config.limits.range_temp_c[0] + 0.2,
        w_crit + 0.0005,
        f'Dew point {dewpt}°C',
        color='blue'
    )

    # Remove any legend
    lg = ax.get_legend()
    if lg:
        lg.remove()

    # Style axes and title in white for dark backgrounds
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('white')

    # Save and display the chart
    fig = ax.get_figure()
    fig.savefig('psychrochart_final.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    main()