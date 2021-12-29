'''
    This model is explicitely used for defining our `users` row from our created database.
    This model is only representation for single `users` row from our db.
    All connection from client request to our server database for `users` is done inhere. 
'''

# import of database connecting `db` from file db.py
from db import db


# User model for representing database table
class UserModel(db.Model):
    # database table name definition
    __tablename__ = 'users'
    
    # database columns definition of each single row
    id = db.Column(db.Integer, primary_key=True) # auto positive integer number assigned when created
    username = db.Column(db.String(80)) # 'db.String(80)' limits max character length to 80
    password = db.Column(db.String(80)) # 'db.String(80)' limits max character length to 80
    # relation with `ItemModel`
    stores = db.relationship('StoreModel', lazy='dynamic') # lazy='dynamic' for 


    # __init__ function for representing required fields from our database
    def __init__(self, username, password):
        self.username = username
        self.password = password

    '''
        # json function to jsonify object while returning the request
        # while working with api, always return object on json format like below
        # each showable information is returned on json format i.e. dictionary or key-value pair
    '''
    def json(self):
        return {
            'id': self.id,
            "username": self.username,
            'stores': [store.json() for store in self.stores.all()]
        }

    # custom save_to_db method for either creating new or updating the existing object from our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # custom delete_from_db method for deleting our object or single row from our database table
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # custom find_by_username classmethod defined to query our database row using filter_by(username)
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # .first() to return first matched object

    # custom find_by_id classmethod defined to query our database row using filter_by(id)
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() # .first() to return first matched object
