from firebase import db
def create_group_func(group_name, admin_email):
    data = {"group_name": group_name,"admin": admin_email}
    response = db.child("Groups").push(data)
    #return group_id
    return response['name']