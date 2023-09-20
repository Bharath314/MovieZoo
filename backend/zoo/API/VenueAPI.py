from flask import request
from flask_security import auth_required, roles_required
from zoo import db
from zoo.models import Venue
from flask_restful import Resource
from zoo.API.schemas import VenueSchema
from zoo.cache import *

class VenueListAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.schema = VenueSchema()

    def get(self):
        venues = get_all_venues()
        return venues, 200
    
    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = request.get_json()
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
        cache.clear()
        serialized_venue = self.schema.dump(venue)
        return serialized_venue, 201

class VenueAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.schema = VenueSchema()
    
    def get(self, id):
        venue = get_venue(id)
        return venue, 200   

    @auth_required('token')
    @roles_required('admin')
    def patch(self, id):
        args = request.get_json()
        errors = self.schema.validate(args, partial=('id', 'name', 'capacity', 'city'))
        if errors:
            return {'errors': errors}, 400        
        venue = db.one_or_404(db.select(Venue).filter_by(id=id))
        for attr in args:
            setattr(venue, attr, args[attr])
        db.session.commit()
        cache.clear()
        serialized_venue = self.schema.dump(venue)        
        return serialized_venue, 200

    @auth_required('token')
    @roles_required('admin')
    def delete(self, id):
        venue = db.one_or_404(db.select(Venue).filter_by(id=id))
        db.session.delete(venue)
        db.session.commit()
        cache.clear()
        return None, 204
