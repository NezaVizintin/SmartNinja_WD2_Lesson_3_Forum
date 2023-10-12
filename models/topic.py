from models.settings import db
from datetime import datetime

class Topic(db.Model):
    topic_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) # Note that SQLAlchemy uses plural when creating table names,
                                                                    # that's why we added users.id in db.ForeignKey()
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship("User") # not an SQL table column. It's just a field that describes
                                    # the relationship with another model (User).

    @classmethod # inserts topic object in to the database
    def create(cls, title, description, author): # cls - method belongs to the class, self - method is related to instance of the class,
                                        # therefore method with cls is accessed by class name where as the one with self is accessed by instance of the class
        topic = cls(title=title, description=description, author=author)
        db.add(topic)
        db.commit()

        return topic