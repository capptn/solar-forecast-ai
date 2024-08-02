import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Beispiel-Daten laden (ersetzen Sie diesen Teil durch das Laden Ihrer eigenen Daten)
# Angenommen, die Daten sind in einer CSV-Datei mit Spalten: 'Zeit', 'power', 'temp', 'rhum'
# Ersetzen Sie 'your_data.csv' durch den Pfad zu Ihrer CSV-Datei
data = pd.read_csv('20240719data.csv', parse_dates=['Zeit'], index_col='Zeit')

# Daten überprüfen
print(data.head())

# Frequenz explizit setzen
data = data.asfreq('h')

# Zeitreihe und exogene Variablen definieren
ts = data['power']
exog = data[['temp', 'rhum']]

# Zeitreihe plotten
plt.figure(figsize=(10, 6))
plt.plot(ts)
plt.title('Hourly Power Generation')
plt.xlabel('Timestamp')
plt.ylabel('Power (kW)')
plt.show()

# ARIMAX-Modell anpassen
# order=(p,d,q) - p: Anzahl der AR-Terme, d: Anzahl der Differenzierungen, q: Anzahl der MA-Terme
model = SARIMAX(ts, exog=exog, order=(5,1,0))
model_fit = model.fit(disp=False, cov_type='robust')

# Modellzusammenfassung drucken
print(model_fit.summary())

# Prognose für die nächsten 24 Stunden (1 Tag)
forecast_steps = 24
exog_forecast = exog.iloc[-forecast_steps:]
forecast = model_fit.get_forecast(steps=forecast_steps, exog=exog_forecast)
forecast_series = forecast.predicted_mean
forecast_index = pd.date_range(start=ts.index[-1], periods=forecast_steps + 1, freq='h')[1:]
forecast_series.index = forecast_index

# Original- und prognostizierte Zeitreihe plotten
plt.figure(figsize=(10, 6))
plt.plot(ts, label='Original')
plt.plot(forecast_series, label='Forecast', linestyle='--')
plt.title('Hourly Power Generation Forecast')
plt.xlabel('Timestamp')
plt.ylabel('Power (kW)')
plt.legend()

plt.savefig('pv_anlage_leistungsprofil.png')

# Peak-Leistung berechnen
peak_power = ts.max()
print(f"Peak Power: {peak_power} kW")