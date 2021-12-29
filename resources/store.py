from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)
from models.store import StoreModel


class Store(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('capital',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    _parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    _parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="Every store needs a user_id."
                        )

    @jwt_required  # inbuilt method that requires jwt access_token to run the function
    def get(self, name):
        store = StoreModel.find_by_name(name) # Query `StoreModel` by 'name'
        if store:
            return store.json() # Return Store json if available
        return {'message': 'store not found'}, 404 # Return error message if store not found

    @fresh_jwt_required # inbuilt method that requires 'fresh' jwt access_token
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with name '{}' already exists.".format(name)}, 400 # Return error if store with 'name' already exists
        data = Store._parser.parse_args() # Get data from parser
        store = StoreModel(name, **data) # Set data on `StoreModel`
        try:
            store.save_to_db() # Save data on our database
        except:
            return {"message": "An error occurred inserting the store."}, 500 # Return error if something went wrong
        return store.json(), 201 # Return json data if success

    @jwt_required # inbuilt method that requires jwt access_token
    def delete(self, name):
        # claims = get_jwt_claims() # inbuilt method to see permissions
        # if not claims['is_admin']: # check if 'is_admin' privilege is given
            # return {"message": "Admin privilage required!"}, 401 # return error if not 'is_admin' privilage
        # Continue if 'is_admin'
        user_id = get_jwt_identity() # getting user_id
        store = StoreModel.find_by_name(name) # query `StoreModel` using filter 'name'
        if store and store.user_id == user_id:
            store.delete_from_db() # delete object from db
            return {'message': 'Store deleted.'}
        return {'message': 'Store not found.'}, 404

    @jwt_required # inbuilt method that requires jwt access_token
    def put(self, name):
        data = Store._parser.parse_args() # getting data from parser
        store = StoreModel.find_by_name(name) # query `StoreModel` using filter 'name'
        if store:
            store.capital = data['capital'] # update capital
            store.address = data['address'] # update address
        else:
            store = StoreModel(name, **data) # create new `StoreModel`
        store.save_to_db() # saving to database
        return store.json()


# `StoreList` to return all stores
class StoreList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity() # getting user_id
        if user_id:
            stores = [store.json() for store in StoreModel.query_by_userid(user_id)] # getting all stores of that user
            return {'stores': stores}, 200 # returning all stores data
        stores = [store.json() for store in StoreModel.find_all()] # getting all stores
        return {
            'stores': [store['name'] for store in stores],
            'message': 'More data available if you log in'
        }, 200 # returning only store name if not logged in
