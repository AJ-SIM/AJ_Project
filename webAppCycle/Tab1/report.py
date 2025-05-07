import streamlit as st
import pandas as pd
import math
from functions import get_default_inputs
from .calculations import calculate_outputs
from plot_weather_data import plot_weather
from vienna_weather_july2024_data import load_weather_data
from .results import show_parameter_descriptions

def display_report():
    st.subheader("Weather Conditions")
    weather_data = load_weather_data()
    selected_date = st.selectbox("Select a date in July 2024:", list(weather_data.keys()))
    daily_weather = weather_data[selected_date]
    avg_temp = round(daily_weather["Temperature"].mean(), 2)

    plot_weather(selected_date)

    from .plot_conditions import render_conditions
    render_conditions(selected_date)


    inputs = get_default_inputs()
    inputs["outdoor_temp_design_db"] = avg_temp

    user_keys = [
        "floor_area", "room_height", "window_orientation",
        "num_lamps", "num_computers", "num_people"
    ]

    user_inputs = {}
    with st.expander("📝 User Input Parameters"):
        with st.form("Editable Inputs"):
            st.markdown("**Use the fields below to configure your room and internal loads.**")
            cols = st.columns(3)
            for i, key in enumerate(user_keys):
                label = key.replace("_", " ").capitalize()
                user_inputs[key] = cols[i % 3].text_input(f"**🛠️ {label}**", value=str(inputs[key]))
            submitted = st.form_submit_button("Recalculate")

    for k in user_inputs:
        try:
            inputs[k] = user_inputs[k] if k == "window_orientation" else float(user_inputs[k])
        except ValueError:
            st.warning(f"Invalid input for {k}. Using default value.")

    room_length = math.sqrt(inputs["floor_area"])
    perimeter = 4 * room_length
    total_wall_area = perimeter * inputs["room_height"]
    wall_area = total_wall_area - inputs["window_area"]
    inputs["wall_area"] = wall_area

    constant_keys = [
        "ventilation_rate", "window_u_value", "window_area", "floor_u_value",
        "shading_coefficient", "wall_u_value", "sensible_gain_per_person",
        "sensible_gain_per_lamp", "roof_u_value", "sensible_gain_per_computer",
        "window_shgc", "infiltration_rate_night", "infiltration_rate_day",
        "latent_gain_per_person", "indoor_set_temp", "ventilation_schedule",
        "initial_indoor_rh", "ac_runtime_schedule", "latent_heat_vaporization",
        "occupancy_schedule", "specific_heat_air", "air_density"
    ]

    computed_constants = {"wall_area": round(wall_area, 2)}
    for key in constant_keys:
        computed_constants[key] = inputs[key]

    with st.expander("📋 Computed & Constant Parameters"):
        st.markdown("**This table shows fixed values and calculated geometry results.**")
        df_const = pd.DataFrame(computed_constants.items(), columns=["Parameter", "Value"])
        st.dataframe(df_const.style.set_properties(**{"font-weight": "bold"}))

    if submitted:
        results = calculate_outputs(inputs)
        st.subheader("Calculated Outputs")
        st.dataframe(pd.DataFrame(results.items(), columns=["Output", "Value"]))

    show_parameter_descriptions()
    return inputs
