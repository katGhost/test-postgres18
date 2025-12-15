# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the db
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = "uploads"

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app



    