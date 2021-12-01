from flask import Flask, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from firebase import db
from user_management import *
from calendar_management import *
from group_management import *
import uuid
app = Flask(__name__)
app.secret_key = "really_bad_secret_key"

# Basic page
@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

@app.route("/signup", methods=["POST"])
def sign_up():
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
    return render_template("user.html", calendars=get_user_calendars(session['fb_user']["localId"]))

@app.route("/create_calendar", methods=["POST"])
def create_calendar():
    owner_email = session['fb_user']['email']
    owner_id = session['fb_user']['localId']
    calendarID = create_cal(request.form['name'], owner_email, owner_id)
    return redirect(url_for('display_calendar', calendar_id=calendarID))

@app.route('/user/<calendar_id>/', methods=['GET'])
def display_calendar(calendar_id):
    return render_template("calendar.html", calendar=get_calendar(calendar_id))

@app.route('/user/<calendar_id>/add_event', methods=['GET', 'POST'])
def add_calendar_event(calendar_id):
    if request.method == "GET":
        return render_template("add_event.html")
    if request.method == "POST":
        add_event(calendar_id, request.form["name"], request.form["date"])
        return redirect(url_for("display_calendar", calendar_id=calendar_id))

@app.route('/user/<calendar_id>/events/<year>/<month>', methods=['GET'])
def get_month_events(calendar_id, year, month):
        return {"items": sort_calendar_events_by_day(calendar_id, int(year), int(month))}

@app.route("/create_group", methods=["GET", "POST"])
def create_group():
    if request.method == "GET":
        return render_template("add_group.html")
    elif request.method == "POST":
        admin_email = session['fb_user']['email']
        groupID = create_group(request.form['group_name'], admin_email)
        return groupID

if __name__ == '__main__':
    app.run(debug=True)