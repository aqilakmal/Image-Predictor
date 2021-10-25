from datetime import datetime as dt
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json

from os import getcwd
from werkzeug.utils import secure_filename

from predictor import predictImage

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html', imgPath='./static/default.jpg')

# Uploading from front-end
@app.route('/upload', methods=['POST'])
def upload():

    # The file name is the time of upload
    upload_time = dt.now().strftime('%Y%m%d%H%M%S%f')
    f = request.files['file']
    ext = f.filename.split('.')[-1]

    if ext not in ['jpg', 'jpeg', 'png']:
        return redirect(url_for('home'))

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
@app.route('/api', methods=['POST'])
def api():

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