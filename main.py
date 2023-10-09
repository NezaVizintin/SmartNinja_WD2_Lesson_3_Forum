import os

from models.user import User, db #A MORAM VSAKIČ db? VPRAŠAJ
from models.topic import Topic
from models.comment import Comment

#sys.path.insert(0, "D:\\Neza\\Programiranje\\SmartNinja\\Lekcija-3-forum\\models")

# from models import user, topic, comment, db
# User = user.User
from flask import Flask, render_template, request, make_response, redirect,url_for, session
import secrets
import bcrypt
import smartninja_redis

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))
app = Flask(__name__)
db.create_all()


def password_hash(password):
    salt = b'customsalt'
    password_hashed = bcrypt.kdf(password.encode(), salt, desired_key_bytes=32, rounds=60)

    return password_hashed

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        user_name = request.cookies.get("user_name")
        topics = db.query(Topic).all()

        return render_template("index.html", name=user_name, topics=topics)
    elif request.method == "POST":
        pass

@app.route("/sign-up", methods=["GET", "POST"])
##! prevent going back after sign up (or something) because multiple threads get created and sqlite doesn't like it, same on login !##
def sign_up():
    if request.method == "GET":
        user_name = request.cookies.get("user_name")
        topics = db.query(Topic).all()

        return render_template("sign-up.html", name=user_name, topics=topics)
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
        response.set_cookie("user_name", input_name)

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
            response.set_cookie("user_name", input_name)

            return response
        else:
            return "Username or password was incorrect."

@app.route("/topic-create", methods=["GET", "POST"])
def topic_create():
    if request.method == "GET":

        return render_template("topic-create.html")

    elif request.method == "POST":
        return

@app.route("/users")
def users():
    if request.method == "GET":
        all_users = db.query(User).all()

        return render_template("users.html", users=all_users)

@app.route("/user-about")
def user_about():
    try:
        if request.method == "GET":
            user_name = session.get("user_name")
            response = make_response(render_template("user-about.html", name=user_name))
            if not user_name:
                return redirect(url_for("login"))

            return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run()