# this file handles adding/modifying/deleting calendars and events, and sorting calendars
from firebase import db
from datetime import date, timedelta
def add_event(id, name, date):
    data = {"event_name": name, "date": date}
    eventID = db.child("Calendars").child(id).child("events").push(data)
    return eventID

def create_cal(calendar_name, admin_email, id):
    data = {"calendar_name":calendar_name, "owner_email": admin_email, "owner": id}
    response = db.child("Calendars").push(data)
    #return calendar_id
    return response['name']

# return all calendars owned by a user
# any error returns null
def get_user_calendars(id):
    try:
        return db.child("Calendars").order_by_child("owner").equal_to(id).get()
    except:
        return None
# return a calendar by ID
# any error returns null
def get_calendar(id):
    try:
        return db.child("Calendars").child(id).get().val()
    except:
        return None

# return all events of a calendar
# any error returns null
def get_calendar_events(id):
    try:
        return db.child("Calendars").child(id).child("events")
    except:
        return None

# return calendar events sorted by days
# TODO fix runtime
def sort_calendar_events_by_day(id, year, month):
    ret = []
    dt = date(year, month, 1)
    while dt.month == month:
        # if day is 0
        ret.append(get_calendar_events(id).order_by_child("date").equal_to(date.isoformat(dt)).get().val())

        dt = dt + timedelta(days=1)
    return ret