import pandas as pd
import pickle

# Modell und Skaler laden
with open('pv_yield_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Beispielvorhersage für eine neue Eingabe
new_data = {
    'eingang': 1000
}

new_df = pd.DataFrame([new_data])

# Skaliere die neuen Daten
new_df_scaled = scaler.transform(new_df)

# Vorhersage treffen
predicted_yield = model.predict(new_df_scaled)
predicted_yield2 = model.predict(new_df)
print(f'Predicted Yield: {predicted_yield[0]}')
print(f'Predicted Yield: {predicted_yield2[0]}')
