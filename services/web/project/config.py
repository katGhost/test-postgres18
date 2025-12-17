import os


basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    CELERY_BROKER_URL = os.environ.get(
        "CELERY_BROKER_URL",
        "redis://redis:6379/0"
    )

    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND",
        "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev"
    )
