import os
from sqla_wrapper import SQLAlchemy
from datetime import datetime

# this connects to a database either on Heroku or on localhost
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class Comment(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created_at = db.Column(db.String)
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)