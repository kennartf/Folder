from flask import Blueprint
from flask_login import login_required
from web_app .models import Post,User
from flask import render_template, request




main_page = Blueprint('main_page', __name__)


@main_page.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    posts = Post.query.all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return render_template('main.html', posts=posts)
    

@main_page.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)




