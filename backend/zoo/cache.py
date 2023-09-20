from zoo import app, db
from flask import current_app
from flask_caching import Cache
from zoo.models import Movie, Venue, Show, Booking
from zoo.API.schemas import MovieSchema, VenueSchema, ShowSchema, BookingSchema

cache = Cache(app)

movie_schema = MovieSchema()
venue_schema = VenueSchema()
show_schema = ShowSchema()

@cache.cached(timeout=50)
def get_all_movies():
    movies = db.session.execute(db.select(Movie).order_by(Movie.name)).scalars()
    serialized_movies = []
    for movie in movies:
        serialized_movies.append(movie_schema.dump(movie))
    return serialized_movies

@cache.memoize(timeout=50)
def get_movie(movie_id):
    movie = db.one_or_404(db.select(Movie).filter_by(id=movie_id))
    serialized_movie = movie_schema.dump(movie)
    return serialized_movie

@cache.cached(timeout=50)
def get_all_venues():
    venues = db.session.execute(db.select(Venue).order_by(Venue.city)).scalars()
    serialized_venues = []
    for venue in venues:
        serialized_venues.append(venue_schema.dump(venue))
    return serialized_venues

@cache.memoize(timeout=50)
def get_venue(id):
    venue = db.one_or_404(db.select(Venue).filter_by(id=id))
    serialized_venue = venue_schema.dump(venue)
    return serialized_venue

@cache.memoize(timeout=50)
def get_shows_by_venue(venue_id):
    shows = db.session.execute(db.select(Show).filter_by(venue_id=venue_id)).scalars()
    serialized_shows = []
    for show in shows:
        show_dict = {
            "id": show.id,
            "movie_id": show.movie_id,
            "movie": show.movie.name,
            "venue_id": show.venue_id,
            "venue": show.venue.name,
            "tickets_booked": show.tickets_booked
        }
        serialized_shows.append(show_schema.dump(show_dict))
    return serialized_shows

@cache.memoize(timeout=50)
def get_shows_by_movie(movie_id):
    shows = db.session.execute(db.select(Show).filter_by(movie_id=movie_id)).scalars()
    serialized_shows = []
    for show in shows:
        show_dict = {
            "id": show.id,
            "movie_id": show.movie_id,
            "movie": show.movie.name,
            "venue_id": show.venue_id,
            "venue": show.venue.name,
            "tickets_booked": show.tickets_booked
        }
        serialized_shows.append(show_schema.dump(show_dict))
    return serialized_shows

@cache.memoize(timeout=50)
def get_show(id):
    show = db.one_or_404(db.select(Show).filter_by(id=id))
    serialized_show = show_schema.dump(show)
    return serialized_show