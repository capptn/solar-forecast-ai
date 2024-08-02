import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Laden der CSV-Datei
file_path = '20240719data.csv'
data = pd.read_csv(file_path)

# Datenvorbereitung
data['Time'] = pd.to_datetime(data['Time'])
data['hour'] = data['Time'].dt.hour

# Filtern der Daten für Sonnenstunden (6 Uhr bis 20 Uhr)
data_filtered = data[(data['hour'] >= 0) & (data['hour'] <= 23)]

# Auswählen der relevanten Merkmale und Zielvariable
features = ['temp', 'hour', 'max_power', 'alignment', 'roof_pitch']
target = 'yield'

X = data_filtered[features]
y = data_filtered[target]

# Aufteilen der Daten in Trainings- und Testsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Trainieren eines linearen Regressionsmodells
model = LinearRegression()
model.fit(X_train, y_train)

# Vorhersage für jede Stunde von 6 Uhr bis 20 Uhr am nächsten Tag
hours = range(0, 23)
temp_tomorrow = 28  # Angenommene Temperatur

# Erstellen eines DataFrames für die Vorhersage
prediction_data = pd.DataFrame({
    'temp': ['13', '13', '13', '13', '13', '14', '14', '15', '17', '19', '23', '26', '27', '28', '28', '30', '30', '29', '29', '27', '25', '24', '19'],
    'hour': list(hours),
    'max_power': [data['max_power'].iloc[0]] * len(hours),
    'alignment': [data['alignment'].iloc[0]] * len(hours),
    'roof_pitch': [data['roof_pitch'].iloc[0]] * len(hours)
})

# Vorhersage der Leistung
predicted_yields = model.predict(prediction_data)

# Kombinieren der Stunden und vorhergesagten Leistungen in einen DataFrame
predicted_df = pd.DataFrame({
    'hour': hours,
    'predicted_yield': predicted_yields
})

# Anzeigen der Vorhersagen
print(predicted_df)

# Plotten der Vorhersagen
plt.figure(figsize=(10, 6))
plt.plot(predicted_df['hour'], predicted_df['predicted_yield'], marker='o', linestyle='-', color='b')
plt.title('Vorhersage der PV-Anlagenleistung für morgen')
plt.xlabel('Stunde')
plt.ylabel('Vorhergesagte Leistung (Watt)')
plt.grid(True)
plt.show()