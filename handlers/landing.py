from flask import render_template, request, Blueprint
from models.settings import db
from models.topic import Topic

landing_handlers = Blueprint("landing_handlers", __name__)

@landing_handlers.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        try:
            topics = db.query(Topic).all()
        except Exception as e:
            print(f"Error retrieving topics: {str(e)}")
            return render_template("index.html")

        return render_template("index.html", topics=topics)
    elif request.method == "POST":
        pass