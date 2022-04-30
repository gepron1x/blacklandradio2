from flask_wtf import FlaskForm
from wtforms import StringField, SearchField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    value = SearchField('Поиск', validators=[DataRequired()])
