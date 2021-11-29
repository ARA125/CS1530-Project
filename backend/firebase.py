import pyrebase

pyrebaseConfig = {
  "apiKey": "AIzaSyAjeCJ-LtVnSD-ccNm6fgX7uvrry18IqYc",
  "authDomain": "acquired-cargo-244705.firebaseapp.com",
  "databaseURL": "https://acquired-cargo-244705-default-rtdb.firebaseio.com",
  "projectId": "acquired-cargo-244705",
  "storageBucket": "acquired-cargo-244705.appspot.com",
  "messagingSenderId": "511206841313",
  "appId": "1:511206841313:web:a541d177280bb5f197d0a0"
#   "serviceAccount": "firebase_config.json"
}

pyre = pyrebase.initialize_app(pyrebaseConfig)

db = pyre.database()
auth = pyre.auth()