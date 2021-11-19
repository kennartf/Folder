from flask import abort
from flask import session
from web_app import admin
from web_app import bcrypt
from datetime import datetime
from flask_login import UserMixin
from web_app import db, login_manager, app
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True, passive_deletes=True)

    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email_address}, '{self.image_file}')"


    
    @property
    def password(self):
        return self.password

    @password.setter
    def hash_password(self, plain_text_password):  
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')  # this will hash the password after it has been set or input

    # this applied to the login to see if the data provided is true
    def check_password_correction(self, attempted_password): # this is to check the and grab the password filled in
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    contents = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255))
    user = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)# the user.id should be in ' ' and small letters

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.contents}')"



class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
admin.add_view(SecureModelView(Post, db.session))

