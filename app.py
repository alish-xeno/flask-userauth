import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister

from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.store import Store, StoreList

app = Flask(__name__)
db_value_conf = os.environ.get('DATABASE_URL', "sqlite:///data.db")
if db_value_conf and db_value_conf.startswith("postgres://"):
    db_value_conf = db_value_conf.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_value_conf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'alish'
api = Api(app)

jwt = JWTManager(app)  # /auth

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    print(identity, '\nhello____________________________')
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
