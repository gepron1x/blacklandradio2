from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class CommentForm(FlaskForm):

    content = TextAreaField("Введите ваш комментарий")
    submit = SubmitField("Отправить комментарий")
