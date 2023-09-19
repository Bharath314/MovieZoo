from marshmallow import Schema, fields, validates, ValidationError, pre_load
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
    release_date = fields.Date(load_default=None, allow_none=True)
    poster = fields.Str(dump_only=True)

    @validates("id")
    def validate_id(self, value):
        if value <= 0:
            raise ValidationError("ID must be greater than 0.")
    
class ShowSchema(Schema):
    id = fields.Int(required=True)
    movie_id = fields.Int(required=True)
    movie = fields.Str(dump_only=True)
    venue_id = fields.Int(required=True)
    venue = fields.Str(dump_only=True)
    tickets_booked = fields.Int()
    price = fields.Int(required=True)

    @validates("id")
    def validate_id(self, value):
        if value <= 0:
            raise ValidationError("ID must be greater than 0")
    
    @validates("tickets_booked")
    def validate_tickets_booked(self, value):
        show_id = self.context.get('id')
        venue_id = self.context.get('venue_id')
        if venue_id:
            venue = db.one_or_404(db.select(Venue).filter_by(id=venue_id))
            if value > venue.capacity:
                raise ValidationError("Venue capacity exceeded")
        elif show_id:
            show = db.one_or_404(db.select(Show).filter_by(id=show_id))
            if value > show.venue.capacity:
                raise ValidationError("Venue capacity exceeded")
    
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
            raise ValidationError("ID must be greater than 0")
    
    @validates("ticket_count")
    def validate_ticket_count(self, value):
        show_id = self.context.get("show_id")
        show = db.one_or_404(db.select(Show).filter_by(id=show_id))
        venue = show.venue
        if venue.capacity == show.tickets_booked:
            raise ValidationError("Show is housefull")
        elif show.tickets_booked + value > venue.capacity:
            raise ValidationError(f"There are only {venue.capacity - show.tickets_booked} tickets left")
        
    def with_context(self, **kwargs):
        contextual_schema = BookingSchema()
        for key in kwargs:
            contextual_schema.context[key] = kwargs[key]
        return contextual_schema


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)
    password = fields.Str(load_only=True)
    confirm_password = fields.Str(load_only=True)

    def with_context(self, **kwargs):
        contextual_schema = UserSchema()
        for key in kwargs:
            contextual_schema.context[key] = kwargs[key]
        return contextual_schema

    @validates("confirm_password")
    def validate_confirm_password(self, value):
        print(value)
        password = self.context.get('password')
        if password != value:
            print("happened")
            raise ValidationError("Confirm password doesn't match password")

    #add password validation logic
    