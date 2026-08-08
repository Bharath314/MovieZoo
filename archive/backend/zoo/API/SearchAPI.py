from flask import request
from flask_restful import Resource
from zoo import db
from zoo.API.schemas import MovieSchema, VenueSchema
from zoo.models import Movie, Venue

class SearchAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.movie_schema = MovieSchema()
        self.venue_schema = VenueSchema()

    def get(self, search_term):
        movies = db.session.query(Movie).filter(Movie.name.like(f'%{search_term}%')).all()
        serialized_movies = []
        for movie in movies:
            serialized_movies.append(self.movie_schema.dump(movie))
        venues = db.session.query(Venue).filter(Venue.name.like(f'%{search_term}%'))
        serialized_venues = []
        for venue in venues:
            serialized_venues.append(self.venue_schema.dump(venue))
        response = {
            "movies": serialized_movies,
            "venues": serialized_venues,
        }
        return response, 200