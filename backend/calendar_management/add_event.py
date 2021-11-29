from firebase import db
def add_event_func(calendar_id, event_name, start_date, end_date):
    data = {"event_name": event_name, "start_date": start_date, "end_date": end_date}
    eventID = db.child("Calendars").child(calendar_id).child("events").push(data)
    return eventID;
def create_calendar_func(calendar_name, admin_email):
    data = {"calendar_name":calendar_name,"admin": admin_email}
    response = db.child("Calendars").push(data)
    #return calendar_id
    return response['name']