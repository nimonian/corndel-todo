from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from src.routes.todos import todos_bp


def create_app():
    # create the app
    app = Flask(__name__)

    # apply CORS
    CORS(app)

    # load the config
    app.config.from_pyfile("config.py")

    # connect to the database
    db = SQLAlchemy(app)
    app.config["DB"] = db

    # register the routes
    app.register_blueprint(todos_bp(db), url_prefix="/todos")

    return app
