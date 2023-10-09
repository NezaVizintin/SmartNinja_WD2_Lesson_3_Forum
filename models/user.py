import os
from sqla_wrapper import SQLAlchemy
from datetime import datetime

# this connects to a database either on Heroku or on localhost
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    session_token = db.Column(db.String)