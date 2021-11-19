from flask_wtf import FlaskForm
from web_app .models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class RegisterForm(FlaskForm):# this function is to check and see if there is existing email address
    username = StringField(label='User Name', validators=[DataRequired(), Length(min=8, max=20)])
    email_address = StringField(label='Email Address', validators=[DataRequired(), Email()])  # the Email will check if @ sign has been applied
    password1 = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=20)])
    password2 = PasswordField(label='Comfirm password', validators=[DataRequired(), EqualTo('password1')])  # want to the comfirm_password to be equal to the main password
    submit = SubmitField(label='Create Account')

    def validate_username(self, username_to_check):# validate_username is to in order that we have username in the form
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exist! Please try a different email address')


class LoginForm(FlaskForm):
    email_address = StringField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign In')