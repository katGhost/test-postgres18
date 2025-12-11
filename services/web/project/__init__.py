# app.py
import os
from flask import Flask, request, send_from_directory, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# route for home page
@app.route('/')
def index():
    return jsonify({'message': 'Hello from Here!'})


    