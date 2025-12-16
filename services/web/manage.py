from flask.cli import FlaskGroup

from project import create_app, db
from project.celery_app import celery

app =create_app()
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    """Create the databse"""
    #db.drop_all()   # make sure ot drop any existing tables
    db.create_all()
    #db.session.commit()
    print("Database created successfully!")

""" Make the celery app availabel""" 
"""
celery = Celery(
    app.import_name,
    backend=app.config["CELERY_RESULT_BACKEND"],
    broker=app.config["CELERY_BROKER_URL"],
)"""

# update app configuration with celery
celery.conf.update(
    backend=app.config["CELERY_RESULT_BACKEND"],
    broker=app.config["CELERY_BROKER_URL"],
)

#
class ContextTask(celery.Task):
    """ Ensure tasks run insde Flask app context """
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        
celery.Task = ContextTask



if __name__ == "__main__":
    cli()