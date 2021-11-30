from flask import Flask, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from firebase import db
from user_management import *
from calendar_management.add_event import *
from group_management.create_group import *
import uuid
app = Flask(__name__)
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
        res = signup(request.form["email"], request.form["password"])
        if res == 0:
            flash("That email is invalid or already in use.")
            return redirect(url_for("signup"))
        elif res == 1:
            flash("An unknown error has occured.")
            return redirect(url_for("signup"))
        else:
            # after signing up, log in automatically and go to user profile
            # NOTE: assumes no errors in get_login will happen
            session['fb_user'] = get_login(request.form["email"], request.form["password"])
            return redirect(url_for("user"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user_or_error = get_login(request.form["email"], request.form["password"])

        # if the login method fails, indicate to the user by redirecting them to the login page
        # with a message
        if user_or_error == 0:
            flash("The username or password is incorrect.")
            return redirect(url_for("login"))
        elif user_or_error == 1:
            flash("An unknown error has occured.")
            return redirect(url_for("login"))
        else:
            session['fb_user'] = user_or_error
        
            # after logging in, take the user to their page
            return redirect(url_for("user"))

@app.route("/user", methods=["GET"])
def user():
    return render_template("user.html", email=session['fb_user']["email"])

@app.route("/create_calendar", methods=["GET", "POST"])
def create_calendar():
    if request.method == "GET":
        return render_template("new_calendar.html")
    elif request.method == "POST":
        admin_email = session['fb_user']['email']
        calendarID = create_calendar_func(request.form['calendar_name'], admin_email)
        return redirect(url_for('add_calendar_event', calendar_id = calendarID))

@app.route('/<calendar_id>/add_calendar_event', methods=['GET', 'POST'])
def add_calendar_event(calendar_id):
    if request.method == "GET":
        return render_template("add_event.html")
    if request.method == "POST":
        event_id = add_event_func(calendar_id, request.form["event_name"], request.form["start_date"], request.form["end_date"])
        return redirect(url_for("user"))

@app.route("/create_group", methods=["GET", "POST"])
def create_group():
    if request.method == "GET":
        return render_template("add_group.html")
    elif request.method == "POST":
        admin_email = session['fb_user']['email']
        groupID = create_group_func(request.form['group_name'], admin_email)
        return groupID

if __name__ == '__main__':
    app.run(debug=True)