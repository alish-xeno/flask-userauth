from app import app
from db import db

db.init_app(app)

# create db at first request when app runs
@app.before_first_request
def create_tables():
    db.create_all()