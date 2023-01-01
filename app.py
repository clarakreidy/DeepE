import os
import uuid

import requests
from flask import Flask, render_template, request, redirect, url_for, Response

from managers.file_manager import save_file
from managers.frame_genenrator import generate_frames
from managers.upload_form import UploadForm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/bucket/uploads'
app.config['SECRET_KEY'] = 'secretkey'


@app.route('/', methods=['GET'])
def landing_page():
    return render_template('index.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    form = UploadForm()
    if request.method == 'GET':
        return render_template('upload-form.html', file_name='', form=form, page='video')


@app.route('/image', methods=['GET', 'POST'])
def image():
    form = UploadForm()
    if request.method == 'GET':
        return render_template('upload-form.html', file_name='', form=form, page='image')
    if request.method == 'POST':
        file_name = save_file(form, app.config['UPLOAD_FOLDER'])
    return redirect(url_for('detect'))


@app.route('/feed', methods=['GET'])
def feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera', methods=['GET'])
def camera():
    return render_template('camera.html')


@app.route('/detection', methods=['GET'])
def detect():
    return render_template('result.html')


if __name__ == '__main__':
    app.run()
