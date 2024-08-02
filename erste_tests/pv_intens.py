import math
import pandas as pd
from datetime import datetime
from pvlib.solarposition import get_solarposition
from pvlib.irradiance import get_total_irradiance
from pvlib.location import Location

# Benutzerdefinierte Parameter
latitude = 52.52  # Breitengrad (z.B. Berlin)
longitude = 13.405  # Längengrad (z.B. Berlin)
altitude = 34  # Höhe über dem Meeresspiegel in Metern
tilt = 30  # Dachneigung in Grad
azimuth = 180  # Ausrichtung des Daches in Grad (Süden = 180°)
date_time = "2024-08-01 11:30:00"  # Datum und Uhrzeit im Format "YYYY-MM-DD HH:MM:SS"
peak_power = 300  # Peakleistung eines Moduls in Watt Peak (Wp)
num_panels = 10  # Anzahl der installierten Module

# Datum und Uhrzeit in ein datetime-Objekt umwandeln
time = pd.to_datetime(date_time)

# Standort definieren
location = Location(latitude, longitude, 'Europe/Berlin', altitude)

# Solarposition berechnen
solar_position = get_solarposition(time, location.latitude, location.longitude)

# Berechnung der Einstrahlung
dni = solar_position['apparent_elevation'].apply(lambda x: max(0, math.cos(math.radians(90 - x))))
ghi = dni * math.sin(math.radians(tilt))
dhi = ghi * (1 - math.cos(math.radians(tilt))) / 2

total_irradiance = get_total_irradiance(tilt, azimuth, solar_position['apparent_zenith'], 
                                        solar_position['azimuth'], dni, ghi, dhi)

# Vermutliche Leistung berechnen
poa_global = total_irradiance['poa_global'].values[0]
power_output = peak_power * num_panels * (poa_global)  # Leistung in Watt

# Ergebnisse anzeigen
print(f"Datum und Uhrzeit: {date_time}")
print(f"Breitengrad: {latitude}°, Längengrad: {longitude}°")
print(f"Höhe über dem Meeresspiegel: {altitude} m")
print(f"Dachneigung: {tilt}°")
print(f"Ausrichtung des Daches: {azimuth}°")
print(f"Sonnenhöhe: {solar_position['apparent_elevation'].values[0]:.2f}°")
print(f"Sonnenposition (Azimut): {solar_position['azimuth'].values[0]:.2f}°")
print(f"Direkte Normalstrahlung (DNI): {dni.values[0]:.2f} W/m²")
print(f"Globale Horizontale Strahlung (GHI): {ghi.values[0]:.2f} W/m²")
print(f"Diffus Horizontale Strahlung (DHI): {dhi.values[0]:.2f} W/m²")
print(f"Gesamte Einstrahlung auf die PV-Anlage: {poa_global:.2f} W/m²")
print(f"Vermutliche Leistung der PV-Anlage: {power_output:.2f} W")