from flask import Flask, render_template, request, make_response, redirect,url_for, session
import os
import secrets
import bcrypt
import smartninja_redis

from models.user import User
from models.topic import Topic
from models.comment import Comment
from models.settings import db

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))
app = Flask(__name__)

db.create_all()

def password_hash(password):
    salt = b'customsalt'
    password_hashed = bcrypt.kdf(password.encode(), salt, desired_key_bytes=32, rounds=60)

    return password_hashed

def user_get(user_token=None):
    if not user_token:
        user_token = request.cookies.get("session_token")
    return db.query(User).filter_by(session_token=user_token).first()

@app.context_processor
def context_processor():
    user = user_get()
    return dict(user=user)


@app.route("/", methods=["GET", "POST"])
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

@app.route("/sign-up", methods=["GET", "POST"])
##! prevent going back after sign up (or something) because multiple threads get created and sqlite doesn't like it, same on login !##
def sign_up():
    if request.method == "GET":
        return render_template("sign-up.html")
    elif request.method == "POST":
    # take information from user
        input_name = request.form.get("input-name")
        input_email = request.form.get("input-email")
        input_password = request.form.get("input-password")
        session_token = secrets.token_urlsafe(16)

        user = db.query(User).filter((User.username == input_name) | (User.email == input_email)).all()

        # if new user create session token, hash password and save them to database
        if user:
            return "Sorry there is already a user with that name or email."
        else:
            input_password_hashed = password_hash(input_password)
            print(f"sign_up() session token before saved: {session_token}")

            user = User(username=input_name, email=input_email, password_hash=input_password_hashed,
                        session_token=session_token)
            db.add(user)
            db.commit()
        # Save comment in database
        # input_message = request.form.get("input-message")
        # if input_message:
        #     user_id = user.user_id
        #     comment = Comment(body=input_message, created_at=datetime.now(), user_id=user_id, topic_id=1)
        #     db.add(comment)
        #     db.commit()

        # respond
        response = make_response(redirect(url_for("user_about")))
        response.set_cookie("session_token", session_token)

        return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        input_name = request.form.get("input-name")
        input_password = request.form.get("input-password")

        input_password_hashed = password_hash(input_password)
        user = db.query(User).filter_by(username=input_name, password_hash=input_password_hashed).first()

        if user and user.username == input_name and user.password_hash == input_password_hashed:
            response = make_response(redirect(url_for("user_about")))
            response.set_cookie("session_token", user.session_token)

            return response
        else:
            return "Username or password was incorrect."

@app.route("/topic-create", methods=["GET", "POST"])
def topic_create():
    user = user_get()
    if request.method == "GET":
        if not user:
            return redirect(url_for("login"))

        return render_template("topic-create.html")

    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        Topic.create(title=title, description=description, author=user)

        return redirect(url_for("index"))

@app.route("/topic/<topic_id>/topic-edit", methods=["GET", "POST"])
def topic_edit(topic_id):
    topic = db.query(Topic).get(int(topic_id))

    if request.method == "GET":
        return render_template("topic-edit.html", topic=topic)

    elif request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        user = user_get()

        if not user:
            return redirect(url_for("login"))
        elif user.user_id != topic.author_id:
            return "You are not the author of this topic."
        else:
            topic.title = title
            topic.description = description
            db.add(topic)
            db.commit()

        return redirect(url_for("index"))

@app.route("/topic/<topic_id>/topic-delete", methods=["GET", "POST"])
def topic_delete(topic_id):
    topic = db.query(Topic).get(int(topic_id))

    if request.method == "GET":
        return render_template("topic-delete.html", topic=topic)

    elif request.method == "POST":
        user = user_get()

        if not user:
            return redirect(url_for("login"))
        elif user.user_id != topic.author_id:
            return "You are not the author of this topic."
        else:
            db.delete(topic)
            db.commit()

        return redirect(url_for("index"))


@app.route("/topic/<topic_id>", methods=["GET", "POST"])
def topic_details(topic_id):
    topic = db.query(Topic).get(int(topic_id))
    user = user_get()

    return render_template("topic-details.html", topic=topic, user=user)

@app.route("/users")
def users():
    if request.method == "GET":
        all_users = db.query(User).all()

        return render_template("users.html", users=all_users)

@app.route("/user-about")
def user_about():
    try:
        if request.method == "GET":
            user = user_get()
            if not user:
                return redirect(url_for("login"))

            response = make_response(render_template("user-about.html", name=user.username))

            return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run()