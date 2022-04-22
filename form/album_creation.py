from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, \
    IntegerRangeField, MultipleFileField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired


class AlbumCreationForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    year = IntegerField("Год", validators=[DataRequired()])
    description = TextAreaField("Описание")
    cover = FileField('Обложка')
    songs = MultipleFileField('Файлы песен')
    genre = SelectField('Жанр', coerce=str)

    submit = SubmitField('Создать альбом')



