from flask.cli import FlaskGroup

from project import app, db


cli = FlaskGroup(app)

cli.command("create_db")
def create_db():
    """Create the databse"""
    db.drop_all()   # make sure ot drop any existing tables
    db.create_all()
    db.session.commit()



if __name__ == "__main__":
    cli()