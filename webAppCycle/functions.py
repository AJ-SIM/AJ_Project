# functions.py

def get_default_inputs():
    return {
        # Room & Envelope Geometry
        "room_area": 50,
        "room_height": 2.4,
        "wall_area": 80,
        "roof_area": 50,
        "floor_area": 50,
        "window_area": 4,
        "window_orientation": "South",

        # Envelope Thermal Properties
        "wall_u_value": 0.35,
        "roof_u_value": 0.25,
        "floor_u_value": 0.3,
        "window_u_value": 1.5,
        "window_shgc": 0.6,
        "shading_coefficient": 0.9,

        # Internal Gains
        "num_people": 5,
        "sensible_gain_per_person": 75,
        "latent_gain_per_person": 55,
        "num_computers": 5,
        "sensible_gain_per_computer": 100,
        "num_lamps": 5,
        "sensible_gain_per_lamp": 60,

        # Ventilation & Infiltration
        "ventilation_rate": 0.35,
        "infiltration_rate_day": 0.5,
        "infiltration_rate_night": 1.0,
        "ventilation_schedule": "Day/Night",

        # Environmental & Design Conditions
        "outdoor_temp_design_db": 35,
        "outdoor_temp_design_wb": 24,
        "outdoor_rh_design": 60,
        "indoor_set_temp": 24,
        "indoor_set_rh": 50,
        "initial_indoor_temp": 29,
        "initial_indoor_rh": 55,

        # HVAC Equipment Specs
        "ac_sensible_capacity": 3.5,
        "ac_latent_capacity": 1.5,
        "ac_efficiency": 3.0,
        "ac_runtime_schedule": "9-17",

        # Psychrometric & Fluid Properties
        "latent_heat_vaporization": 2450,
        "specific_heat_air": 1.005,
        "air_density": 1.2,

        # Simulation Control
        "simulation_days": 7,
        "time_step": 1,
        "occupancy_schedule": "9-17",
        "equipment_schedule": "9-17",
    }

