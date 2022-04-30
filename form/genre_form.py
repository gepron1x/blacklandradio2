from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from data import db_session
from data.album import Genre


def validate_genre(form, field):
    db_sess = db_session.create_session()
    if db_sess.query(Genre).filter(Genre.name == field.data).first():
        raise ValidationError("Жанр с таким именем уже существует!")


class GenreForm(FlaskForm):

    name = StringField('Название', validators=[DataRequired(), validate_genre])

    submit = SubmitField("Добавить жанр")
