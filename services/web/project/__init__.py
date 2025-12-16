# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialize the db
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object("project.config.Config")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev"
    )   # Will not crash on missing env (...maybe)
    app.config["UPLOAD_FOLDER"] = "uploads"

    db.init_app(app)

    #register app with blueprint
    from .routes import bp
    app.register_blueprint(bp)

    return app


    