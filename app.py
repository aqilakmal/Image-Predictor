from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
from os import getcwd
from werkzeug.utils import secure_filename

from predictor import predictImage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', imgPath='./static/default.jpg')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    full_name = f"upload__{secure_filename(f.filename)}"
    imgPath = f"static/user-uploads/{full_name}"
    f.save(f'{getcwd()}/{imgPath}')

    # Predict
    preds = predictImage(imgPath=imgPath, best_only=False)
    preds = [(l.capitalize(), str(round(p, 2))) for (l,p) in preds]

    return render_template('index.html', imgPath=imgPath, preds=preds)