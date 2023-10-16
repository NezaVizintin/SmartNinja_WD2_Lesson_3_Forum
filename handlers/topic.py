from redis import csrf_token_set, csrf_token_check
from flask import render_template, request, redirect, url_for, Blueprint
from models.settings import db
from models.topic import Topic
from models.comment import Comment
from handlers.user import user_get

topic_handlers = Blueprint("topic_handlers", __name__)


# create
@topic_handlers.route("/topic-create", methods=["GET", "POST"])
def topic_create():
    user = user_get()

    if not user:
        return redirect(url_for("authentication_handlers.login"))
    else:
        username = user.username

    if request.method == "GET":
        csrf_token = csrf_token_set(username) # sets a new CSRF token

        return render_template("/topic/topic-create.html", user=user, csrf_token=csrf_token)  # send CSRF token into HTML template

    elif request.method == "POST":
        input_token = request.form.get("input_csrf")  # get csrf from HTML
        if csrf_token_check(input_token, username):
            title = request.form.get("title")
            description = request.form.get("description")

            # create a Topic object
            Topic.create(title=title, description=description, author=user)

            return redirect(url_for("landing_handlers.index"))
        else:
            return "CSRF token is not valid!"

# details
@topic_handlers.route("/topic/<topic_id>", methods=["GET", "POST"])
def topic_details(topic_id):
    topic = db.query(Topic).get(int(topic_id))
    user = user_get()

    if user:
        username = user.username

    if request.method == "GET":
        try:
            comments = db.query(Comment).filter_by(topic_id=topic_id)
        except Exception as e:
            comments = ""
            print(f"Exception retreiving commnets: {e}")
        if user:
            csrf_token = csrf_token_set(username)  # sets a new CSRF token
        else:
            csrf_token = ""

        return render_template("topic/topic-details.html", topic=topic, user=user, comments=comments, csrf_token=csrf_token)   # send CSRF token into HTML template

    elif request.method == "POST":
        input_token = request.form.get("input_csrf")  # get csrf from HTML

        if csrf_token_check(input_token, username):
            body = request.form.get("text")
            Comment.create(body=body, author=user, topic=topic)

            return redirect(url_for("topic_handlers.topic_details", topic_id=topic_id))
        else:
            return "CSRF token is not valid!"


# edit
@topic_handlers.route("/topic/<topic_id>/topic-edit", methods=["GET", "POST"])
def topic_edit(topic_id):
    topic = db.query(Topic).get(int(topic_id))
    user = user_get()

    if not user:
        return redirect(url_for("authentication_handlers.login"))

    elif user.user_id != topic.author_id:
        return "You are not the author of this topic."
    else:
        username = user.username

    if request.method == "GET":
        csrf_token = csrf_token_set(username)  # sets a new CSRF token

        return render_template("topic/topic-edit.html", topic=topic, csrf_token=csrf_token) # send CSRF token into HTML template

    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        input_token = request.form.get("input_csrf")  # get csrf from HTML

        if csrf_token_check(input_token, username):
            topic.title = title
            topic.description = description
            db.add(topic)
            db.commit()

        else:
            return "CSRF token is not valid!"

        return redirect(url_for("landing_handlers.index"))


# delete
@topic_handlers.route("/topic/<topic_id>/topic-delete", methods=["GET", "POST"])
def topic_delete(topic_id):
    topic = db.query(Topic).get(int(topic_id))

    if request.method == "GET":
        return render_template("topic/topic-delete.html", topic=topic)

    elif request.method == "POST":
        user = user_get()

        if not user:
            return redirect(url_for("authentication_handlers.login"))
        elif user.user_id != topic.author_id:
            return "You are not the author of this topic."
        elif "yes" in request.form:
            db.delete(topic)
            db.commit()
        else:
            pass

        return redirect(url_for("landing_handlers.index"))
