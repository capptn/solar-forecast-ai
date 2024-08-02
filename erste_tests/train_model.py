# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Erstellen Sie ein Dummy-Dataset
data = {
    'hour': np.arange(24),
    'temperature': np.random.uniform(15, 25, 24),
    'humidity': np.random.uniform(30, 70, 24),
    'wind_speed': np.random.uniform(0, 15, 24),
    'solar_irradiance': np.random.uniform(0, 1, 24),
    'energy_output': np.random.uniform(50, 200, 24)
}

df = pd.DataFrame(data)

# Features und Zielvariable
X = df[['hour', 'temperature', 'humidity', 'wind_speed', 'solar_irradiance']]
y = df['energy_output']

# Daten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell trainieren
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Modell speichern
joblib.dump(model, 'energy_model.pkl')