import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

# DWD CDC Base URL
DWD_CDC_BASE_URL = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

# Funktion zur Dateisuche auf dem DWD-Server
def get_file_url(data_type, station_id, year):
    response = requests.get(DWD_CDC_BASE_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch directory listing: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and f"tageswerte_KL_{station_id}" in href and href.endswith('.zip'):
            return DWD_CDC_BASE_URL + href
    
    raise Exception(f"File not found for {data_type}, station {station_id}, year {year}")

# Funktion zum Abrufen der Daten
def get_data(station_id, date, data_type):
    year = date.strftime('%Y')
    file_url = get_file_url(data_type, station_id, year)
    response = requests.get(file_url)
    if response.status_code == 200:
        # Speichern und Entpacken der ZIP-Datei
        zip_filename = f"{data_type}_{station_id}_{year}.zip"
        with open(zip_filename, 'wb') as file:
            file.write(response.content)
        
        os.system(f"unzip -o {zip_filename} -d {data_type}_{station_id}_{year}")
        
        # Suche nach der entpackten CSV-Datei
        for root, dirs, files in os.walk(f"{data_type}_{station_id}_{year}"):
            for file in files:
                if file.endswith('.csv'):
                    csv_file = os.path.join(root, file)
                    return pd.read_csv(csv_file, sep=';', na_values='-999')
        
        raise Exception("CSV file not found after unzipping")
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Hauptfunktion
def main(station_id, date, output_filename):
    temp_data = get_data(station_id, date, 'air_temperature')
    humidity_data = get_data(station_id, date, 'humidity')
    solar_data = get_data(station_id, date, 'solar')

    # Zusammenführen der Daten
    merged_data = pd.merge(temp_data, humidity_data, on=['STATIONS_ID', 'MESS_DATUM'], suffixes=('_temp', '_humidity'))
    merged_data = pd.merge(merged_data, solar_data, on=['STATIONS_ID', 'MESS_DATUM'])

    # Filterung nach dem spezifischen Datum
    specific_date = date.strftime('%Y%m%d')
    filtered_data = merged_data[merged_data['MESS_DATUM'] == int(specific_date)]

    # Auswahl der relevanten Spalten und Umbenennung
    filtered_data = filtered_data[['MESS_DATUM', 'TT_TU', 'RF_TU', 'SD_SO']]
    filtered_data.columns = ['Date', 'Temperature', 'Humidity', 'Sunshine_Duration']

    # Speichern der Daten als CSV
    filtered_data.to_csv(output_filename, index=False)
    print(f"Daten für {date.strftime('%Y-%m-%d')} wurden erfolgreich in {output_filename} gespeichert.")

# Beispielverwendung
if __name__ == "__main__":
    # Beispielstation und Datum
    station_id = "00044"  # Beispielstation-ID (muss existieren)
    date = datetime.datetime.strptime("2023-07-29", "%Y-%m-%d")  # Beispieldatum
    
    output_filename = "weather_data.csv"
    
    main(station_id, date, output_filename)
