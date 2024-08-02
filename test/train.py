import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import pickle

# CSV-Datei laden
file_path = 'output.csv'
df = pd.read_csv(file_path)


# Features und Zielvariable definieren
features = ['eingang']
y = df['ausgang']
X = df[features]

# Skaliere die Features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Daten in Trainings- und Testset aufteilen
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Modell wählen
model = Ridge(alpha=1.0)

# Modell mit Kreuzvalidierung bewerten
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_absolute_error')
print(f'Cross-Validation MAE: {-np.mean(cv_scores)}')

# Modell trainieren
model.fit(X_train, y_train)

# Vorhersagen treffen
y_pred = model.predict(X_test)

# Evaluierung des Modells
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f'Test MAE: {mae}')
print(f'Test MSE: {mse}')
print(f'Test RMSE: {rmse}')

# Modell und Skaler speichern
with open('pv_yield_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)