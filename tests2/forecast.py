import pandas as pd
from fastai.tabular.all import *

# Lade das trainierte Modell
learn = load_learner('pv_model.pkl')

def predict_pv_output(peak_power, orientation, tilt, temperature, humidity, wind_speed):
    # Erstelle einen DataFrame mit den Eingabewerten
    input_data = pd.DataFrame({
        'Anlage_Peak_Leistung': [peak_power],
        'Ausrichtung': [orientation],
        'Neigung': [tilt],
        'Temperatur': [temperature],
        'Luftfeuchtigkeit': [humidity],
        'Windgeschwindigkeit': [wind_speed]
    })

    # Erhalte die Vorhersage
    dl = learn.dls.test_dl(input_data)
    pred, _ = learn.get_preds(dl=dl)
    return pred.item()

# Beispielvorhersage
if __name__ == "__main__":
    peak_power = 5.0  # kWp
    orientation = 180  # Grad
    tilt = 30  # Grad
    temperature = 25  # °C
    humidity = 50  # %
    wind_speed = 5  # m/s

    prediction = predict_pv_output(peak_power, orientation, tilt, temperature, humidity, wind_speed)
    print(f"Vorhergesagter PV-Ertrag: {prediction} kWh")
