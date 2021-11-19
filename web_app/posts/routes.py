from web_app import db
from flask import Blueprint
from .forms import PostForm
from web_app .models import Post, User
from flask_login import login_required, current_user
from flask import render_template, url_for, flash, request, redirect, abort



posts = Blueprint('posts', __name__)



@posts.route('/new_post', methods=['GET',  'POST']) 
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, contents=form.contents.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('main_page.main'))
    return render_template('newpost.html', form=form, legend='New Post')


@posts.route('/post/<int:post_id>') #This script help us to update a post with an (id)
def post(post_id):
    post = Post.query.get_or_404(post_id) #geting a 
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required  
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.contents = form.contents.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET': #this script helps to populate back when a user want to update it
        form.title.data = post.title
        form.contents.data = post.contents
    return render_template('newpost.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required  
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('main_page.main'))


@posts.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)
