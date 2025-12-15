from flask import Blueprint, request, jsonify, current_app, render_template
from .models import File
from . import db
import os
from werkzeug.utils import secure_filename
import uuid

bp = Blueprint("files", __name__)

""" Running a basic health check route -> Home"""
@bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")
    #return {"status": "File manager running"}


""" File upload route """
@bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return render_template("404.html"), 400
    
    # check for files in the folder if 'upload' folder exists
    file = request.files["file"]

    # empty file handling
    if file.filename == "":
        return {"error": "No file selected"}, 400

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    # secure filename
    #filename = secure_filename(file.filename)
    filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # upload file
    db_file = File(
        filename=file.filename,
        file_path=file_path
    )

    # add file to db and commit changes
    db.session.add(db_file)
    db.session.commit()

    # if file uploaded successfully
    return {"message": "File uploaded successfully!"}, 201
