from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_ckeditor import CKEditor
# from flask_ckeditor import CKEditorfield
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .contacts_page.config import  mail_username, mail_password



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends_post.db'
app.config['SECRET_KEY'] = '3af0739eb8aaaa294356e5e9'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config["MAIL_USERNAME"] = mail_username
app.config["MAIL_PASSWORD"] = mail_password
# app.config["MAIL_USERNAME"] = os.environ.get('EMAIL_USER')
# app.config["MAIL_PASSWORD"] =  os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



mail = Mail(app)
bcrypt = Bcrypt(app)
admin = Admin(app)
db = SQLAlchemy(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
login_manager .login_view = 'auth.login'
login_manager .login_message_category = 'info'



from web_app.auth.routes import auth
from web_app.posts.routes import posts
from web_app.views.routes import views
from web_app.errors.handlers import errors
from web_app.main.routes import main_page
from web_app.account.routes import accounts
from web_app.admin_page.routes import admin_
from web_app.Search_engine.routes import Search
from web_app.contacts_page.routes import contact_admin


#https://www.saleshandy.com/smtp/outlook-smtp-settings/
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(posts, url_prefix='/')
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(errors, url_prefix='/')
app.register_blueprint(Search, url_prefix='/')
app.register_blueprint(admin_, url_prefix='/')
app.register_blueprint(accounts, url_prefix='/')
app.register_blueprint(main_page, url_prefix='/')
app.register_blueprint(contact_admin, url_prefix='/')
