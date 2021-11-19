from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email



class ContactForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    contents = TextAreaField(validators=[DataRequired()])