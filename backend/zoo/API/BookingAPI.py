from flask import request
from flask_restful import Resource
from zoo import db
from zoo.API.schemas import BookingSchema
from zoo.models import Booking

class BookingAPI(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.schema = BookingSchema()

    def post(self):
        args = request.get_json()
        errors = self.schema.validate(args, partial=("id",))
        if errors:
            return {"errors": errors}, 400
        booking = Booking()
        for attr in args:
            setattr(booking, attr, args[attr])
        db.session.add(booking)
        db.session.commit()
        serialized_booking = self.schema.dump(booking)
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
    