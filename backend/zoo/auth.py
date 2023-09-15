from flask_security.signals import user_registered
from flask import current_app
from zoo.models import user_datastore

def register_signup_handler(app, db):
    @user_registered.connect_via(app)
    def user_registered_signal_handler(app, user, confirm_token):
        print("working")
        default_role = user_datastore.find_role("user")
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()