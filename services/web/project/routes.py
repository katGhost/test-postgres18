from flask import Blueprint, request, jsonify, current_app, render_template, \
redirect, url_for, flash
from .models import File
from . import db
import os
from werkzeug.utils import secure_filename
import uuid
import math

bp = Blueprint("files", __name__)

""" Running a basic health check route -> Home"""
@bp.route("/", methods=["GET"])
def home():
    #paagination
    # default values for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # total files count
    total_files = File.query.count()

    # Query the files for the current page
    files = File.query.order_by(File.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # Calculate the total number of pages
    total_pages = math.ceil(total_files / per_page)

    # Render with pagination
    return render_template("index.html", files=files.items, 
        page=page,
        per_page=per_page,
        total_files=total_files,
        total_pages=total_pages
    )

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
        return render_template("404.html"), 400

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
    flash("Success: File uploaded succesfully!", "success"), 201
    return redirect(url_for("files.home"))

# Delete some files
@bp.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    # get file id from the database
    db_file = db.session.query(File).filter(File.id == file_id).first()

    if not db_file:
        flash("Error: File not Found!"), 404
        return redirect(url_for("files.home"))

    # delete file from the upload folder
    try:
        if os.path.exists(db_file.file_path):
            os.remove(db_file.file_path)

        db.session.delete(db_file)
        db.session.commit()
        flash("File deleted successfully!", "primary"), 200

    except Exception as e:
        os.rollback(db.session)
        flash(f"Error deleting file: {str(e)}", "danger"), 500

    return redirect(url_for("files.home"))


    
