from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, ValidationError


def check_password(form, field):
    password_len = len(field.data)

    if password_len < 6:
        raise ValidationError("Пароль должен содержать больше шести символов.")


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), check_password])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), check_password])
    name = StringField('Имя', validators=[DataRequired()])
    description = TextAreaField('Немного о себе')
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
