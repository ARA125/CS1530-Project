from firebase.firebase import db
def add_event_func(calendar_id, event_name, start_date, end_date):
    data = {"event_name": event_name, "start_date": start_date, "end_date": end_date}
    validCalendar = db.child("Calendars").child(calendar_id).child("events").push(data)
    return 1;