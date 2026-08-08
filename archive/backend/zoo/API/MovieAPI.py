import os
import uuid
from datetime import datetime

from flask import current_app, request
from flask_restful import Resource
from flask_security import auth_required, roles_required
from zoo import db
from zoo.API.schemas import MovieSchema
from zoo.models import Movie
from zoo.cache import *


def save_poster(file):
    _, file_extn = os.path.splitext(file.filename)
    filename = str(uuid.uuid4()) + file_extn
    file_location = os.path.join(current_app.config["POSTER_FOLDER"], filename)
    while os.path.exists(file_location):
        filename = str(uuid.uuid4()) + file_extn
        file_location = os.path.join(current_app.config["POSTER_FOLDER"], filename)
    file.save(file_location)
    return file_location

class MovieListAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.schema = MovieSchema()

    def get(self):
        movies_list = get_all_movies()
        return movies_list, 200
    
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = request.form
        errors = self.schema.validate(args, partial=("id", "poster", "release_date"))
        if errors:
            return {"errors": errors}, 400
        movie = Movie()
        for attr in args:
            if attr == "release_date":
                date_format = "%Y-%m-%d"
                release_date = datetime.strptime(args["release_date"], date_format)
                setattr(movie, 'release_date', release_date)
            else:
                setattr(movie, attr, args[attr])
        if "poster" in request.files:
            poster = request.files["poster"]
            poster_location = save_poster(poster)
            setattr(movie, "poster", poster_location)
        db.session.add(movie)
        db.session.commit()
        cache.clear()
        serialized_movie = self.schema.dump(movie)
        return serialized_movie, 201

class MovieAPI(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.schema = MovieSchema()

    def get(self, id):
        movie = get_movie(id)
        return movie, 200
    
    @auth_required('token')
    @roles_required('admin')
    def patch(self, id):
        args = request.form
        errors = self.schema.validate(args, partial=('id', 'name',))
        if errors:
            return {'errors': errors}, 400
        movie = db.one_or_404(db.select(Movie).filter_by(id=id))
        if "poster" in request.files:
            if movie.poster != os.path.join(current_app.config["POSTER_FOLDER"], "default.png"):
                os.remove(movie.poster)
            movie.poster = save_poster(request.files["poster"])
        for attr in args:
            if attr == "release_date":
                date_format = "%Y-%m-%d"
                release_date = datetime.strptime(args["release_date"], date_format)
                setattr(movie, 'release_date', release_date)
            else:
                setattr(movie, attr, args[attr])
        db.session.commit()
        cache.clear()
        serialized_movie = self.schema.dump(movie)
        return serialized_movie, 200

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        movie = db.one_or_404(db.select(Movie).filter_by(id=id))
        if movie.poster != os.path.join(current_app.config["POSTER_FOLDER"], "default.png"):
            os.remove(movie.poster)
        db.session.delete(movie)
        db.session.commit()
        cache.clear()
        return None, 204