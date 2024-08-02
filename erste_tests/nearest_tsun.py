from datetime import datetime
from meteostat import Point, Stations, Daily, Hourly
import pandas as pd
from geopy.distance import geodesic

# Standort definieren (z.B. Berlin)
latitude = 51.3656
longitude = 7.3834
location = Point(latitude, longitude)

# Zeitraum definieren
start = datetime(2024, 7, 28)
end = datetime(2024, 7, 28)

# Radius definieren (z.B. 50 km)
radius = 100  # in kilometers

# Wetterstationen im Umkreis finden
stations = Stations()
stations = stations.nearby(51.3656, 7.3834)

newstations = stations.fetch(100)

for index, station in newstations.iterrows():

    data = Daily(station['wmo'], start, end)
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
        print(data)
        
        if 'tsun' in data.columns:
            tsun_data = data['tsun'].dropna()
            if not tsun_data.empty:
                print(tsun_data.astype(int).tolist())
            else:
                print('Keine Daten für tsun vorhanden')
        else:
            print('tsun-Spalte nicht gefunden')
        
        tsun_minutes = tsun_data.astype(int).tolist()[0] / 60
        average_solar_irradiance = 4  # kWh/m²
        pv_area = 10  # m²
        pv_efficiency = 0.7  # 15%

        # Umrechnung der Sonnenscheindauer in Stunden
        tsun_hours = tsun_minutes / 60  # 5 Stunden

        # Berechnung der täglichen Solarenergie
        daily_solar_energy = tsun_hours * average_solar_irradiance  # kWh/m² pro Tag

        # Berechnung der Energieausbeute der PV-Anlage
        energy_output = daily_solar_energy * pv_area * pv_efficiency  # kWh pro Tag

        print(energy_output)
        break
   
