from flask import request
from flask_restful import Resource
from flask_security import auth_required
from zoo import db
from zoo.API.schemas import BookingSchema
from zoo.models import Booking, Show
from zoo.cache import *

class BookingAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.schema = BookingSchema()

    @auth_required('token')
    def post(self):
        args = request.get_json()
        errors = self.schema.with_context(show_id=args['show_id']).validate(args, partial=("id",))
        if errors:
            return {"errors": errors}, 400
        booking = Booking()
        for attr in args:
            setattr(booking, attr, args[attr])
        db.session.add(booking)
        show = db.one_or_404(db.select(Show).filter_by(id=booking.show_id))
        show.tickets_booked += booking.ticket_count
        db.session.commit()
        serialized_booking = self.schema.dump(booking)
        cache.clear()
        return serialized_booking, 201
    
    def get(self):
        args = request.get_json()
        errors = self.schema.validate(args, partial=("user_id", "show_id", "ticket_count"))
        if errors:
            return {"errors": errors}, 400
        booking = db.one_or_404(db.select(Booking).filter_by(id=args["id"]))
        serialized_booking = self.schema.dump(booking)
        return serialized_booking, 200
    
    def patch(self):
        args = request.get_json()
        errors = self.schema.validate(args, partial=("user_id", "show_id", "ticket_count"))
        if errors:
            return {"errors": errors}, 400
        booking = db.one_or_404(db.select(Booking).filter_by(id=args["id"]))
        for attr in args:
            setattr(booking, attr, args[attr])
        db.session.commit()
        serialized_booking = self.schema.dump(booking)
        return serialized_booking, 200

    def delete(self):
        args = request.get_json()
        errors = self.schema.validate(args, partial=("user_id", "show_id", "ticket_count"))
        if errors:
            return {"errors": errors}, 400
        booking = db.one_or_404(db.select(Booking).filter_by(id=args["id"]))
        db.session.delete(booking)
        db.session.commit()
        return None,204
    