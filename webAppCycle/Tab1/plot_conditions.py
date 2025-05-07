#!/usr/bin/env python3
"""
plot_conditions.py

Render a psychrometric chart with:
 - summer comfort zone (23–26°C, 30–60% RH)
 - optimal comfort point (24.5°C, 50% RH)
 - critical dew-point line at 16.8°C
 - styling for dark background
 - closed black curve connecting hourly points
 - hour labels next to each point
 - four colored dots at 6 AM, 12 PM, 6 PM, 12 AM
 - right-side y-axis
 - separate zoomed‐in figure
"""

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import psychrolib
from psychrochart import PsychroChart
from vienna_weather_july2024_data import load_weather_data
import pandas as pd


def group_hours_into_ranges(hours):
    if not hours:
        return "None"
    hours = sorted(hours)
    ranges = []
    start = prev = hours[0]
    for h in hours[1:]:
        if h == prev + 1:
            prev = h
        else:
            ranges.append((start, prev))
            start = prev = h
    ranges.append((start, prev))
    return ", ".join(f"{s}–{e}" if s != e else f"{s}" for s, e in ranges)


def render_conditions(selected_date: str):
    psychrolib.SetUnitSystem(psychrolib.SI)
    pressure = 101325.0  # Pa

    # --- Main psychrometric chart ---
    chart = PsychroChart.create()
    chart.config.chart_params.with_zones = False
    chart.config.chart_params.with_constant_h = True
    ax = chart.plot()

    # Comfort zone patch
    T_min, T_max = 23.0, 25.0
    RH_min_pct, RH_max_pct = 30, 60
    rh_min, rh_max = RH_min_pct / 100.0, RH_max_pct / 100.0
    corners = [
        (T_min, 1000 * psychrolib.GetHumRatioFromRelHum(T_min, rh_min, pressure)),
        (T_min, 1000 * psychrolib.GetHumRatioFromRelHum(T_min, rh_max, pressure)),
        (T_max, 1000 * psychrolib.GetHumRatioFromRelHum(T_max, rh_max, pressure)),
        (T_max, 1000 * psychrolib.GetHumRatioFromRelHum(T_max, rh_min, pressure)),
    ]
    comfort_patch = Polygon(corners, closed=True,
                            facecolor='skyblue', edgecolor='blue',
                            alpha=0.3, linewidth=1.0, zorder=0)
    ax.add_patch(comfort_patch)

    # Optimal comfort point
    RH_opt_pct = 50
    chart.plot_points_dbt_rh({
        'Optimal Comfort': {
            'xy': (24.5, RH_opt_pct),
            'style': {'marker': '^', 'color': 'green', 'markersize': 12},
            'label': f'Optimal ({RH_opt_pct}%)'
        }
    })

    # Captions — white text on black boxes with white edges, auto‑spaced
    captions = [
        "Green ▲ shows optimal comfort:\n24.5 °C, 50 % RH",
        "Shaded polygon is comfort zone:\n23–25 °C, 30–60 % RH",
        "Colored ● at key times:\n6 AM (red), 12 PM (yellow), 6 PM (blue), 12 AM (green)",
    ]
    base_y = 0.98
    spacing = 0.06
    for i, txt in enumerate(captions):
        ypos = base_y - i * spacing
        ax.text(
            0.01, ypos, txt,
            transform=ax.transAxes,
            fontsize=14,
            fontweight='bold',
            verticalalignment='top',
            horizontalalignment='left',
            color='black',
            bbox=dict(
                facecolor='white',
                edgecolor='white',
                boxstyle='round,pad=0.4',
                alpha=0.7
            )
        )

    # Dew‑point line at 16.8°C
    dewpt = 16.8
    w_crit = 1000 * psychrolib.GetHumRatioFromRelHum(dewpt, 1.0, pressure)
    ax.hlines(w_crit,
              chart.config.limits.range_temp_c[0],
              chart.config.limits.range_temp_c[1],
              linestyles='--', linewidth=1.5, color='blue')
    ax.text(chart.config.limits.range_temp_c[0] + 0.2,
            w_crit + 0.0005,
            f'Dew point {dewpt}°C',
            color='blue')

    # Load and plot daily weather curve
    weather_data = load_weather_data()
    if selected_date not in weather_data:
        st.warning(f"No weather data for {selected_date}")
        return
    daily = weather_data[selected_date]

    # Track hours in comfort zone
    zone_hours = [
        int(r["Hour"])
        for _, r in daily.iterrows()
        if (T_min <= r["Temperature"] <= T_max)
        and (RH_min_pct <= r["Relative Humidity (%)"] <= RH_max_pct)
    ]
    zone_str = group_hours_into_ranges(zone_hours)
    ax.text(0.01, 0.8,
            f"Hours in comfort zone/suggested hours to open the windows: {zone_str}",
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            verticalalignment='top', horizontalalignment='left',
            color='black',
            bbox=dict(
                facecolor='white',
                edgecolor='white',
                boxstyle='round,pad=0.4',
                alpha=0.7))

    points = []
    highlight_hours = {6: 'red', 12: 'yellow', 18: 'blue', 0: 'green'}
    for _, row in daily.iterrows():
        hr = int(row["Hour"])
        temp = row["Temperature"]
        rh_pct = row["Relative Humidity (%)"]
        w = 1000 * psychrolib.GetHumRatioFromRelHum(temp, rh_pct / 100.0, pressure)
        points.append((temp, w))
        ax.text(temp + 0.2, w + 0.0002, f"{hr}", fontsize=8, color='black')
        if hr in highlight_hours:
            ax.plot(temp, w, 'o',
                    color=highlight_hours[hr], markersize=8)

    if points:
        # close the loop
        pts_closed = points + [points[0]]
        xs, ys = zip(*pts_closed)
        ax.plot(xs, ys, color='black', linewidth=1.5)

    # Style axes and spines
    ax.tick_params(colors='black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.title.set_color('black')
    for spine in ax.spines.values():
        spine.set_color('black')
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    if ax.get_legend():
        ax.get_legend().remove()

    ax.set_title(f"Psychrometric Chart – {selected_date}",
                 color="black", pad=12)

    # Render main figure
    fig = ax.get_figure()
    st.pyplot(fig)


if __name__ == "__main__":
    st.title("Vienna July 2024 Weather on Psychrometric Chart")
    date = st.selectbox("Select date:", list(load_weather_data().keys()))
    render_conditions(date)
