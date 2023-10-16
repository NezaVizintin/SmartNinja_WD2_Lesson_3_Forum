from flask import render_template, request, make_response, redirect, url_for, Blueprint
from models.settings import db
from models.user import User

user_handlers = Blueprint("user_handlers", __name__)

def user_get(user_token=None):
    if not user_token:
        user_token = request.cookies.get("session_token")
    return db.query(User).filter_by(session_token=user_token).first()

@user_handlers.route("/users")
def users():
    if request.method == "GET":
        all_users = db.query(User).all()

        return render_template("user/users.html", users=all_users)

@user_handlers.route("/user-about")
def user_about():
    if request.method == "GET":
        user = user_get()
        if not user:
            return redirect(url_for("authentication_handlers.login"))

        response = make_response(render_template("user/user-about.html", name=user.username))

        return response
