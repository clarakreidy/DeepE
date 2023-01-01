from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, URLField, SubmitField
from wtforms.validators import url, Optional


class UploadForm(FlaskForm):
    url = URLField('link', validators=[Optional(), url()])
    file = FileField('file', validators=[FileAllowed(['jpeg', 'jpg', 'png'], 'Images only.'), Optional()])

    submit = SubmitField('Upload')
