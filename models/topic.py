import os
from sqla_wrapper import SQLAlchemy
from datetime import datetime
from models.user import User

# this connects to a database either on Heroku or on localhost
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class Topic(db.Model):
    topic_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    author = db.relationship(User)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, title, text, author):
        topic = cls(title=title, text=text, author=author)
        db.add(topic)
        db.commit()

        return topic

    def User(self):
        return User