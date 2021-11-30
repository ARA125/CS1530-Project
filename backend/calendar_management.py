# this file handles adding/modifying/deleting calendars and events, and sorting calendars
from firebase import db
def add_event(calendar_id, event_name, start_date, end_date):
    data = {"event_name": event_name, "start_date": start_date, "end_date": end_date}
    eventID = db.child("Calendars").child(calendar_id).child("events").push(data)
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