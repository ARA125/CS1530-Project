from firebase.firebase import auth

# login as user and get user
def get_login(email, password):
    return auth.sign_in_with_email_and_password(email, password)