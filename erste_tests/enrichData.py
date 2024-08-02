import requests
import pandas as pd
import datetime


# Funktion, um historische Wetterdaten zu erhalten
def get_weather_data(date, lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/onecall/timemachine'
    params = {
        'lat': lat,
        'lon': lon,
        'dt': int(pd.Timestamp(date).timestamp()),
        'appid': '7d2c7d95d3b2af7d6fbd3f5ee8668b75',
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data);
    if 'current' in data:
        current = data['current']
        return {
            'temperature': current.get('temp'),
            'humidity': current.get('humidity'),
            'wind_speed': current.get('wind_speed'),
            'solar_irradiance': current.get('uvi', 0)  # Solarstrahlung ist oft als UV-Index verfügbar
        }
    return None


# Beispiel-Koordinaten für Berlin (ersetzen Sie dies mit Ihren tatsächlichen Koordinaten)

location = {'lat': 51.61, 'lon': 7.63}  # Beispiel-Koordinaten für Berlin

# Wetterdaten abrufen und in DataFrame integrieren
weather_data = get_weather_data(int(datetime.datetime.strptime('2024-07-28 13:00:00', '%Y-%m-%d %H:%M:%S').strftime("%s")), location['lat'], location['lon'])

print(weather_data)