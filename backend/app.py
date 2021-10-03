from flask import Flask, render_template, request
from firebase_admin import initialize_app, credentials, db
app = Flask(__name__, template_folder="../frontend")


fire = initialize_app(
    credentials.Certificate("firebase_config.json"),
    {
        "databaseURL": "https://acquired-cargo-244705-default-rtdb.firebaseio.com/"
    })

pyre_config = {
  "apiKey": "AIzaSyAjeCJ-LtVnSD-ccNm6fgX7uvrry18IqYc",
  "authDomain": "acquired-cargo-244705.firebaseapp.com",
  "databaseURL": "https://acquired-cargo-244705-default-rtdb.firebaseio.com",
  "projectId": "acquired-cargo-244705",
  "storageBucket": "acquired-cargo-244705.appspot.com",
  "messagingSenderId": "511206841313",
  "appId": "1:511206841313:web:a541d177280bb5f197d0a0"

}

# Basic page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Return entire database
@app.route("/database", methods=["GET"])
def PROTO_get_database():
    whole_database = db.reference("/data").get()
    return whole_database or {}

# Add item to database
@app.route("/insert", methods=["GET", "POST"])
def PROTO_insert_item():
    if request.method == "GET":
        return render_template("value.html")
    elif request.method == "POST":
        value = request.form["value"]
        db.reference("/data").child("proto").push(value)
        return "", 200

# protype sign up
@app.route("/signup", methods=["GET", "POST"])
def PROTO_signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # TODO

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

### if __name__ == '__main__':
###     app.run(debug=True)