from zoo import db, app
from datetime import datetime
import os
from flask import current_app
from flask_security import Security, hash_password, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

class Movie(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.DateTime)

    def default_poster():
        return os.path.join(current_app.config['POSTER_FOLDER'], 'default.png')

    poster = db.Column(
        db.String(200), default=default_poster)

    def __repr__(self):
        return f"Movie('{self.name}', '{self.release_date}')"

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Venue('{self.id}', '{self.name}', '{self.capacity}', '{self.city}')"

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    movie = db.relationship("Movie", backref=db.backref("shows", lazy="dynamic", cascade="all, delete"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    venue = db.relationship("Venue", backref=db.backref("shows", lazy="dynamic", cascade="all, delete"))
    tickets_booked = db.Column(db.Integer, default=0, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Show('{self.id}, '{self.movie_id}', '{self.venue_id}', '{self.tickets_booked}')"


class Booking(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
    show = db.relationship("Show", backref=db.backref("bookings", lazy="dynamic", cascade="all, delete"))
    ticket_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Booking('{self.id}, '{self.user_id}', '{self.show_id}', '{self.ticket_count}')"

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)

with app.app_context():
    db.create_all()
    
    if not app.security.datastore.find_user(email="admin@moviezoo.com"):
        user_role = Role(name="user", description="Does usery stuff")
        admin_role = Role(name="admin", description="Does adminy stuff")
        db.session.add(user_role)
        db.session.add(admin_role)
        admin = user_datastore.create_user(email="admin@moviezoo.com", password=hash_password("password"))
        user_datastore.add_role_to_user(admin, 'admin')
    db.session.commit()   