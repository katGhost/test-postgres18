# app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


#celery = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'))

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








"""TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery"""
