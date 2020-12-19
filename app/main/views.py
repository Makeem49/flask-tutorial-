from datetime import datetime
from flask import render_template, url_for, redirect, session, flash, request, current_app 
from app.main.forms import NameForm, EditProfileForm, PostForm 
from app import db 
from app.models import User, Permission, Post
from app.main import main
from app.decorator import admin_required, permission_required
from flask_login import login_required, current_user 
from flask import abort 

 

@main.route('/', methods=['POST', 'GET'])  
def index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data,author=current_user._get_current_object())
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('main.index'))
	page = request.args.get('page', 1, type=int )
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page = page , per_page = current_app.config['FLASKY_POSTS_PER_PAGE'] , error_out = False)
	posts = pagination.items
	return render_template('index.html', pagination = pagination, form=form, posts = posts) 

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	page = request.args.get('page', 1, type=int )
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page = page , per_page = current_app.config['FLASKY_POSTS_PER_PAGE'] , error_out = False)
	posts = pagination.items
	return render_template('user.html', user = user, posts = posts, pagination = pagination )


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your profile has been updated')
		return redirect(url_for('main.user', username = current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form = form )

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_prof_admin():
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user = user)
	if form.validate_on_submit():
		user.email = form.email.data 
		user.name = form.name.data
		user.surname = form.surname.data
		user.comfirmed = form.confirmed.data
		user.role = form.role.data
		user.about_me = form.about_me.data
		user.location = form.location.data
		db.session.commit()
		flash('The profile has been updated')
		return redirect(url_for(main.user, username = user.username))
	form.email.data = user.email
	form.name.data = user.name
	form.surname.data = user.surname
	form.role.data = user.role_id
	form.confirmed.data = user.confirmed
	form.location.data = user.location
	form.about_me.data = user.about_me
	db.session.commit()
	return render_template('edit_profile.html', form = form , user= user)

@main.route('/post/<int:id>', methods = ['GET', 'POST'])
def post(id):
	posts = Post.query.get_or_404(id)
	return render_template('post.html', posts = [post])




























