from web_app import mail
from flask import Blueprint
from flask_mail import Message
from flask import render_template, request, flash



contact_admin = Blueprint('contact_admin', __name__)



@contact_admin.route('contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        email = request.form['email']
        msg = request.form['message']
        message = Message(sender='kenneeartf@gmail.com', recipients=[email])
        message.body = msg
        mail.send(message)
        flash('Message sent successfully', category='success')
    return render_template('home.html')