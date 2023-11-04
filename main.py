from flask import Flask
from handlers.user import user_get
from models.settings import db
from handlers import authorisation, landing, topic, user, comment, game

app = Flask(__name__)

db.create_all()

# makes function available to all blueprints
@app.context_processor
def context_processor():
    user = user_get()
    return dict(user=user)

app.register_blueprint(authorisation.authentication_handlers)
app.register_blueprint(landing.landing_handlers)
app.register_blueprint(topic.topic_handlers)
app.register_blueprint(user.user_handlers)
app.register_blueprint(comment.comment_handlers)
app.register_blueprint(game.game_handlers)

if __name__ == "__main__":
    app.run()