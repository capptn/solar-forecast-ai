import numpy as np
import pvlib
from datetime import datetime, timedelta
import pandas as pd
from meteostat import Point, Stations, Daily, Hourly
from geopy.distance import geodesic
from weatherforecast import get_wetaher_forecast

def find_nearest_station_with_zsun(latitude, longitude, date):
    # Radius definieren (z.B. 50 km)
    radius = 100  # in kilometers

    # Wetterstationen im Umkreis finden
    stations = Stations()
    stations = stations.nearby(latitude, longitude)

    newstations = stations.fetch(100)

    start = date
    end = date + timedelta(days=1)

    for index, station in newstations.iterrows():

        

        data = Hourly(station['wmo'], start, end)
        data = data.fetch()
        #print(index)
        #print(data)
        if data['tsun'].notna().any():
            print("DIESE STATION LIEFERT DIE WERTE")
            print("Stations-Name", station['name'])
            print("Stations-WMO: ", station['wmo'])
            station_location = (station['latitude'], station['longitude'])
            my_location = (latitude, longitude)
            distance = geodesic(my_location, station_location).kilometers
            print('Stations-Entfernung: ', distance)
        
            if 'tsun' in data.columns:
                tsun_data = data['tsun'].dropna()
                if not tsun_data.empty:
                     return station['wmo']
                else:
                    print('Keine Daten für tsun vorhanden')
            else:
                print('tsun-Spalte nicht gefunden')

def get_weather_data(latitude, longitude, date):
    """Fetch hourly weather data for a specific date using Meteostat."""
    start = date
    end = date + timedelta(days=1)
   
    the_station = find_nearest_station_with_zsun(latitude, longitude, date)
    # Fetch hourly weather data
    data = Hourly(the_station, start, end)
    data = data.fetch()
    #print('DATA: ', data)
    # Extract required data
    temperatures = data['temp'].tolist()
    humidities = data['rhum'].tolist()
    sun_minutes_per_hour = [(60 if x > 0 else 0) for x in data['tsun'].tolist()]  # Assuming coco (cloud cover) 0 means full sun
    
    return temperatures, humidities, sun_minutes_per_hour

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

def calculate_daily_solar_indices(date, latitude, longitude, orientation, tilt):
    """Calculate solar indices for each hour of the given date."""

    date2 = datetime.strptime(date, "%d-%m-%Y")

    #temperatures, humidities, sun_minutes_per_hour = get_weather_data(latitude, longitude, date2)
    sun_minutes_per_hour, temperatures, humidities = get_wetaher_forecast(date2.strftime("%Y-%m-%d") ,latitude, longitude)
    

    print(temperatures)
    print(humidities)
    print(sun_minutes_per_hour)

    indices = []
    values = []
    dates = []
    results = []

    for hour in range(24):
        date_time = datetime(date2.year, date2.month, date2.day, hour)
        temperature = temperatures[hour]
        humidity = humidities[hour]
        sun_minutes = sun_minutes_per_hour[hour]
        
        solar_index = calculate_solar_index(
            date_time, latitude, longitude, orientation, tilt,
            temperature, humidity, sun_minutes
        )
        indices.append((date_time, solar_index))
        values.append(round(float(solar_index), 1))
        dates.append(date_time.strftime("%H"))
    
    results = {"time": dates,"power": values}

    return results

def calculate_actual_solar_indices(latitude, longitude, orientation, tilt):
    """Calculate solar indices for each hour of the given date."""

    datenow = datetime.today()

    temperatures, humidities, sun_minutes_per_hour = get_weather_data(latitude, longitude, datetime(int(datetime.today().strftime('%Y')), int(datetime.today().strftime('%m')), int(datetime.today().strftime('%d'))))
    

    #print(temperatures)
    #print(humidities)
    #print(sun_minutes_per_hour)

    indices = []
    date_time = datetime(int(datetime.today().strftime('%Y')), int(datetime.today().strftime('%m')), int(datetime.today().strftime('%d')), int(datetime.today().strftime('%H')))
    temperature = temperatures[int(datetime.today().strftime('%H'))]
    humidity = humidities[int(datetime.today().strftime('%H'))]
    sun_minutes = sun_minutes_per_hour[int(datetime.today().strftime('%H'))]
        
    solar_index = calculate_solar_index(
        date_time, latitude, longitude, orientation, tilt,
        temperature, humidity, sun_minutes
    )
    indices.append((date_time, solar_index, temperature, humidity, sun_minutes))
    print(indices)
    return indices

# Example usage


#daily_solar_indices = calculate_daily_solar_indices(
#    date, latitude, longitude, orientation, tilt
#)

#for date_time, solar_index in daily_solar_indices:
#    print(f"Solar Index at {date_time}: {solar_index:.2f}")

#solar_indices = calculate_actual_solar_indices(
#    latitude, longitude, orientation, tilt
#)


#print(f"Solar Index at {solar_indices[0][0]}: {solar_indices[0][1]:.2f}, {solar_indices[0][2]:.2f},{solar_indices[0][3]:.2f} ,{solar_indices[0][4]:.2f}")