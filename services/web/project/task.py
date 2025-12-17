from project.celery_app import celery
from project import create_app, db
from project.models import File
from flask import current_app
import os
import uuid



""" Create a celery task making it important for postgres18 testing.
    Because each task performs real concurrent writes
    The result is written to postgresql -> and db commits occur in parallel
    from multiple workers
"""
#@celery.task(bind=True, autometry_for=(Exception), retry_backoff=5, max_retry=3)
@celery.task(bind=True)
def save_uploaded_files(self, filename, data):
    app = create_app()

    with app.app_context():
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        unique_name = f"{uuid.uuid4()}_{filename}"
        path = os.path.join(upload_folder, unique_name)

        with open(path, "wb") as f:
            f.write(data)

        db.session.add(File(filename=filename, file_path=path))
        db.session.commit()

    #return {
    #    "id": db_file.id,
    #    "file_name": db_file.filename
    #}

