import pandas as pd
import os

def compute_relative_humidity(temp_c, dew_point_c):
    """Compute relative humidity (%) from temperature and dew point (both in Celsius)."""
    e_t = 6.11 * 10**((7.5 * temp_c) / (237.7 + temp_c))
    e_td = 6.11 * 10**((7.5 * dew_point_c) / (237.7 + dew_point_c))
    rh = 100 * (e_td / e_t)
    return rh

def load_weather_data():
    folder_path = os.path.dirname(__file__)
    # r"C:\Users\Besitzer\Simulation\AJ_Project\webAppCycle"
    weather_data = {}

    for day in range(1, 31):
        file_name = f"{day}july.xlsx"
        file_path = os.path.join(folder_path, file_name)
        
        df = pd.read_excel(file_path)
        df = df[['time', 'temp', 'dwpt']].copy()
        df.rename(columns={'time': 'Hour', 'temp': 'Temperature', 'dwpt': 'Dew Point'}, inplace=True)

        if not pd.api.types.is_numeric_dtype(df['Hour']):
            df['Hour'] = pd.to_datetime(df['Hour']).dt.hour

        df['Relative Humidity (%)'] = compute_relative_humidity(df['Temperature'], df['Dew Point'])

        weather_data[f"2024-07-{day:02d}"] = df

    return weather_data
