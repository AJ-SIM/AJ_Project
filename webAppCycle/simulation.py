
from vienna_weather_july2024_data import (load_weather_data)

import pickle

# Example: your data
weather_data = load_weather_data()  # in your case from simulation.py

# Save to a file
with open('weather_data.pkl', 'wb') as f:
    pickle.dump(weather_data, f)

import pickle

# Load from the file
with open('weather_data.pkl', 'rb') as f:
    weather_data = pickle.load(f)

# Now weather_data is ready!
print(weather_data['2024-07-01'])  # Same as before
