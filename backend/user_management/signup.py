from firebase.firebase import auth

def signup(email, password):
    auth.create_user_with_email_and_password(email, password)