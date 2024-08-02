import pandas as pd
import pickle

# Modell und Skaler laden
with open('pv_yield_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Beispielvorhersage für eine neue Eingabe
new_data = {
    'max_power': 6000,
    'alignment': 30,
    'roof_pitch': 15,
    'temp': 28,
    'rhum': 60,
    'wspd': 5,
    'Hour': 12
}

new_df = pd.DataFrame([new_data])

# Skaliere die neuen Daten
new_df_scaled = scaler.transform(new_df)

# Vorhersage treffen
predicted_yield = model.predict(new_df_scaled)
print(f'Predicted Yield: {predicted_yield[0]}')
