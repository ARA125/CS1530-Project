from flask import Flask, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from user_management.login import get_login
from firebase.firebase import db
from user_management.signup import signup
app = Flask(__name__, template_folder="../frontend")
app.secret_key = "really_bad_secret_key"

# Basic page
@app.route("/", methods=["GET"])
def home():
    return redirect(url_for(login))

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        signup(request.form["email"], request.form["password"])

        return "", 200

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        session['fb_user'] = get_login(request.form["email"], request.form["password"])

        return "", 200

if __name__ == '__main__':
    app.run(debug=True)