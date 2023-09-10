from marshmallow import Schema, fields, validates, ValidationError
from zoo import db
from zoo.models import Show, Venue, Movie

class VenueSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    capacity = fields.Int(required=True)
    city = fields.Str(required=True)

    @validates("id")
    def validate_id(self, value):
        if value <= 0:
            raise ValidationError("ID must be greater than 0.")

    @validates("capacity")
    def validate_capacity(self, value):
        if value <= 0:
            raise ValidationError("Capacity must be greater than 0.")

class MovieSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    release_date = fields.DateTime()
    poster = fields.Str(load_only=True)

    @validates("id")
    def validate_id(self, value):
        if value <= 0:
            raise ValidationError("ID must be greater than 0.")

class ShowSchema(Schema):
    id = fields.Int(required=True)
    movie_id = fields.Int(required=True)
    venue_id = fields.Int(required=True)
    tickets_booked = fields.Int()
    price = fields.Int(required=True)

    @validates("id")
    def validate_id(self, value):
        if value <= 0:
            raise ValidationError("ID must be greater than 0.")
    
    @validates("tickets_booked")
    def validate_tickets_booked(self, value):
        show_id = self.context.get('id')
        venue_id = self.context.get('venue_id')
        if venue_id:
            venue = db.one_or_404(db.select(Venue).filter_by(id=venue_id))
            if value > venue.capacity:
                raise ValidationError("Venue capacity exceeded.")
        elif show_id:
            show = db.one_or_404(db.select(Show).filter_by(id=show_id))
            if value > show.venue.capacity:
                raise ValidationError("Venue capacity exceeded.")
    
    def with_context(self, **kwargs):
        contextual_schema = ShowSchema()
        for key in kwargs:
            contextual_schema.context[key] = kwargs[key]
        return contextual_schema
    
class BookingSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    show_id = fields.Int(required=True)
    ticket_count = fields.Int(required=True)

    @validates("id")
    def validate_id(self, value):
        if value <= 0:
            raise ValidationError("ID must be greater than 0.")