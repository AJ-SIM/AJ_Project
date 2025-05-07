# calculations.py
import math

def calculate_outputs(inputs):
    outputs = {}

    # Geometry
    outputs["room_volume"] = inputs["floor_area"] * inputs["room_height"]

    # Envelope Transmission Gains (simplified for steady-state ΔT)
    delta_t = inputs["outdoor_temp_design_db"] - inputs["indoor_set_temp"]
    outputs["Q_trans_wall"] = inputs["wall_u_value"] * inputs["wall_area"] * delta_t
    outputs["Q_trans_roof"] = inputs["roof_u_value"] * inputs["floor_area"] * delta_t
    outputs["Q_trans_floor"] = inputs["floor_u_value"] * inputs["floor_area"] * delta_t
    outputs["Q_trans_windows"] = inputs["window_u_value"] * inputs["window_area"] * delta_t

    # Solar Gains
    solar_radiation = 500  # W/m² default (can be added to inputs)
    sunshine_hours = 4
    outputs["Q_solar"] = solar_radiation * inputs["window_area"] * inputs["shading_coefficient"] * sunshine_hours

    # Internal Gains
    outputs["Q_int_sensible_total"] = (
        inputs["num_people"] * inputs["sensible_gain_per_person"] +
        inputs["num_computers"] * inputs["sensible_gain_per_computer"] +
        inputs["num_lamps"] * inputs["sensible_gain_per_lamp"]
    )
    outputs["Q_int_latent_total"] = inputs["num_people"] * inputs["latent_gain_per_person"]

    # Total Cooling Loads
    outputs["sensible_cooling_load"] = (
        outputs["Q_trans_wall"] + outputs["Q_trans_roof"] + outputs["Q_trans_floor"] +
        outputs["Q_trans_windows"] + outputs["Q_solar"] + outputs["Q_int_sensible_total"]
    )
    outputs["latent_cooling_load"] = outputs["Q_int_latent_total"]  # Extend to include infiltration
    outputs["total_cooling_load"] = outputs["sensible_cooling_load"] + outputs["latent_cooling_load"]

    # SHR
    outputs["shr"] = outputs["sensible_cooling_load"] / outputs["total_cooling_load"]

    return outputs
