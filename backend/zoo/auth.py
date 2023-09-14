from flask_security.signals import user_registered
from zoo import app, db
from models import user_datastore

@user_registered.connect_via(app)
def user_registered_signal_handler(app, user, confirm_token):
    default_role = user_datastore.find_role("user")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()