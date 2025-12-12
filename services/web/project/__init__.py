# app.py
import os
from flask import Flask, request, send_from_directory, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('project.config.Config')
db = SQLAlchemy(app)

# create absolute path for upload folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# make sure the directorr exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Defile a model for file metadata
class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)

    def __init__(self, filename):
        self.filename = filename
        self.file_path = os.path.join(UPLOAD_FOLDER, filename)

    def __repr__(self):
        return f'<File {self.filename}>'


# route for home page
@app.route('/')
def index():
    return render_template('index.html')


    