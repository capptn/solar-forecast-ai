from flask import Flask, json, request
from solarindex3 import calculate_actual_solar_indices, calculate_daily_solar_indices
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./ai-pv-forecast-firebase-adminsdk-fu9qk-3fbb251864.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

def get_settings_from_firestore(uid):

  doc_ref = store.collection("pv_settings").document(uid)

  doc = doc_ref.get()
  if doc.exists:
      return doc.to_dict()
  else:
      return False



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
  data = get_settings_from_firestore(request.args.get('uid'))
  if data == False:
     return 'bad request!', 400
  print(data)
  lat = float(data['lat'])
  lng = float(data['lng'])
  tilt = int(data['roofPitch'])
  ori = int(data['orientation'])
  print(date)
  print(lng)
  print(lat)
  value = calculate_daily_solar_indices(
      date, lat, lng, ori, tilt
  )
  return json.dumps(value)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=10000)