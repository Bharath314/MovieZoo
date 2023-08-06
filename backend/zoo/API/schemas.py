from marshmallow import Schema, fields, validates, ValidationError

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
    
