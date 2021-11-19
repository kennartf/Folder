from flask_wtf import FlaskForm
from flask_login import current_user
from web_app .models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class UpdateAccountForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired(), Length(min=7, max=20)])
    email_address = StringField(label='Email Address', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Update account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exist! Please try a different username')

    def validate_email_address(self, email_address):
        if email_address.data != current_user.email_address:
            email_address = User.query.filter_by(email_address=email_address.data).first()
            if email_address:
                raise ValidationError('Email Address already exist! Please try a different email address')

    