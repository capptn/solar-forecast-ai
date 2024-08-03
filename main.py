from flask import Flask, json
from solarindex3 import calculate_actual_solar_indices


companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/yet', methods=['GET'])
def get_companies():
  value = calculate_actual_solar_indices(
    52.52, 13.405, 180, 30
)
  return json.dumps(value[0])

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=10000)