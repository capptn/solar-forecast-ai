from flask import Flask, json, request
from solarindex3 import calculate_actual_solar_indices, calculate_daily_solar_indices


companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/yet', methods=['GET'])
def get_companies():
  value = calculate_actual_solar_indices(
      52.52, 13.405, 180, 30
  )
  return json.dumps(value[0])

@api.route('/daily', methods=['GET'])
def get_dialy():
  date = request.args.get('date')
  lat = float(request.args.get('lat'))
  lon = float(request.args.get('lon'))
  tilt = int(request.args.get('tilt'))
  ori = int(request.args.get('ori'))
  print(date)
  print(lon)
  print(lat)
  value = calculate_daily_solar_indices(
      date, lat, lon, ori, tilt
  )
  return json.dumps(value)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=10000)