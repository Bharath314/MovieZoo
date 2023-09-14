from flask import current_app, request
from flask_restful import Resource
from flask_security import current_user, auth_required
from zoo.models import db
from zoo.API.schemas import UserSchema

class CurrentUserAPI(Resource):

    def __init__(self) -> None:
        super().__init__()
        self.schema = UserSchema()

    @auth_required('token')
    def get(self):
        user_dict = {
            'email': current_user.email,
            'role': current_user.roles[0].name,
        }
        serialized_user = self.schema.dump(user_dict)
        return serialized_user, 200
