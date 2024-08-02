from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Modell laden
model = joblib.load('energy_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    hour = data['hour']
    temperature = data['temperature']
    humidity = data['humidity']
    wind_speed = data['wind_speed']
    solar_irradiance = data['solar_irradiance']
    
    # Daten umformen
    input_data = np.array([[hour, temperature, humidity, wind_speed, solar_irradiance]])
    
    # Vorhersage machen
    prediction = model.predict(input_data)
    
    return jsonify({'predicted_energy_output': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)