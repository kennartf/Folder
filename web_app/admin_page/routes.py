from flask import session
from flask import Blueprint
from .form import AdminForm
from flask.helpers import flash
from flask_login import logout_user
from flask import render_template, redirect, request


admin_ = Blueprint('admin_', __name__)



@admin_.route('/adminlog-kennart', methods=['GET', 'POST'])
def adminlogkennart():
    form = AdminForm()
    if form.validate_on_submit():
        if form.username.data == "kenn" and form.password.data == "art":
            flash(f'You have been logged in successfully', category='success')
            session['logged_in'] = True
            return redirect('/admin')
        else:
            flash('Login unsuccessful!! please check username or password', category='danger')
    return render_template('admin.html', form=form)



@admin_.route('/logout')  
def logout():
    logout_user()
    session.clear()
    flash('You have been loged out successfully', category='success')
    return render_template('home.html') 
