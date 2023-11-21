from flask import render_template, request, redirect, url_for, Blueprint
from models.settings import db
from models.topic import Topic
from models.comment import Comment
from handlers.user import user_get

comment_handlers = Blueprint("comment_handlers", __name__)

@comment_handlers.route("/comment-create", methods=["GET", "POST"])
def comment_create():

    user = user_get()
    if request.method == "GET":
        if not user:
            return redirect(url_for("authentication_handlers.login"))
        pass

    elif request.method == "POST":
        body = request.form.get("input-comment")

        Comment.create(body=body, author=user)

        return redirect(url_for("landing_handlers.index"))

@comment_handlers.route("/comment/<comment_id>/comment-delete", methods=["GET", "POST"])
def comment_delete(comment_id):
    comment = db.query(Topic).get(int(comment_id))

    if request.method == "GET":
        return render_template("comment/comment-delete.html", comment=comment)

    elif request.method == "POST":
        user = user_get()

        if not user:
            return redirect(url_for("authentication_handlers.login"))
        elif user.user_id != comment.author_id:
            return "You are not the author of this comment."
        elif "yes" in request.form:
            db.delete(comment)
            db.commit()
        elif "no" in request.form:
            pass

        return redirect(url_for("landing_handlers.index"))