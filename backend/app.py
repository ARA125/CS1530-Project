from flask import Flask, render_template, request
import pyrebase
app = Flask(__name__, template_folder="../frontend")


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

# Basic page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Return entire database FIXME won't work unless logged in as a user?
@app.route("/database", methods=["GET"])
def PROTO_get_database():
    whole_database = db.child("proto").get().val()
    return whole_database or {}

# Add item to database FIXME won't work unless logged in as a user?
@app.route("/insert", methods=["GET", "POST"])
def PROTO_insert_item():
    if request.method == "GET":
        return render_template("value.html")
    elif request.method == "POST":
        value = request.form["value"]
        db.child("proto").push(value)
        return "", 200

# protype sign up
@app.route("/signup", methods=["GET", "POST"])
def PROTO_signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        auth.create_user_with_email_and_password(email,password)

        return "", 200

# protype sign up
@app.route("/login", methods=["GET", "POST"])
def PROTO_login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # TODO

        return "", 200

if __name__ == '__main__':
    app.run(debug=True)