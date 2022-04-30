from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SubmitField


class UserForm(FlaskForm):

    new_name = StringField("Новое имя")

    new_password = StringField("Новый пароль")

    new_avatar = FileField("Новая аватарка")

    new_description = TextAreaField("О себе")

    save = SubmitField("Сохранить")
