from flask import Blueprint, request, jsonify, current_app, render_template, \
redirect, url_for, flash
import os
import math
from .models import File
from . import db
from .task import save_uploaded_files


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


""" File upload route / uploading files Asynchronously"""
@bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    # check for files in the folder if 'upload' folder exists
    file = request.files["file"]

    filename=file.filename

    # empty file handling
    if filename == "":
        return jsonify({"error": "No file provided"}), 400
    
    # read bytes
    # dispatch async task without storing unused variable and use keyword args to avoid positional mismatch
    save_uploaded_files.delay(filename=filename, file_bytes=file.read())

    # if file uploaded successfully
    flash("Success: File uploaded succesfully!", "success"), 201
    return redirect(url_for("files.home"))


"""  Endpoint for file deletion """
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

""" Large file error handler """
@bp.errorhandler(413)
def file_too_large(error):
    flash("Files too large"), 413
    return redirect(url_for("files.home"))

    
