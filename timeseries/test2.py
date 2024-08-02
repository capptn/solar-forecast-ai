import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import datetime, timedelta

# 1. Laden der historischen Daten
historical_data = pd.read_csv('20240719data.csv')
historical_data['Zeit'] = pd.to_datetime(historical_data['Zeit'])

# Extrahieren von Merkmalen aus der Zeitspalte
historical_data['hour'] = historical_data['Zeit'].dt.hour
historical_data['dayofyear'] = historical_data['Zeit'].dt.dayofyear

# 2. Abrufen der Wetterdaten
api_key = '2bed426b310541c0a3064503240108'
latitude = '51.3656'
longitude = '7.3834'
weather_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={latitude},{longitude}&hours=24'

response = requests.get(weather_url)
weather_data = response.json()

# Erstellen eines DataFrame für die nächsten 24 Stunden
forecast_hours = weather_data['forecast']['forecastday'][0]['hour']
forecast_data = pd.DataFrame(forecast_hours)
forecast_data['time'] = pd.to_datetime(forecast_data['time'])

# Extrahieren von Merkmalen aus der Zeitspalte
forecast_data['hour'] = forecast_data['time'].dt.hour
forecast_data['dayofyear'] = forecast_data['time'].dt.dayofyear

# Benennen der Spalten für Konsistenz
forecast_data.rename(columns={'temp_c': 'temp', 'humidity': 'rhum'}, inplace=True)

# 3. Vorbereitung der Daten für das Modell
X = historical_data[['hour', 'dayofyear', 'temp', 'rhum']]
y = historical_data['power']

# Daten aufteilen in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Erstellen und Trainieren des Modells
model = LinearRegression()
model.fit(X_train, y_train)

# Modell evaluieren
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 4. Vorhersage der PV-Anlagenleistung für die nächsten 24 Stunden
forecast_X = forecast_data[['hour', 'dayofyear', 'temp', 'rhum']]
forecast_power = model.predict(forecast_X)

forecast_data['predicted_power'] = forecast_power

# Ausgabe der Vorhersage
print(forecast_data[['time', 'predicted_power']])