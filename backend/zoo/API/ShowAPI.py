import os

from flask import request
from flask_restful import Resource
from flask_security import auth_required, roles_required
from zoo import db
from zoo.API.schemas import ShowSchema
from zoo.models import Show
from zoo.cache import *

class ShowAPI(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.schema = ShowSchema()

    def post(self):
        args = request.get_json()
        errors = self.schema.with_context(id=args.get("id"), venue_id=args.get("venue_id")).validate(args, partial=("id",))
        if errors:
            return {"errors": errors}, 400
        show = Show()
        for attr in args:
            setattr(show, attr, args[attr])
        db.session.add(show)
        db.session.commit()
        serialized_show = self.schema.dump(show)
        cache.clear()
        return serialized_show, 201
    
    def get(self, id):
        show = get_show(id)
        return show, 200
    
    def patch(self):
        args = request.get_json()
        errors = self.schema.with_context(id=args.get("id"), venue_id=args.get("venue_id")).validate(args, partial=("movie_id", "venue_id", "price", ))
        if errors:
            return {"error": errors}, 400
        show = db.one_or_404(db.select(Show).filter_by(id=args["id"]))
        for attr in args:
            setattr(show, attr, args[attr])
        db.session.commit()
        serialized_show = self.schema.dump(show)
        cache.clear()
        return serialized_show, 200

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        show = db.one_or_404(db.select(Show).filter_by(id=id))
        db.session.delete(show)
        db.session.commit()
        cache.clear()
        return None, 204
    
class VenueShowsAPI(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.schema = ShowSchema()

    def get(self, venue_id):
        shows = get_shows_by_venue()
        return shows, 200

    @auth_required('token')
    @roles_required('admin')
    def post(self, venue_id):
        args = request.get_json()
        show_dict = {
            "movie_id": args['movie_id'],
            "venue_id": venue_id,
            "price": args['price']
        }
        errors = self.schema.with_context(venue_id=venue_id).validate(show_dict, partial=("id",))
        if errors:
            return {"errors": errors}, 400
        show = Show(venue_id=venue_id)
        for attr in args:
            setattr(show, attr, args[attr])
        db.session.add(show)
        db.session.commit()
        cache.clear()
        serialized_show = self.schema.dump(show)
        return serialized_show, 201

class MovieShowsAPI(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.schema = ShowSchema()
    
    def get(self, movie_id):
        shows = get_shows_by_movie(movie_id)
        return shows, 200