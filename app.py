from datetime import datetime as dt
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json

import os
import shutil
from os import getcwd
from werkzeug.utils import secure_filename

from predictor import predictImage

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html', imgPath=url_for('static', filename='default.jpg'))

# Uploading from front-end
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    # Handle get request
    if request.method == 'GET':
        return redirect(url_for('home'))

    # Deletes any file in the user-uploads
    folder = 'static/user-uploads'

    # Remove all files in user-uploads if there are any
    if len(os.listdir(folder)) != 0:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # The file name is the time of upload
    upload_time = dt.now().strftime('%Y%m%d%H%M%S%f')
    f = request.files['file']
    ext = f.filename.split('.')[-1]

    # Handle non-standard images
    if ext not in ['jpg', 'jpeg', 'png']:
        return render_template(
            'index.html',
            imgPath=url_for('static', filename='default.jpg'),
            error="That's not an image!"
        )

    print('Saving image')
    imgPath = f"static/user-uploads/{upload_time}.{ext}"
    f.save(f'{getcwd()}/{imgPath}')
    print(f'{getcwd()}/{imgPath}')

    print('Predicting...')
    # Predict
    preds = predictImage(imgPath=imgPath, best_only=False)
    preds = [(l.capitalize(), str(round(p, 2))) for (l,p) in preds]

    print('Rendering')
    return render_template('index.html', imgPath=imgPath, preds=preds)

# API functionality
@app.route('/api', methods=['GET', 'POST'])
def api():

    # Handle get request
    if request.method == 'GET':
        return redirect(url_for('home'))

    # The file name is the time of upload
    upload_time = dt.now().strftime('%Y%m%d%H%M%S%f')
    f = request.files['file']
    ext = f.filename.split('.')[-1]

    if ext not in ['jpg', 'jpeg', 'png']:
        return "The file you upload is not an Image!", 400

    imgPath = f"static/user-uploads/{upload_time}.{ext}"
    f.save(f'{getcwd()}/{imgPath}')

    # Predict
    preds = predictImage(imgPath=imgPath, best_only=False)
    preds = [{"label": l.capitalize(), "confidence": str(round(p, 2))} for (l,p) in preds]
    print(preds)

    return json.dumps(preds)

# 404 Not Found Handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404