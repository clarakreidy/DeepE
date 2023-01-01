import os
import uuid

import requests
from flask import request

from managers.upload_form import UploadForm


def save_file(form: UploadForm, upload_folder: str) -> str:
    file_name = uuid.uuid4()
    path: str = ''
    if form.url.data != '':
        response = requests.get(form.url.data)
        extension = form.url.data.split(".")[-1]
        path = os.path.join(upload_folder, f'{str(file_name)}.{extension}')
        open(path, "wb").write(response.content)
    elif form.file.data != '':
        file = request.files[form.file.name]
        path = os.path.join(upload_folder, f'{str(file_name)}_{file.filename}')
        file.save(path)
    return path
