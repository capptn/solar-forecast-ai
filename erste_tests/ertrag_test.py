import pandas as pd
import matplotlib.pyplot as plt
import pvlib
from pvlib import location, modelchain, pvsystem, irradiance
import requests

# Standort der PV-Anlage
latitude = 48.1351  # Beispiel: München
longitude = 11.5820
tz = 'Europe/Berlin'

# API-Schlüssel für WeatherAPI
api_key = '2bed426b310541c0a3064503240108'  # Ersetzen Sie 'YOUR_WEATHERAPI_KEY' durch Ihren echten API-Schlüssel

# Datum für die Berechnung
date = '2023-08-01'  # Beispieldatum
date = pd.to_datetime(date)  # Konvertiere in datetime

# Zeitreihe für einen Tag in 1-Stunden-Intervallen erstellen
times = pd.date_range(start=date, end=date + pd.Timedelta(days=1), freq='1H', tz=tz)

# Wetterdaten von WeatherAPI abrufen
def get_weather_data(lat, lon, date, api_key):
    url = f"http://api.weatherapi.com/v1/history.json"
    params = {
        'key': api_key,
        'q': f"{lat},{lon}",
        'dt': date.strftime('%Y-%m-%d')
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['forecast']['forecastday'][0]['hour']

weather_data = get_weather_data(latitude, longitude, date, api_key)

# Wetterdaten in DataFrame umwandeln
weather_df = pd.DataFrame(weather_data)
weather_df['time'] = pd.to_datetime(weather_df['time']).dt.tz_localize('UTC').dt.tz_convert(tz)
weather_df = weather_df.set_index('time')

# Zeitreihe an Wetterdaten anpassen
weather_df = weather_df.reindex(times)

# Berechnung von DNI und DHI aus GHI
solar_position = pvlib.solarposition.get_solarposition(times, latitude, longitude)
dni_dhi = irradiance.erbs(weather_df['temp_c'] * 10, solar_position['zenith'], weather_df.index.dayofyear)

# PVLib-kompatibles Wetterdaten-Format
weather = pd.DataFrame({
    'ghi': weather_df['temp_c'] * 10,  # Temporäre GHI-Werte, sollten durch reale Werte ersetzt werden
    'dni': dni_dhi['dni'],
    'dhi': dni_dhi['dhi'],
    'temp_air': weather_df['temp_c'],
    'wind_speed': weather_df['wind_kph'] / 3.6  # Umrechnung von km/h in m/s
}, index=weather_df.index)

# Standortobjekt erstellen
site = location.Location(latitude, longitude, tz=tz)

# Systemobjekt erstellen
module_database = pvlib.pvsystem.retrieve_sam('CECMod')
inverter_database = pvlib.pvsystem.retrieve_sam('CECInverter')

module_name = list(module_database.keys())[0]  # erstes Modul in der Datenbank
inverter_name = list(inverter_database.keys())[0]  # erster Wechselrichter in der Datenbank

module_parameters = module_database[module_name]
inverter_parameters = inverter_database[inverter_name]
temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

system = pvsystem.PVSystem(surface_tilt=30,
                           surface_azimuth=180,
                           module_parameters=module_parameters,
                           inverter_parameters=inverter_parameters,
                           temperature_model_parameters=temperature_model_parameters)

mc = modelchain.ModelChain(system, site, aoi_model='no_loss', spectral_model='no_loss')

# Berechnung der Leistungsdaten
mc.run_model(weather)

# Tagesverlauf der Leistung berechnen (W)
ac_power = mc.results.ac

# Debug-Ausgabe, um sicherzustellen, dass die Daten korrekt generiert wurden
print(ac_power.head())

# Plotten der Ergebnisse
plt.figure(figsize=(12, 6))
plt.plot(ac_power.index, ac_power, label='AC Power', color='tab:blue')
plt.xlabel('Zeit')
plt.ylabel('Leistung (W)')
plt.title('Leistungsprofil der PV-Anlage über den Tag')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Speichern des Diagramms
plt.savefig('pv_anlage_leistungsprofil.png')

# Stellen Sie sicher, dass das Diagramm angezeigt wird
plt.show()

# Tagesertrag berechnen und anzeigen
daily_energy = ac_power.resample('D').sum() / 1000  # Umrechnung in kWh
print(f"Tagesertrag: {daily_energy.values[0]:.2f} kWh")