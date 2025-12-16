import os
import uuid
from werkzeug.utils import secure_filename
from project.celery_app import celery
from project import db
from project.models import File
from flask import current_app


""" Create a celery task making it important for postgres18 testing.
    Because each task performs real concurrent writes
    The result is written to postgresql -> and db commits occur in parallel
    from multiple workers
"""
@celery.task(bind=True, autometry_for=(Exception), retry_backoff=5, max_retry=3)
def save_uploaded_files(filename, data):

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    path = os.path.join(upload_folder, filename)
    with open(path, "wb") as f:
        f.write(data)

    db.session.add(File(filename=filename, file_path=path))
    db.session.commit()

    #return {
    #    "id": db_file.id,
    #    "file_name": db_file.filename
    #}

