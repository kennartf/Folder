from web_app import db
from web_app import mail
from flask import Blueprint
from web_app import bcrypt
from flask_mail import Message
from web_app .models import User
from .forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user
from flask import render_template, url_for, flash, redirect
from web_app.posts.forms import  RequestResetForm, ResetPasswordForm




auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()  # this is to call the instance of the the register form
    if form.validate_on_submit():
        user = User(username=form.username.data, email_address=form.email_address.data, hash_password=form.password1.data)  # this is taken the agument from password hash from model
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully! {user.username} You can now login', category='success')
        return redirect(url_for('auth.login'))
    if form.errors != {}:  # if there are not errors from the validations
        for err_msg in form.errors.values():  # fetching the value from dic values
            flash(f'Registration unsuccessful: {err_msg}', category='danger')
    return render_template('signup.html', form=form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():  
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user and user.check_password_correction(attempted_password=form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Success! You are logged in as {user.email_address}', category='success')
            return redirect(url_for('main_page.main'))
        else:
            flash('Login Unsuccessful! Please check email address and password',category='danger')
    return render_template('login.html', form=form)



@auth.route('/logout')  
def logout():
    logout_user()
    flash('You have been loged out successfully', category='success')
    return render_template('home.html') 


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='kenneeartf@gmail.com', recipients=[user.email_address])
    msg.body =  f''' To reset your password, visit the following link: {url_for('auth.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.'''
    mail.send(msg)



@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        send_reset_email(user)
        flash('A link has been sent into your e-mail with instructions to reset your password.', category='info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form)



@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User(password_hash=form.password.data)# this is taken the agument from password hash from model
        user.password_hash = user
        db.session.commit()
        flash('Your password has been reset!!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
