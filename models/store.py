'''
    This model is explicitely used for defining our `stores` row from our created database.
    This model is only representation for single `stores` row from our db.
    All connection from client request to our server database for `stores` is done inhere. 
'''

# import of database connecting `db` from file db.py
from db import db


# User model for representing database table
class StoreModel(db.Model):
    # database table name definition
    __tablename__ = 'stores'

    # database columns definition of each single row
    id = db.Column(db.Integer, primary_key=True) # auto positive integer number assigned when created
    name = db.Column(db.String(80)) # 'db.String(80)' limits max character length to 80
    capital = db.Column(db.Float(precision=2)) # float variable with 2 digits after '.' decimal
    address = db.Column(db.String(250)) # 'db.String(250)' limits max character length to 250
    # ForeignKey relational variable
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # relational user id variable
    user = db.relationship('UserModel') # representing model object class

    # __init__ function for representing required fields from our database
    def __init__(self, name, capital, address, user_id):
        self.name = name
        self.capital = capital
        self.address = address
        self.user_id = user_id

    # json function to convert object variables into JSON format for returning the request
    def json(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'capital': self.capital, 
            'address': self.address, 
            'user_id': self.user_id
        }

    # custom find_by_name classmethod defined to query our database row using filter_by(name)
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    # custom find_all classmethod defined to query and return all objects related to this model
    @classmethod
    def find_all(cls):
        return cls.query.all()

    # custom query_by_userid classmethod to query stores using 'user_id' field
    @classmethod
    def query_by_userid(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    # custom save_to_db method for either creating new or updating the existing object from our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # custom delete_from_db method for deleting our object or single row from our database table
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
