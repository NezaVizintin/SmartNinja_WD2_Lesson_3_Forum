import secrets
from flask import render_template, request, make_response, redirect, url_for, Blueprint
from models.settings import db
from models.user import User
import bcrypt

authentication_handlers = Blueprint("authentication_handlers", __name__)

def password_hash(password):
    salt = b'customsalt'
    password_hashed = bcrypt.kdf(password.encode(), salt, desired_key_bytes=32, rounds=60)

    return password_hashed

@authentication_handlers.route("/sign-up", methods=["GET", "POST"])
##! prevent going back after sign up (or something) because multiple threads get created and sqlite doesn't like it, same on login !##
def sign_up():
    if request.method == "GET":
        return render_template("authorisation/sign-up.html")
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

        # respond
        response = make_response(redirect(url_for("user_handlers.user_about")))
        response.set_cookie("session_token", session_token)

        return response

@authentication_handlers.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("authorisation/login.html")

    elif request.method == "POST":
        input_name = request.form.get("input-name")
        input_password = request.form.get("input-password")
        input_password_hashed = password_hash(input_password)
        user = db.query(User).filter_by(username=input_name, password_hash=input_password_hashed).first()

        if user and user.username == input_name and user.password_hash == input_password_hashed:
            response = make_response(redirect(url_for("user_handlers.user_about")))
            response.set_cookie("session_token", user.session_token)

            return response
        else:
            return "Username or password was incorrect."


@authentication_handlers.route("/logout", methods=["GET", "POST"])
def logout():
    response = make_response(redirect(url_for("landing_handlers.index")))
    response.set_cookie("session_token", "session_token", max_age=0)

    return response
