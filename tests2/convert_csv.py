import pandas as pd
from datetime import datetime
from meteostat import Hourly
from meteostat import Stations
from meteostat import Point

stations = Stations()
stations = stations.nearby(51.3656, 7.3834)

station = stations.fetch(1)

print(station)

def get_weather(Year, Month, Day, Yearto, Monthto, Dayto):
    # Set time period
    start = datetime(Year, Month, Day)
    end = datetime(Yearto, Monthto, Dayto, 23, 59)

    # Get hourly data
    data = Hourly('72219', start, end)
    data = data.fetch()

    # Print DataFrame
    print(data)

    data.to_csv('wetterdaten_stuendlich.csv')

def find_datetime_column(df):
    for column in df.columns:
        try:
            # Versuch, die Spalte in datetime-Objekte zu konvertieren
            pd.to_datetime(df[column])
            return column
        except (ValueError, TypeError):
            continue
    raise ValueError("Keine Datums-/Zeitspalte gefunden")

def convert_csv(input_file, output_file, weather_csv, yield_col_name):
    # CSV-Datei einlesen
    df = pd.read_csv(input_file)
    
    # Datums-/Zeitspalte automatisch erkennen
    datetime_column = find_datetime_column(df)
    print(f"Gefundene Datums-/Zeitspalte: {datetime_column}")
    
    # Datums-/Zeitspalte in datetime-Objekte konvertieren
    df[datetime_column] = pd.to_datetime(df[datetime_column])
    
    # Datum und Zeit in separate Spalten aufteilen
    df['Date'] = df[datetime_column].dt.date
    df['Time'] = df[datetime_column].dt.time
    
    # Nur Einträge zur vollen Stunde beibehalten
    df_full_hours = df[df[datetime_column].dt.minute == 0]
    
    date =  df['Date'][1]
    end = df['Date'][ df.shape[0] -1]

    print(end)

    get_weather(int(date.strftime('%Y')), int(date.strftime('%m')), int(date.strftime('%d')),int(end.strftime('%Y')), int(end.strftime('%m')), int(end.strftime('%d')))


    additional_df = pd.read_csv(weather_csv)

    additional_df['time'] = pd.to_datetime(additional_df['time'])
    
    # Datum und Zeit in separate Spalten aufteilen
    additional_df['Date'] = additional_df['time'].dt.date
    additional_df['Time'] = additional_df['time'].dt.time

    # Zusammenführen der beiden DataFrames basierend auf Date und Time
    merged_df = pd.merge(df_full_hours, additional_df, on=['Time', 'Date'], how='left')
    
    merged_df = merged_df.drop('time', axis=1)
    cold = merged_df.pop('Date')
    merged_df.insert(1, cold.name, cold)
    colt = merged_df.pop('Time')
    merged_df.insert(2, colt.name, colt)

    merged_df.insert(3, 'max_power', '6000')
    merged_df.insert(4, 'alignment', '160')
    merged_df.insert(5, 'roof_pitch', '30')

    merged_df = merged_df.rename(columns={yield_col_name: 'yield'})

    # Ergebnis als neue CSV-Datei exportieren
    new_outputfile = date.strftime('%Y') + date.strftime('%m') +  date.strftime('%d') + "data.csv"
    merged_df.to_csv(new_outputfile, index=False)
    #df_full_hours.to_csv(output_file, index=False)

# Beispielaufruf
convert_csv('input.csv', 'output.csv', 'wetterdaten_stuendlich.csv', 'PV-Ertrag(W)')