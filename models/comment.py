from models.settings import db
from datetime import datetime

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.topic_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    author = db.relationship("User")
    topic = db.relationship("Topic")
