from flask import Blueprint, app
from web_app import db
from web_app .utils.picture_utils import save_picture
from flask import render_template, url_for, flash, request, redirect
from flask_login import login_required, current_user
from .forms import UpdateAccountForm


accounts = Blueprint('account', __name__)


@accounts.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data #this is script help us to change our email and username
        current_user.email_address = form.email_address.data
        db.session.commit()
        flash('Your account has been updated! successfully', category='success')
        return redirect(url_for('main_page.main'))
    elif request.method == 'GET':
        form.username.data = current_user.username #this helps by populating the form of user data
        form.email_address.data = current_user.email_address #this helps by populating the form of user data
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form) 
    

