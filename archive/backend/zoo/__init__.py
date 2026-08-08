import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla

from zoo.config import Config


app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)

db = SQLAlchemy()
db.init_app(app)

CORS(app)

from zoo.API.VenueAPI import VenueAPI, VenueListAPI, ExportVenueDetailsAPI
from zoo.API.MovieAPI import MovieAPI, MovieListAPI
from zoo.API.ShowAPI import ShowAPI, VenueShowsAPI, MovieShowsAPI
from zoo.API.BookingAPI import BookingAPI
from zoo.API.UserAPI import CurrentUserAPI, SignUpAPI
from zoo.API.SearchAPI import SearchAPI

api.add_resource(SignUpAPI, '/register')
api.add_resource(CurrentUserAPI, '/api/current-user')
api.add_resource(VenueListAPI, '/api/venues')
api.add_resource(VenueAPI, '/api/venues/<int:id>')
api.add_resource(VenueShowsAPI, '/api/venues/<int:venue_id>/shows')
api.add_resource(ExportVenueDetailsAPI, '/api/venues/<int:venue_id>/export')
api.add_resource(MovieListAPI, '/api/movies')
api.add_resource(MovieAPI, '/api/movies/<int:id>')
api.add_resource(MovieShowsAPI, '/api/movies/<int:movie_id>/shows')
api.add_resource(ShowAPI, '/api/show/<int:id>')
api.add_resource(BookingAPI, '/api/booking')
api.add_resource(SearchAPI, '/api/search/<search_term>')
