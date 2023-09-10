import os

from flask import request
from flask_restful import Resource
from zoo import db
from zoo.API.schemas import ShowSchema
from zoo.models import Show

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
        return serialized_show, 201
    
    def get(self):
        args = request.get_json()
        errors = self.schema.validate(args, partial=("movie_id", "venue_id", "price",))
        if errors:
            return {"errors": errors}, 400
        show = db.one_or_404(db.select(Show).filter_by(id=args["id"]))
        serialized_show = self.schema.dump(show)
        return serialized_show, 200
    
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
        return serialized_show, 200

    def delete(self):
        args = request.get_json()
        errors = self.schema.validate(args, partial=("movie_id", "venue_id", "price", ))
        if errors:
            return {"error": errors}, 400
        show = db.one_or_404(db.select(Show).filter_by(id=args["id"]))
        db.session.delete(show)
        db.session.commit()
        return None, 204