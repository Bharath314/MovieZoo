from flask import current_app, request
from flask_restful import Resource
from flask_security import current_user, auth_required, hash_password
from zoo.models import db, user_datastore
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

class SignUpAPI(Resource):
    
    def __init__(self) -> None:
        super().__init__()
        self.schema = UserSchema()

    def post(self):
        args = request.get_json()
        print(args)
        errors = self.schema.with_context(password=args['password'],).validate(args, partial=('role', ))
        print(errors)
        if errors:
            print("bruh")
            return {'errors': errors}, 400
        user = user_datastore.create_user(
            email= args['email'],
            password = hash_password(args['password'])
        )
        user_datastore.add_role_to_user(user, 'user')
        db.session.commit()
        return None, 200