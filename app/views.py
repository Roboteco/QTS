from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response, session, send_from_directory
from werkzeug.utils import secure_filename
import os



@app.route('/')
def index():
    # тут просто пробрасываем файлик, без всякого препроцессинга
    return app.send_static_file("index.html")
    

@app.route('/<path:path>')
def static_dist(path):
    # тут пробрасываем статику
    return send_from_directory("static/dist", path)
