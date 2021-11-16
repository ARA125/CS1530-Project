from flask import Flask, render_template, request, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from user_management.login import get_login
from firebase.firebase import db
from user_management.signup import signup
from calendar_management.add_event import *
import uuid
app = Flask(__name__, template_folder="../frontend")
app.secret_key = "really_bad_secret_key"

# Basic page
@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

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

@app.route("/create_calendar", methods=["GET", "POST"])
def create_calendar():
    if request.method == "GET":
        return render_template("new_calendar.html")
    elif request.method == "POST":
        admin_email = session['fb_user']['email']
        data = {"calendar_name": request.form['calendar_name'],"admin": admin_email}
        response = db.child("Calendars").push(data)
        calendarID = response['name']
        return redirect(url_for('add_calendar_event', calendar_id = calendarID))

@app.route('/<calendar_id>/add_calendar_event', methods=['GET', 'POST'])
def add_calendar_event(calendar_id):
    if request.method == "GET":
        return render_template("add_event.html")
    if request.method == "POST":
        success = add_event_func(calendar_id, request.form["event_name"], request.form["start_date"], request.form["end_date"])
        return "Event Successfully Added", 200
if __name__ == '__main__':
    app.run(debug=True)