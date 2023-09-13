from flask import Flask, request, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "f4fa483fa875f9cbf287dac5e6f36f006cd889289913d1698007df55cd9898cd"
app.config['SECURITY_PASSWORD_SALT'] = "317253998663595341291509795129662632201"
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['POSTER_FOLDER'] = os.path.join('zoo', 'static', 'posters')


api = Api(app)
db = SQLAlchemy()
db.init_app(app)
CORS(app)

from zoo.API.VenueAPI import VenueAPI
from zoo.API.MovieAPI import MovieAPI, MovieListAPI
from zoo.API.ShowAPI import ShowAPI
from zoo.API.BookingAPI import BookingAPI
# from zoo.API.UserAPI import LoginResource, LogoutResource

# api.add_resource(UserAPI, '/api/user')
# api.add_resource(LoginResource, '/api/login')
# api.add_resource(LogoutResource, '/api/logout')
api.add_resource(VenueAPI, '/api/venue')
api.add_resource(MovieListAPI, '/api/movies')
api.add_resource(MovieAPI, '/api/movies/<int:id>')
api.add_resource(ShowAPI, '/api/show')
api.add_resource(BookingAPI, '/api/booking')

