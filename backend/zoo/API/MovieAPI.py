import os
from datetime import datetime

from flask import current_app, request
from flask_restful import Resource
from zoo import db
from zoo.API.schemas import MovieSchema
from zoo.models import Movie


def save_poster(movie_name, file):
    _, file_extn = os.path.splitext(file.filename)
    filename = movie_name + file_extn
    file_location = os.path.join(current_app.config["POSTER_FOLDER"], filename)
    file.save(file_location)
    return file_location

class MovieAPI(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.schema = MovieSchema()

    def get(self):
        args = request.form
        errors = self.schema.validate(args, partial=("name", "poster", "release_date"))
        if errors:
            return {"errors": errors}, 400
        movie = db.one_or_404(db.select(Movie).filter_by(id=args["id"]))
        serialized_movie = self.schema.dump(movie)
        return serialized_movie, 200

    def post(self):
        args = request.form
        print(args)
        errors = self.schema.validate(args, partial=("id", "poster"))
        if errors:
            return {"errors": errors}, 400
        movie = Movie()
        for attr in args:
            if attr == "release_date":
                date_format = "%Y-%m-%dT%H:%M:%S"
                release_date = datetime.strptime(args["release_date"], date_format)
                print(type(release_date))
                setattr(movie, 'release_date', release_date)
            else:
                setattr(movie, attr, args[attr])
        if "poster" in request.files:
            poster = request.files["poster"]
            poster_location = save_poster(args["name"], poster)
            setattr(movie, "poster", poster_location)
        db.session.add(movie)
        db.session.commit()
        serialized_movie = self.schema.dump(movie)
        return serialized_movie, 201
    
    def patch(self):
        args = request.form
        errors = self.schema.validate(args, partial=('name',))
        if errors:
            return {'errors': errors}, 400
        movie = db.one_or_404(db.select(Movie).filter_by(id=args["id"]))
        if "poster" in request.files:
            poster = request.files["poster"]
            print("marco")
            if "name" in args:
                if movie.poster == os.path.join(current_app.config["POSTER_FOLDER"], "default.png"):
                    poster_location = save_poster(args["name"], poster)
                    setattr(movie, "poster", poster_location)
                else:
                    os.remove(movie.poster)
                    poster_location = save_poster(args["name"], poster)
                    print(poster_location)
                    setattr(movie, "poster", poster_location)
            elif movie.poster == os.path.join(current_app.config["POSTER_FOLDER"], "default.png"):
                poster_location = save_poster(movie.name, poster)
                print(poster_location)
                setattr(movie, "poster", poster_location)
            else:
                os.remove(movie.poster)
                poster_location = save_poster(movie.name, poster)
                print(poster_location)
                setattr(movie, "poster", poster_location)
        elif "name" in args and movie.poster != os.path.join(current_app.config["POSTER_FOLDER"], "default.png"):
            _, file_extn = os.path.splitext(movie.poster)
            renamed_poster_loc = os.path.join(current_app.config["POSTER_FOLDER"], args['name'] + file_extn)
            os.rename(movie.poster, renamed_poster_loc)
            movie.poster = renamed_poster_loc
        for attr in args:
            if attr == "release_date":
                date_format = "%Y-%m-%dT%H:%M:%S"
                release_date = datetime.strptime(args["release_date"], date_format)
                print(type(release_date))
                setattr(movie, 'release_date', release_date)
            else:
                setattr(movie, attr, args[attr])
        db.session.commit()
        serialized_movie = self.schema.dump(movie)
        return serialized_movie, 200

    def delete(self):
        args = request.form
        errors = self.schema.validate(args, partial=('name',))
        if errors:
            return {'errors': errors}, 400
        movie = db.one_or_404(db.select(Movie).filter_by(id=args["id"]))
        if movie.poster != os.path.join(current_app.config["POSTER_FOLDER"], "default.png"):
            os.remove(movie.poster)
        db.session.delete(movie)
        db.session.commit()
        return 204

        
        

