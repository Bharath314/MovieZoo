from flask import current_app, request
from flask_restful import Resource
from flask_security import current_user, login_user, logout_user, verify_password, login_required
from zoo.models import db

# class UserAPI(Resource):
#     def get(self):
#         return {
#             "email": f"{current_user.email}"
#         }
    
# class LoginResource(Resource):
#     def post(self):
#         args = request.get_json()
#         print(args)
#         user = user_datastore.find_user(email=args["email"])
#         print(user)
#         if user and verify_password(args['password'], user.password):
#             login_user(user)
#             return {'message': 'Login successful'}, 200
#         else:
#             return {'message': 'Invalid credentials'}, 401

# class LogoutResource(Resource):
#     @login_required
#     def post(self):
#         logout_user()
#         return {'message': 'Logout successful'}, 200