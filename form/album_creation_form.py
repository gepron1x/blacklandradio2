import datetime
import os

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, \
    MultipleFileField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, ValidationError


def validate_year(form, field):
    if field.data > datetime.date.today().year:
        raise ValidationError('Вы из будущего? Укажите правильный год.')


def validate_songs(form, field):
    if len(field.data) == 0:
        raise ValidationError('Добавьте хоть одну песню!')
    for song_file in field.data:
        if os.path.splitext(song_file.filename)[1] != '.mp3':
            print(song_file, song_file.filename, os.path.splitext(song_file.filename)[1])
            raise ValidationError('Разрешены только mp3 файлы.')


class AlbumCreationForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    year = IntegerField("Год", validators=[DataRequired(), validate_year])
    description = TextAreaField("Описание", validators=[DataRequired()])
    cover = FileField('Обложка', validators=[FileRequired(), FileAllowed(
        ['jpg', 'png', 'gif'], 'Можно загружать только картинки!')])
    songs = MultipleFileField('Файлы песен', validators=[
        validate_songs])
    genre = SelectField('Жанр', coerce=str)
    submit = SubmitField('Создать альбом')
