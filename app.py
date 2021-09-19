import pyrebase


firebaseConfig = {
    "apiKey": "AIzaSyAa7tX8ARcpXcd5RVUqxWGD6nFgV7s6qG0",
    "authDomain": "calendarwebapp-38945.firebaseapp.com",
    "projectId": "calendarwebapp-38945",
    "storageBucket": "calendarwebapp-38945.appspot.com",
    "messagingSenderId": "28380169951",
    "appId": "1:28380169951:web:c3a6eaa43c9b7fbeb08b6a",
    "measurementId": "G-MY592ZMD67",
    "databaseURL": "https://calendarwebapp-38945-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

database = firebase.database()


data = {"name": "Mortimer 'Morty' Smith"}
database.child("users").push(data)