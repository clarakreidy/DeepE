import sys

import cv2
from flask import Flask, render_template, request, Response, make_response

from managers.emotion_detection import stream, analyze
from managers.file_manager import save_file
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
    if request.method == 'POST':
        file_name = save_file(form, app.config['UPLOAD_FOLDER'])
    return render_template('result.html', file_name=file_name, page='video')


@app.route('/image', methods=['GET', 'POST'])
def image():
    form = UploadForm()
    if request.method == 'GET':
        return render_template('upload-form.html', file_name='', form=form, page='image')
    if request.method == 'POST':
        file_name = save_file(form, app.config['UPLOAD_FOLDER'])
    return render_template('result.html', file_name=file_name, page='image')


@app.route('/feed', defaults={'source': 0}, methods=['GET'])
@app.route('/feed/<source>', methods=['GET'])
def feed(source):
    if source is not None and source != 0:
        source = f"{app.config['UPLOAD_FOLDER']}/{source}"
    return Response(stream(source), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect', methods=['GET'])
def detect():
    filename = request.args['filename']
    return make_response(analyze(filename))


@app.route('/camera', methods=['GET'])
def camera():
    return render_template('camera.html')


if __name__ == '__main__':
    app.run()
