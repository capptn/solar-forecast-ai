import requests
import pandas as pd
from datetime import datetime, timedelta

# Funktion, um stündliche Wetterdaten vom DWD abzurufen
def get_dwd_hourly_data(station_id, date):
    base_url = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/recent/'
    file_name = f'historical/tageswerte_KL_{station_id}_akt.zip'
    url = base_url + file_name

    # Laden der ZIP-Datei mit den Daten
    response = requests.get(url)
    with open('data.zip', 'wb') as file:
        file.write(response.content)
    
    # Entpacken der ZIP-Datei
    import zipfile
    with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        zip_ref.extractall('data')
    
    # Laden der CSV-Datei
    csv_file = f'data/tageswerte_KL_{station_id}_akt.csv'
    df = pd.read_csv(csv_file, sep=';', parse_dates=['MESS_DATUM'], index_col='MESS_DATUM')

    # Filtern nach dem gewünschten Datum
    start_date = datetime(date.year, date.month, date.day)
    end_date = start_date + timedelta(days=1)
    mask = (df.index >= start_date) & (df.index < end_date)
    daily_data = df.loc[mask]

    return daily_data

# Beispielstation und Datum
station_id = '00044'  # Beispielstation (Berlin)
date = datetime(2022, 1, 1)

# Abrufen der Daten
data = get_dwd_hourly_data(station_id, date)

# Daten anzeigen
print(data)

# Optional: Daten als CSV speichern
data.to_csv('historical_weather_data_dwd.csv')