import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Laden der Daten
data = pd.read_csv('20240719data.csv')

data['Time'] = pd.to_datetime(data['Time'])
data['hour'] = data['Time'].dt.hour

# Annahme: Daten enthalten Spalten ['''Temperatur', 'Luftfeuchtigkeit', 'Windgeschwindigkeit', 'Sonneneinstrahlung', 'Leistung']
X = data[['hour','temp', 'rhum', 'wspd']]
y = data['yield']

# Datenaufteilung in Trainings- und Testset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Daten skalieren
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modell erstellen
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Modell kompilieren
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Modell trainieren
history = model.fit(X_train_scaled, y_train, epochs=50, validation_split=0.2)

# Modell bewerten
loss, mae = model.evaluate(X_test_scaled, y_test)
print(f'Model Mean Absolute Error: {mae}')

# Vorhersagen machen
y_pred = model.predict(X_test_scaled)

# Ergebnis anzeigen
predictions = pd.DataFrame({'Tatsächlich': y_test, 'Vorhergesagt': y_pred.flatten()})
print(predictions.head())

# Vorhersage für zukünftige Daten (Beispiel)
future_weather_data = np.array([[15 ,29, 50, 2]])  # Beispielwerte für Temperatur, Luftfeuchtigkeit, Windgeschwindigkeit, Sonneneinstrahlung
future_weather_data_scaled = scaler.transform(future_weather_data)
future_prediction = model.predict(future_weather_data_scaled)
print(f'Vorhergesagte Leistung: {future_prediction[0][0]}')
