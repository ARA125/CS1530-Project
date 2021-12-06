# this file handles adding/modifying/deleting calendars and events, and sorting calendars
from firebase import db
from datetime import date, timedelta
def add_event(id, name, dt):
    data = {"event_name": name, "date": date.fromisoformat(dt).toordinal()}
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

# return all calendars a user is invited to
# any error returns null
def get_invited_calendars(id):
    try:
        return db.child("Users").child(id).child("invites").get().val()
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
def sort_calendar_events_by_day(id, year, month):
    ret = []
    # dt - start of month
    dt = date(year, month, 1).toordinal()
    new_month = month + 1
    new_year = year
    if new_month == 13:
        new_year = year + 1
        new_month = 1
    # dte - end of month
    dte = date(new_year, new_month, 1) - timedelta(days=1)
    dte = dte.toordinal()
    events = get_calendar_events(id).order_by_child("date").start_at(dt).end_at(dte).get().val()

    day = []
    dt_count = dt
    # NOTE assume events in order
    for e in events:
        # if it is not still counting events of the day
        if events[e]["date"] != dt_count:
            ret.append(day)
            dt_count += 1
            # set dt_count to new date
            # set any dates skipped over to empty objects
            while dt_count != events[e]["date"]:
                ret.append(None)
                dt_count += 1
            day = []
        
        day.append(events[e])
    ret.append(day)
    return ret

# TODO if user is the owner, fail
def invite_user(id, email):
    # get the user id by email
    try:
        uid = db.child("Users").order_by_child("email").equal_to(email).get().pyres[0].key()
    except:
        print("FAIL")
        return 0
    # add the user to the calendar's whitelist
    db.child("Calendars").child(id).child("whitelist").child(uid).set({"elevation": 0})
    # add the calendar to the user's list of calendars
    db.child("Users").child(uid).child("invites").child(id).set({"accepted": 0})
    return -1

# recommend the date with the lowest amount of events scheduled
# return the day with the lowest amount of dates scheduled
# break ties with the earlier date
def recommend_day(id, limit):
    # dt - start of month
    dt = date.today()
    dte = date(dt.year, dt.month, dt.day) + timedelta(days=limit-1)
    dt = dt.toordinal()
    dte = dte.toordinal()
    events = get_calendar_events(id).order_by_child("date").start_at(dt).end_at(dte).get().val()

    dt_count = dt
    events_in_day = 0
    best_day = dt
    best_day_events = -1
    # NOTE assume events in order

    for e in events:
        # if it is not still counting events of the day
        if events[e]["date"] != dt_count:
            # if the next event skips over at least a day, return the first skipped day
            # because that day has no events
            # exclude starting cycle
            if events[e]["date"] != dt_count + 1 and dt_count != dt:
                return date.fromordinal(dt_count + 1)

            # if starting cycle, count events in first day
            if dt_count == dt:
                best_day_events = events_in_day
                if events_in_day == 0:
                    return date.fromordinal(dt_count)
            elif events_in_day < best_day_events:
                best_day_events = events_in_day
                best_day = dt_count
            
            events_in_day = 0
            # set dt_count to new date
            dt_count += 1
        
        events_in_day += 1
    if events_in_day < best_day_events:
        best_day_events = events_in_day
        best_day = dt_count
    # if dt_count does not reach dte, the end of the range is not reached, so there are days
    # at the end that are free. return the next date after dt_count, which is free
    # if dt_count == dt, there are no events in the calendar, so skip
    if dt_count != dte and dt_count != dt:
        return date.fromordinal(dt_count + 1)
    return date.fromordinal(best_day)