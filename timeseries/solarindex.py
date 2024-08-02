import numpy as np
import pvlib
from datetime import datetime

def calculate_solar_index(date_time, latitude, longitude, orientation, tilt, temperature, humidity, sun_minutes):
    """Calculate the solar yield index based on sun minutes."""
    # Calculate solar position
    solar_position = pvlib.solarposition.get_solarposition(date_time, latitude, longitude)
    solar_zenith = solar_position['zenith'].values[0]
    solar_azimuth = solar_position['azimuth'].values[0]
    
    # Calculate angle of incidence
    aoi = pvlib.irradiance.aoi(tilt, orientation, solar_zenith, solar_azimuth)
    
    # Assume sun minutes is a fraction of the hour (e.g., 30 minutes = 0.5)
    sun_fraction = sun_minutes / 60
    
    # Assume a maximum possible irradiance (W/m^2) during clear sky conditions
    max_irradiance = 1000  # Example value
    
    # Calculate the irradiance on the plane of the array
    poa_irradiance = pvlib.irradiance.get_total_irradiance(
        tilt, orientation, solar_zenith, solar_azimuth,
        dni=max_irradiance * sun_fraction,
        ghi=max_irradiance * sun_fraction * np.cos(np.radians(solar_zenith)),
        dhi=max_irradiance * sun_fraction * (1 - np.cos(np.radians(solar_zenith))) / 2
    )
    
    # Extract the total plane of array irradiance (poa_global)
    poa_global = poa_irradiance['poa_global']
    
    # Simple model for temperature and humidity effect
    temp_factor = 1 - 0.005 * (temperature - 25)
    humidity_factor = 1 - 0.001 * humidity
    
    # Calculate final index
    solar_index = poa_global * temp_factor * humidity_factor
    
    return solar_index

# Example usage
date_time = datetime(2024, 8, 2, 16, 0)
latitude = 52.52
longitude = 13.405
orientation = 180  # Facing south
tilt = 30  # Typical tilt angle
temperature = 29  # Example temperature in Celsius
humidity = 60  # Example humidity in percentage
sun_minutes = 60  # Example sun minutes in the current hour

solar_index = calculate_solar_index(
    date_time, latitude, longitude, orientation, tilt,
    temperature, humidity, sun_minutes
)

print(f"Solar Index at {date_time}: {solar_index:.2f}")
