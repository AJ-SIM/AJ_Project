# plot_weather_data.py

import streamlit as st
import pandas as pd
import altair as alt
from vienna_weather_july2024_data import load_weather_data

def plot_weather(selected_date: str):
    """Plot temperature and humidity for the selected July 2024 date."""
    weather_data = load_weather_data()

    if selected_date not in weather_data:
        st.warning(f"No weather data found for {selected_date}")
        return

    df = weather_data[selected_date]
    df_melted = df.melt(id_vars="Hour", value_vars=["Temperature", "Relative Humidity (%)"],
                        var_name="Metric", value_name="Value")

    chart = alt.Chart(df_melted).mark_line(
        strokeWidth=3  # Thicker lines
    ).encode(
        x=alt.X('Hour:O', title='Hour of Day'),
        y=alt.Y('Value:Q', title='Value'),
        color=alt.Color('Metric:N', title='Measurement'),
        tooltip=['Hour', 'Metric', 'Value']
    ) + alt.Chart(df_melted).mark_point(
        filled=True,
        size=60  # Thicker points
    ).encode(
        x='Hour:O',
        y='Value:Q',
        color='Metric:N',
        tooltip=['Hour', 'Metric', 'Value']
    )

    chart = chart.properties(
        title=f"Hourly Temperature and Humidity – {selected_date}",
        width=700,
        height=400
    ).configure_title(
        fontSize=18,
        anchor='start',
        font='Helvetica'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
        domain=True,
        domainColor='black',
        domainWidth=2,  # Thicker axis lines
        tickColor='black',
        tickWidth=2
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
