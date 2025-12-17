from flask.cli import FlaskGroup
from project import create_app, db
from project.celery_app import celery
#from project.celery_app import celery

app = create_app()
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    """Create the databse"""
    #db.drop_all()   # make sure ot drop any existing tables
    db.create_all()
    #db.session.commit()
    print("Database created successfully!")

""" Config celery """ 
celery.conf.update(
    broker_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"]
)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask




#celery.Task = ContextTask

if __name__ == "__main__":
    cli()