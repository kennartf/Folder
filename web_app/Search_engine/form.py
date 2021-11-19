from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchh = StringField(label='Searched', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

