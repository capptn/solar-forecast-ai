import pandas as pd
from fastai.tabular.all import *

# Lade den Datensatz
data = pd.read_csv('output.csv')

# Definiere die Eingabe- und Zielspalten
dep_var = 'yield'
cont_names = ['Date', 'Time', 'max_power', 'alignment', 'roof_pitch', 'temp', 'rhum', 'wspd']

# Erstelle einen DataLoader
dls = TabularDataLoaders.from_df(data, procs=[Normalize], cont_names=cont_names, y_names=dep_var)

# Trainiere das Modell
learn = tabular_learner(dls, metrics=rmse)
learn.fit_one_cycle(10, 1e-2)

# Speichere das Modell
learn.export('pv_model.pkl')

print("Modelltraining abgeschlossen und gespeichert.")