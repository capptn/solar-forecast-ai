import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import requests
from datetime import datetime, timedelta

data = pd.read_csv('20240719data.csv')

# Nur die benötigten Spalten auswählen
data = data[['Time', 'yield', 'temp', 'rhum']]

# Datentypen konvertieren
# Falls die Zeit Sekunden enthält, verwenden wir das Format "%H:%M:%S"
try:
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.hour
except ValueError:
    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M').dt.hour

data = data.rename(columns={'temp': 'temperature', 'rhum': 'humidity'})

# Zielvariable und Merkmale definieren
X = data[['Time', 'temperature', 'humidity']]
y = data['yield']

# Daten normalisieren
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

# Daten in Trainings- und Testdaten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Modell definieren
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[X_train.shape[1]]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
])

# Modell kompilieren
model.compile(optimizer='adam', loss='mse')

# Modell trainieren
history = model.fit(X_train, y_train, epochs=100, validation_split=0.2)

# Modell evaluieren
loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}")

# Funktion zur Vorhersage des nächsten Tages für eine gegebene Stunde
def predict_next_day_for_hour(time, temperature, humidity):
    input_data = np.array([[time, temperature, humidity]])
    input_scaled = scaler_X.transform(input_data)
    predicted_scaled = model.predict(input_scaled)
    predicted = scaler_y.inverse_transform(predicted_scaled)
    return max(0, predicted[0][0])  # Sicherstellen, dass die Vorhersage nicht negativ ist

# OpenWeatherMap API-Schlüssel und Basis-URL
api_key = '7d2c7d95d3b2af7d6fbd3f5ee8668b75'  # Ersetzen Sie dies durch Ihren OpenWeatherMap API-Schlüssel
base_url = "http://api.openweathermap.org/data/2.5/forecast"

# Standort (z.B. Stadt)
city = "Berlin,de"  # Ersetzen Sie dies durch Ihre Stadt

# Anfrage an die API senden
response = requests.get(f"{base_url}?q={city}&appid={api_key}&units=metric")
weather_data = response.json()

# Wetterdaten für jede Stunde des nächsten Tages abrufen
next_day = datetime.now() + timedelta(days=1)
next_day_str = next_day.strftime('%Y-%m-%d')

predictions = []
for entry in weather_data['list']:
    forecast_time = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
    if forecast_time.strftime('%Y-%m-%d') == next_day_str:
        hour = forecast_time.hour
        temperature = entry['main']['temp']
        humidity = entry['main']['humidity']
        predicted_yield = predict_next_day_for_hour(hour, temperature, humidity)
        predictions.append((hour, temperature, humidity, predicted_yield))
        print(f"Vorhergesagter Ertrag für {hour}:00 Uhr: {predicted_yield} (Temp: {temperature}°C, Humidity: {humidity}%)")

# Ergebnisse in ein DataFrame umwandeln und anzeigen
predictions_df = pd.DataFrame(predictions, columns=['Hour', 'Temperature', 'Humidity', 'Predicted Yield'])
print(predictions_df)
