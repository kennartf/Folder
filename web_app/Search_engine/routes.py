from flask import flash
from flask import Blueprint
from web_app.posts.routes import post
from .form import SearchForm
from web_app .models import Post
from flask.templating import render_template



Search = Blueprint('Search', __name__)


@Search.app_context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@Search.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        post.searchh = form.searchh.data
        posts = posts.filter(Post.contents.like('%' + post.searchh + '%'))
        posts = posts.order_by(Post.title).all()
        flash(f'You have searched for {post.searchh}', category='success' )
    return render_template('search.html', form=form, searched=post.searchh, posts=posts)

