import pyrebase
from flask import *

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
storage = firebase.storage()

app  = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
        if request.method == 'POST':
            name = request.form['name']
            database.child("todo").push(name)
            todo = database.child("todo").get()
            #return todo.val() instead pass val to html
            to = todo.val()
            return render_template('index.html', t=to)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

