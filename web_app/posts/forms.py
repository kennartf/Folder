from flask_wtf import FlaskForm
from web_app.models import User
# from flask_ckeditor import CKEditorfield
from wtforms.fields.simple import PasswordField
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError




class PostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    contents = TextAreaField(label='Content', validators=[DataRequired()])
    # contents = CKEditorfield(label='Content', validators=[DataRequired()])
    submit = SubmitField('Send Post')

class RequestResetForm(FlaskForm):
    email_address = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Reset Password')