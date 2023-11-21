from flask import render_template, request, Blueprint

game_handlers = Blueprint("game_handlers", __name__)

@game_handlers.route("/game", methods=["GET"])
def game():
    if request.method == "GET":
        return render_template("game/game.html")