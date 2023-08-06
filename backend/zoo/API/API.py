from pprint import pprint
from flask import request
from zoo import db
from zoo.models import User, Venue
from flask_restful import Resource, reqparse, marshal_with, fields
from zoo.API.schemas import VenueSchema

class VenueAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.schema = VenueSchema()

    def post(self):
        args = request.form
        errors = self.schema.validate(args, partial=('id',))
        if errors:
            return {'errors': errors}, 400 
        venue = Venue(
            name = args['name'],
            capacity = args['capacity'],
            city = args['city']
        )
        db.session.add(venue)
        db.session.commit()
        serialized_venue = self.schema.dump(venue)
        return serialized_venue, 201
    
    def get(self):
        args = request.form
        errors = self.schema.validate(args, partial=('name', 'capacity', 'city'))
        if errors:
            return {'errors': errors}, 400
        venue = db.one_or_404(db.select(Venue).filter_by(id=args['id']))
        serialized_venue = self.schema.dump(venue)
        return serialized_venue, 200   

    def patch(self):
        args = request.form
        errors = self.schema.validate(args, partial=('name', 'capacity', 'city'))
        if errors:
            return {'errors': errors}, 400        
        venue = db.one_or_404(db.select(Venue).filter_by(id=args['id']))
        for attr in args:
            setattr(venue, attr, args[attr])
        db.session.commit()
        print(venue)
        serialized_venue = self.schema.dump(venue)        
        return serialized_venue, 200

    def delete(self):
        print(request.form)
        args = request.form
        errors = self.schema.validate(args, partial=('name', 'capacity', 'city'))
        if errors:
            return {'errors': errors}, 400
        venue = db.one_or_404(db.select(Venue).filter_by(id=args['id']))
        db.session.delete(venue)
        db.session.commit()
        return 204
