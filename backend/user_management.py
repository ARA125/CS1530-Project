# this module handles the login/logout, creation/deletion, modification, etc. of users
from flask import session
from requests.exceptions import HTTPError
from firebase import auth

# register account with a given email and password
# return 0 if email or password is wrong, 1 if unexpected error
def signup(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
    # if the email is already taken, return code 0 to indicate so
    except HTTPError:
        return 0
    # if something else goes wrong, return 1 to indicate so
    except:
        return 1
    # return -1 if successful
    return -1


# login with a given email and password, and get user if correct
# return 0 if email or password is wrong, 1 if unexpected error
def get_login(email, password):
    try:
        return auth.sign_in_with_email_and_password(email, password)
    # if the username or password is wrong, return code 0 to indicate so
    except HTTPError:
        return 0
    # if something else goes wrong, return 1 to indicate so
    except:
        return 1


def logout():
    session['fb_user'] = None