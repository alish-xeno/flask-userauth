from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity
)
from models.user import UserModel

# private variables declaration
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                        )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                        )


# `UserRegister` for new user registration
class UserRegister(Resource):
    def post(self):
        # storage of user input datas into data variable
        data = _user_parser.parse_args() # declaration of required args necessary for creating db row
        # check if `users` db with input username already exists
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400 # return 400 for already exists users
        # if new user create new user model data and save to our database
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201 # success json response with 201


# `User` resource for getting and deleting user
class User(Resource):
    # To get user information, user must be authenticated or logged in
    @jwt_required   # inbuilt method that requires jwt access_token to run the function
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)    # Query user by 'user_id'
        if not user:
            return {"message": "user not found"}, 404   # Returning 404 if not user 
        logged_userid = get_jwt_identity() # getting user_id
        if user_id == logged_userid: # check if user object is of logged_in user
            return user.json()  # Returning json data of user on success
        else:
            # return {"message": "Unaccessible"}
            return {
                'id': user.id,
                'username': user.username
            }
        

    @jwt_required # inbuilt method that requires jwt access_token
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id) # Query user by 'user_id'
        if not user:
            return {"message": "user not found"}, 404 # Returning 404 if user not found
        # if user, then user object is deleted or removed from our database
        logged_userid = get_jwt_identity() # getting user_id
        if user_id == logged_userid: # check if user object is of logged_in user
            user.delete_from_db() # accessing `delete_from_db()` method to delete from our database
            return {"Message": 'user deleted'}, 200 # returning success delete message
        else:
            return {"message": "Access restricted"}


# User can login with this resource
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args() # Get data from parser
        user = UserModel.find_by_username(data['username']) # Find user in database
        if user and safe_str_cmp(user.password, data['password']): # Check password
            access_token = create_access_token(identity=user.id, fresh=True) # Create access token
            refresh_token = create_refresh_token(user.id) # Create refresh token
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200 # Return tokens
        return {"message": "invalid credentials."}, 401 # returning 401 if invalid credentials


# `TokenRefresh` resource to get new fresh access_token for user
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity() # getting current logged_in user 
        new_token = create_access_token(identity=current_user, fresh=False) # creating new fresh access_token for the user
        return {"access_token": new_token}, 200 # returning fresh access_token



